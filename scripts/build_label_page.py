"""Build a self-contained, offline labelling page for the rework precision check.

Reads the sampled links (planning/precision_check/*_strict.csv, from scripts/sample_links.py), fetches
both commits of each link from GitHub with the `gh` CLI (title, date, changed files, and the diff of the
shared files), and writes one HTML file with Yes / No / Unsure buttons. Labels are saved in the browser
as you go and exported as CSV files in the same format the results script reads.

Usage: python scripts/build_label_page.py SAMPLES_DIR [--out label.html] [--max-diff-lines 80]
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

COMMIT = re.compile(r"github\.com/([^/]+/[^/]+)/commit/([0-9a-f]{40})")


def gh_commit(repo: str, sha: str) -> dict:
    r = subprocess.run(["gh", "api", f"repos/{repo}/commits/{sha}"], capture_output=True, text=True)
    if r.returncode != 0:
        return {"error": r.stderr.strip()[:200]}
    d = json.loads(r.stdout)
    msg = d["commit"]["message"]
    return {
        "title": msg.split("\n", 1)[0],
        "body": msg.split("\n", 1)[1].strip()[:600] if "\n" in msg else "",
        "date": d["commit"]["committer"]["date"][:10],
        "files": [{"name": f["filename"], "add": f.get("additions", 0), "del": f.get("deletions", 0),
                   "patch": f.get("patch", "")} for f in d.get("files", [])],
    }


def trim_patch(patch: str, limit: int) -> str:
    lines = patch.splitlines()
    return "\n".join(lines[:limit]) + (f"\n… {len(lines) - limit} more lines" if len(lines) > limit else "")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("samples")
    ap.add_argument("--out", default=None)
    ap.add_argument("--max-diff-lines", type=int, default=80)
    args = ap.parse_args()
    items, wanted = [], set()
    for path in sorted(glob.glob(os.path.join(args.samples, "*_strict.csv"))):
        project = os.path.basename(path).replace("_strict.csv", "")
        for i, row in enumerate(csv.DictReader(open(path, newline=""))):
            a, b = COMMIT.search(row["earlier_commit"]), COMMIT.search(row["fix_commit"])
            items.append({"project": project, "n": i + 1, "earlier_url": row["earlier_commit"], "fix_url": row["fix_commit"],
                          "days": row["days_apart"], "shared": [s.strip() for s in row["shared_files"].split(";") if s.strip()],
                          "repo": a.group(1), "earlier": a.group(2), "fix": b.group(2)})
            wanted |= {(a.group(1), a.group(2)), (b.group(1), b.group(2))}
    with ThreadPoolExecutor(8) as pool:
        fetched = dict(zip(wanted, pool.map(lambda k: gh_commit(*k), wanted)))
    for it in items:
        for side in ("earlier", "fix"):
            c = dict(fetched[(it["repo"], it[side])])
            if "files" in c:
                shared = set(it["shared"])
                c["shared_diffs"] = [{"name": f["name"], "patch": trim_patch(f["patch"], args.max_diff_lines)}
                                     for f in c["files"] if f["name"] in shared]
                c["other_files"] = [f"{f['name']} (+{f['add']} −{f['del']})" for f in c["files"] if f["name"] not in shared]
                del c["files"]
            it[side + "_data"] = c
    out = args.out or os.path.join(args.samples, "label.html")
    html = TEMPLATE.replace("/*DATA*/", json.dumps(items).replace("</", "<\\/"))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    errors = sum("error" in it[s + "_data"] for it in items for s in ("earlier", "fix"))
    print(f"wrote {out}: {len(items)} links from {len({i['project'] for i in items})} projects ({errors} fetch errors)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Rework precision check: labelling</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
 :root { --bg:#fafafa; --card:#fff; --ink:#1f2328; --muted:#59636e; --line:#d1d9e0; --yes:#1a7f37; --no:#cf222e; --unsure:#9a6700; --accent:#0969da; }
 * { box-sizing: border-box; }
 body { margin:0; font:15px/1.45 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color:var(--ink); background:var(--bg); }
 header { position:sticky; top:0; z-index:2; background:var(--card); border-bottom:1px solid var(--line); padding:10px 20px; display:flex; gap:14px; align-items:center; flex-wrap:wrap; }
 header h1 { font-size:16px; margin:0 12px 0 0; }
 select, input[type=text] { font:inherit; padding:5px 8px; border:1px solid var(--line); border-radius:6px; }
 .bar { flex:1; min-width:160px; height:8px; background:#eaeef2; border-radius:4px; overflow:hidden; }
 .bar > div { height:100%; background:var(--accent); width:0; }
 main { max-width:1280px; margin:0 auto; padding:16px 20px 120px; }
 .q { background:#ddf4ff; border:1px solid #b6e3ff; border-radius:8px; padding:10px 14px; margin-bottom:14px; }
 .meta { color:var(--muted); font-size:13px; }
 .cols { display:grid; grid-template-columns:1fr 1fr; gap:14px; }
 @media (max-width:900px) { .cols { grid-template-columns:1fr; } }
 .card { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:12px 14px; min-width:0; }
 .card h2 { font-size:13px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); margin:0 0 6px; }
 .title { font-weight:600; font-size:15px; margin:2px 0 6px; word-break:break-word; }
 .body { white-space:pre-wrap; color:var(--muted); font-size:13px; max-height:7em; overflow:auto; }
 pre { background:#f6f8fa; border:1px solid var(--line); border-radius:6px; padding:8px; overflow:auto; font:12px/1.4 ui-monospace, SFMono-Regular, Menlo, monospace; max-height:420px; }
 .add { color:#116329; background:#dafbe1; display:block; } .del { color:#82071e; background:#ffebe9; display:block; } .hunk { color:var(--accent); display:block; }
 .fname { font:12px ui-monospace, Menlo, monospace; font-weight:600; margin:8px 0 2px; }
 details { margin-top:6px; font-size:13px; color:var(--muted); }
 footer { position:fixed; bottom:0; left:0; right:0; background:var(--card); border-top:1px solid var(--line); padding:10px 20px; display:flex; gap:10px; align-items:center; flex-wrap:wrap; justify-content:center; }
 button { font:inherit; padding:8px 16px; border-radius:6px; border:1px solid var(--line); background:var(--card); cursor:pointer; }
 button.yes { border-color:var(--yes); color:var(--yes); } button.no { border-color:var(--no); color:var(--no); } button.unsure { border-color:var(--unsure); color:var(--unsure); }
 button.on.yes { background:var(--yes); color:#fff; } button.on.no { background:var(--no); color:#fff; } button.on.unsure { background:var(--unsure); color:#fff; }
 #note { width:280px; }
 kbd { font:11px ui-monospace, Menlo, monospace; border:1px solid var(--line); border-bottom-width:2px; border-radius:4px; padding:0 4px; color:var(--muted); }
 a { color:var(--accent); }
 .err { color:var(--no); }
</style></head><body>
<header>
 <h1>Rework precision check</h1>
 <label>Labeller <input type="text" id="who" placeholder="your name" size="12"></label>
 <label>Project <select id="proj"></select></label>
 <div class="bar"><div id="prog"></div></div><span id="count" class="meta"></span>
 <button id="export">Export CSV</button>
</header>
<main>
 <div class="q"><b>Question:</b> does the <b>later commit</b> fix something the <b>earlier commit</b> introduced or broke?
 <b>Yes</b> if it repairs, corrects or reverts the earlier change; <b>No</b> if they only touched the same file for unrelated reasons; <b>Unsure</b> if you can't tell.
 <span class="meta">Diffs show only the shared files. Use the links for full context.</span></div>
 <div id="pair"></div>
</main>
<footer>
 <button id="prev">← Prev</button>
 <button class="yes" data-v="yes">Yes <kbd>Y</kbd></button>
 <button class="no" data-v="no">No <kbd>N</kbd></button>
 <button class="unsure" data-v="unsure">Unsure <kbd>U</kbd></button>
 <input type="text" id="note" placeholder="note (optional)">
 <button id="next">Next →</button>
</footer>
<script>
const ITEMS = /*DATA*/;
const KEY = "rework-precision-labels-v1";
let labels = JSON.parse(localStorage.getItem(KEY) || "{}");
let who = localStorage.getItem(KEY + "-who") || "";
const projects = [...new Set(ITEMS.map(i => i.project))].sort((a, b) => (b === "homebrew") - (a === "homebrew") || a.localeCompare(b));
const sel = document.getElementById("proj");
projects.forEach(p => sel.add(new Option(p, p)));
let proj = projects[0], idx = 0;
const id = it => it.project + "#" + it.n;
const list = () => ITEMS.filter(i => i.project === proj);
document.getElementById("who").value = who;
document.getElementById("who").oninput = e => { who = e.target.value; localStorage.setItem(KEY + "-who", who); };
function esc(s) { return String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
function diff(p) {
  return esc(p).split("\n").map(l => l.startsWith("@@") ? `<span class="hunk">${l}</span>` :
    l.startsWith("+") ? `<span class="add">${l}</span>` : l.startsWith("-") ? `<span class="del">${l}</span>` : l + "\n").join("");
}
function side(label, url, d) {
  if (d.error) return `<div class="card"><h2>${label}</h2><p class="err">Couldn't fetch: ${esc(d.error)}</p><a href="${url}" target="_blank">Open on GitHub</a></div>`;
  const diffs = d.shared_diffs.map(f => `<div class="fname">${esc(f.name)}</div><pre>${f.patch ? diff(f.patch) : "(no textual diff)"}</pre>`).join("");
  const others = d.other_files.length ? `<details><summary>${d.other_files.length} other files changed</summary>${d.other_files.map(esc).join("<br>")}</details>` : "";
  return `<div class="card"><h2>${label} · ${esc(d.date)} · <a href="${url}" target="_blank">GitHub ↗</a></h2>
    <div class="title">${esc(d.title)}</div>${d.body ? `<div class="body">${esc(d.body)}</div>` : ""}${diffs}${others}</div>`;
}
function render() {
  const L = list(), it = L[idx], lab = labels[id(it)] || {};
  document.getElementById("pair").innerHTML =
    `<p class="meta">${esc(it.project)} · link ${it.n} of ${L.length} · ${esc(it.days)} days apart · shared: ${it.shared.map(esc).join(", ")}</p>
     <div class="cols">${side("Earlier commit", it.earlier_url, it.earlier_data)}${side("Later commit (flagged as its fix)", it.fix_url, it.fix_data)}</div>`;
  document.querySelectorAll("footer [data-v]").forEach(b => b.classList.toggle("on", b.dataset.v === lab.v));
  document.getElementById("note").value = lab.note || "";
  const done = L.filter(i => labels[id(i)] && labels[id(i)].v).length, all = ITEMS.filter(i => labels[id(i)] && labels[id(i)].v).length;
  document.getElementById("prog").style.width = (100 * done / L.length) + "%";
  document.getElementById("count").textContent = `${done}/${L.length} in ${proj} · ${all}/${ITEMS.length} overall`;
  window.scrollTo(0, 0);
}
function save(v) {
  const it = list()[idx]; const k = id(it);
  labels[k] = { v: v ?? (labels[k] || {}).v, note: document.getElementById("note").value };
  localStorage.setItem(KEY, JSON.stringify(labels));
}
function go(d) { save(); idx = Math.max(0, Math.min(list().length - 1, idx + d)); render(); }
document.querySelectorAll("footer [data-v]").forEach(b => b.onclick = () => { save(b.dataset.v); if (idx < list().length - 1) go(1); else render(); });
document.getElementById("prev").onclick = () => go(-1);
document.getElementById("next").onclick = () => go(1);
document.getElementById("note").onchange = () => save();
sel.onchange = () => { save(); proj = sel.value; idx = 0; render(); };
document.addEventListener("keydown", e => {
  if (e.target.tagName === "INPUT") return;
  const m = { y: "yes", n: "no", u: "unsure" }[e.key.toLowerCase()];
  if (m) document.querySelector(`footer [data-v="${m}"]`).click();
  if (e.key === "ArrowRight") go(1); if (e.key === "ArrowLeft") go(-1);
});
document.getElementById("export").onclick = () => {
  save();
  if (!who.trim()) { alert("Enter your name in 'Labeller' first, so two people's labels stay separate."); return; }
  const slug = who.trim().toLowerCase().replace(/[^a-z0-9]+/g, "-");
  projects.forEach(p => {
    const rows = [["earlier_commit","fix_commit","days_apart","shared_files","real_fix (yes/no)","note"]];
    ITEMS.filter(i => i.project === p).forEach(i => { const l = labels[id(i)] || {}; rows.push([i.earlier_url, i.fix_url, i.days, i.shared.join("; "), l.v || "", l.note || ""]); });
    const csv = rows.map(r => r.map(x => /[",\n]/.test(x) ? `"${String(x).replace(/"/g, '""')}"` : x).join(",")).join("\n") + "\n";
    const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
    a.download = `${p}_strict.labels.${slug}.csv`; a.click();
  });
};
render();
</script></body></html>
"""

if __name__ == "__main__":
    main()
