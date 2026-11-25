"""Write figures/homebrew.dat (worked-example figure data) from the Homebrew example outputs.

Final monthly P and AR come from examples/homebrew/monthly.csv; the Hold flag comes from the
month-by-month replay in examples/homebrew/timeline.csv (what a team would have seen at the time).
"""

import csv

monthly = {r["month"]: r for r in csv.DictReader(open("examples/homebrew/monthly.csv"))}
timeline = {r["as_of"]: r for r in csv.DictReader(open("examples/homebrew/timeline.csv"))}
with open("figures/homebrew.dat", "w") as fh:
    fh.write("i month production ar hold\n")
    for i, (month, r) in enumerate(sorted(monthly.items())):
        if not r["absorption_ratio"]:
            continue
        hold = 1 if timeline.get(month, {}).get("verdict") == "hold" else 0
        fh.write(f"{i} {month} {float(r['production']):.1f} {float(r['absorption_ratio']):.4f} {hold}\n")
print("wrote figures/homebrew.dat")
