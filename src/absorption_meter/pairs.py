"""Paired metrics and decision rules.

Each DORA metric lags: it moves after the damage is done. Each is paired with a
leading indicator of absorption. A DORA metric that improves or holds steady
while its paired indicator worsens is the signature of hidden delivery debt.

Every measure is compared with the team's *own* trailing baseline, never with a
universal threshold: the recent window (default 3 months) against the months
before it (default 6). A move counts if it exceeds ``k`` standard deviations of
the baseline (default 1) and a minimum practical size. With ``robust``, the
median and the median absolute deviation replace the mean and standard
deviation, so one unusual month can't set the bar. These are starting
heuristics: calibrate them against your own history.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, median, pstdev
from typing import Dict, List, Optional, Sequence

from .metrics import Analysis, MonthStats

UP, DOWN, FLAT, NA = "up", "down", "flat", "n/a"

DEBT = "debt-signal"
OK = "no-signal"
INSUFFICIENT = "insufficient-data"

SCALE, HOLD, ADDRESS, UNKNOWN = "scale", "hold", "address", "insufficient-data"


@dataclass
class Settings:
    recent: int = 3
    baseline: int = 6
    k: float = 1.0
    robust: bool = False   # median and MAD instead of mean and standard deviation


@dataclass
class Trend:
    direction: str
    baseline: Optional[float]
    recent: Optional[float]

    def __str__(self) -> str:
        if self.direction == NA:
            return NA
        return f"{self.direction} ({_fmt(self.baseline)} → {_fmt(self.recent)})"


@dataclass
class PairResult:
    pair: str
    dora_metric: str
    dora: Trend
    indicator: str
    signal: Trend
    status: str
    debt_type: str
    reading: str


@dataclass
class Recommendation:
    verdict: str
    rules: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    reading: str = ""


def _fmt(value: Optional[float]) -> str:
    if value is None:
        return "–"
    if abs(value) < 1:
        return f"{value:.2f}"
    return f"{value:.1f}"


def trend(
    rows: Sequence[MonthStats],
    attr: str,
    settings: Settings = Settings(),
    rel_min: float = 0.10,
    abs_min: Optional[float] = None,
) -> Trend:
    """Direction of the recent window against the team's trailing baseline.

    A move counts when it is larger than ``k`` baseline standard deviations
    *and* larger than a practical minimum: ``abs_min`` for rates (e.g. 0.02, two
    percentage points) or ``rel_min`` of the baseline mean for everything else.
    """
    need = settings.recent + settings.baseline
    values = [getattr(r, attr) for r in rows][-need:]
    if len(values) < need:
        return Trend(NA, None, None)
    base = [v for v in values[:settings.baseline] if v is not None]
    recent = [v for v in values[settings.baseline:] if v is not None]
    if len(base) < max(2, settings.baseline // 2) or len(recent) < max(1, settings.recent - 1):
        return Trend(NA, None, None)
    if settings.robust:
        b, r = median(base), median(recent)
        spread = 1.4826 * median(abs(v - b) for v in base)   # MAD, scaled to match a normal SD
    else:
        b, r = mean(base), mean(recent)
        spread = pstdev(base)
    minimum = abs_min if abs_min is not None else rel_min * abs(b)
    threshold = max(settings.k * spread, minimum)
    diff = r - b
    if threshold == 0:
        direction = UP if diff > 0 else DOWN if diff < 0 else FLAT
    else:
        direction = UP if diff > threshold else DOWN if diff < -threshold else FLAT
    return Trend(direction, round(b, 4), round(r, 4))


def _status(dora_ok: bool, worsening: bool, available: bool) -> str:
    if not available:
        return INSUFFICIENT
    return DEBT if dora_ok and worsening else OK


def indicators(analysis: Analysis, s: Settings) -> Dict[str, Trend]:
    rows = analysis.months
    t = {
        "production": trend(rows, "production", s),
        "absorption_ratio": trend(rows, "absorption_ratio", s, abs_min=0.02),
        "changes": trend(rows, "changes", s),
        "releases": trend(rows, "releases", s),
        "rework_rate": trend(rows, "rework_rate", s, abs_min=0.02),
        "untested_share": trend(rows, "untested_share", s, abs_min=0.03),
        "mutation_score": trend(rows, "mutation_score", s, abs_min=0.03),
        "mean_dirs": trend(rows, "mean_dirs", s),
        "median_lines": trend(rows, "median_lines", s),
        "contract_drift_per_100": trend(rows, "contract_drift_per_100", s, abs_min=0.5),
        "patch_release_rate": trend(rows, "patch_release_rate", s, abs_min=0.05),
        "revert_rate": trend(rows, "revert_rate", s, abs_min=0.01),
        "recovery_hours": trend(rows, "recovery_hours", s, rel_min=0.20),
        "time_to_detect_hours": trend(rows, "time_to_detect_hours", s, rel_min=0.20),
        "telemetry_coverage": trend(rows, "telemetry_coverage", s, abs_min=0.05),
        "median_lead_hours": trend(rows, "median_lead_hours", s),
        "median_first_review_hours": trend(rows, "median_first_review_hours", s),
        "review_comments_per_100_lines": trend(rows, "review_comments_per_100_lines", s),
        "median_pr_lines": trend(rows, "median_pr_lines", s),
    }
    return t


def evaluate(analysis: Analysis, settings: Optional[Settings] = None) -> List[PairResult]:
    s = settings or Settings()
    t = indicators(analysis, s)
    window = f"needs {s.recent + s.baseline} months of history"
    results: List[PairResult] = []

    # 1. Deployment frequency <-> verification effectiveness (verification). Rework rate is itself a DORA
    #    outcome, so it corroborates the reading rather than serving as the leading signal.
    df_key = "releases" if analysis.releases_used else "changes"
    df_name = "Deployment frequency (" + ("releases/month" if analysis.releases_used else "merged changes/month, proxy") + ")"
    df, rework = t[df_key], t["rework_rate"]
    if t["mutation_score"].direction != NA:
        verif, verif_name, weakening = t["mutation_score"], "Verification effectiveness (mutation score)", t["mutation_score"].direction == DOWN
    else:
        verif, verif_name = t["untested_share"], "Verification effectiveness (code changes merged without tests)"
        weakening = verif.direction == UP
    available = NA not in (df.direction, verif.direction)
    status = _status(df.direction == UP, weakening, available)
    also = " Rework, the corroborating outcome, is rising too." if rework.direction == UP else ""
    reading = {DEBT: "Busier, not faster: deployments are rising while verification weakens." + also,
               OK: "Verification keeps pace with deployment." + also, INSUFFICIENT: window.capitalize() + "."}[status]
    results.append(PairResult("Deployment frequency ↔ Verification effectiveness", df_name, df, verif_name, verif,
                              status, "verification", reading))

    # 2. Lead time <-> decision latency and change cost (decision, coupling)
    lead, latency = t["median_lead_hours"], t["median_first_review_hours"]
    depth, pr_size = t["review_comments_per_100_lines"], t["median_pr_lines"]
    cost_up = t["mean_dirs"].direction == UP or t["median_lines"].direction == UP
    thinning = pr_size.direction == UP and depth.direction == DOWN
    if analysis.pr_data and lead.direction != NA:
        speed_ok = lead.direction in (DOWN, FLAT)
        worsening = latency.direction == UP or thinning or cost_up
        status = _status(speed_ok, worsening, True)
        why = [w for w, on in (("changes wait longer for a first review", latency.direction == UP),
                               ("PRs grow while review depth falls", thinning),
                               ("each change touches more of the system", cost_up)) if on]
        reading = ("Lead time looks fine, but " + "; ".join(why) + "." if status == DEBT
                   else "Decisions and change cost keep pace.")
        debt = "decision" if (latency.direction == UP or thinning) else "coupling"
    else:
        # Without PR data, read change cost against merged-change throughput.
        throughput = t["changes"]
        available = NA not in (throughput.direction, t["mean_dirs"].direction)
        status = _status(throughput.direction in (UP, FLAT), cost_up, available)
        lead = Trend(NA, None, None)
        reading = {DEBT: "Each change costs more (more areas or lines per change): look for hidden coupling. "
                         "Add --github for decision latency.",
                   OK: "Change cost is steady. Add --github for decision latency.",
                   INSUFFICIENT: window.capitalize() + "."}[status]
        debt = "coupling"
    signal = latency if analysis.pr_data and latency.direction != NA else (
        t["mean_dirs"] if t["mean_dirs"].direction == UP or t["median_lines"].direction != UP else t["median_lines"])
    results.append(PairResult("Lead time ↔ Decision latency + Change cost", "Lead time (PR opened → merged, hours)", lead,
                              "Decision latency; review depth; areas and lines per change", signal,
                              status, debt, reading))

    # 3. Change failure rate <-> contract drift rate (contract)
    cfr_key = "patch_release_rate" if analysis.releases_used else "revert_rate"
    cfr_name = ("Change failure rate (releases patched within 7 days)" if analysis.releases_used
                else "Change failure rate (revert rate, proxy)")
    cfr, drift = t[cfr_key], t["contract_drift_per_100"]
    recent_drift = sum(r.contract_drift for r in analysis.months[-s.recent:])
    drift_worse = drift.direction == UP or (recent_drift > 0 and drift.direction != DOWN)
    available = cfr.direction != NA
    status = _status(cfr.direction in (DOWN, FLAT), drift_worse, available)
    reading = {DEBT: f"Failure rate looks steady, but {recent_drift} contract change(s) in the last {s.recent} months "
                     "broke compatibility without a version bump: failures may be hiding downstream.",
               OK: "No silent contract changes.", INSUFFICIENT: window.capitalize() + "."}[status]
    results.append(PairResult("Change failure rate ↔ Contract drift", cfr_name, cfr,
                              "Contract drift (breaking schema changes without a version bump, per 100 changes)", drift,
                              status, "contract", reading))

    # 4. Recovery time <-> telemetry coverage and time to detect (observability)
    rec, cov, ttd = t["recovery_hours"], t["telemetry_coverage"], t["time_to_detect_hours"]
    has_obs = NA not in (cov.direction,) or NA not in (ttd.direction,)
    worsening = cov.direction == DOWN or ttd.direction == UP
    status = _status(rec.direction in (DOWN, FLAT) or rec.direction == NA, worsening, has_obs)
    reading = {DEBT: "Recovery looks fine, but " + " and ".join(
                   w for w, on in (("telemetry coverage is falling", cov.direction == DOWN),
                                   ("failures take longer to detect", ttd.direction == UP)) if on) + ".",
               OK: "Observability keeps pace.",
               INSUFFICIENT: "Needs team data: pass --team-metrics with telemetry_coverage or time_to_detect_hours."}[status]
    results.append(PairResult("Recovery time ↔ Telemetry coverage", "Recovery time (hours to patch or restore)", rec,
                              "Telemetry coverage; time to detect", cov if cov.direction != NA else ttd,
                              status, "observability", reading))
    return results


ORDER = ("contract", "verification", "observability", "coupling")
ACTIONS = {
    "contract": "R2 · Contracts first: version the schemas that drifted and fail CI on breaking changes.",
    "verification": "R3 · Automated verification: acceptance tests from the spec, property or mutation tests where verification is weakest and rework is highest.",
    "observability": "R4 · Telemetry: make instrumentation part of done; set SLOs and alerts on the new paths.",
    "coupling": "R5 · Simplification: a budget for removing coupling, sized to the share of code AI writes.",
    "decision": "R6 · Governance: cap PR size and require a decision record for high-risk changes.",
}


def recommend(analysis: Analysis, settings: Optional[Settings] = None) -> Recommendation:
    """Apply rules R0–R6. Actions come in the default order C, A, T, S (a hypothesis, not a finding);
    when change cost is the dominant constraint, simplification may come first."""
    s = settings or Settings()
    t = indicators(analysis, s)
    rec = Recommendation(verdict=UNKNOWN)

    production, ar = t["production"], t["absorption_ratio"]
    if NA in (production.direction, ar.direction):
        rec.reading = f"Needs {s.recent + s.baseline} months of history to compare against a baseline."
        return rec

    recent_drift = sum(r.contract_drift for r in analysis.months[-s.recent:])
    fired = {
        "contract": t["contract_drift_per_100"].direction == UP or (
            recent_drift > 0 and t["contract_drift_per_100"].direction != DOWN),
        "verification": t["rework_rate"].direction == UP or t["untested_share"].direction == UP
                        or t["mutation_score"].direction == DOWN,
        "observability": t["time_to_detect_hours"].direction == UP or t["recovery_hours"].direction == UP
                         or t["telemetry_coverage"].direction == DOWN,
        "coupling": t["mean_dirs"].direction == UP or t["median_lines"].direction == UP,
        "decision": t["median_first_review_hours"].direction == UP or (
            t["median_pr_lines"].direction == UP and t["review_comments_per_100_lines"].direction == DOWN),
    }
    # R3 applies when verification weakens or rework rises, and contract drift doesn't explain it.
    if fired["contract"]:
        fired["verification"] = False

    if production.direction == UP and ar.direction == DOWN:
        rec.verdict = HOLD
        rec.rules.append("R1")
        rec.reading = ("Production is rising while the absorption ratio falls: pause expansion and use the "
                       "diagnostic matrix to identify the control requiring investment.")
    elif any(fired.values()):
        rec.verdict = ADDRESS
        rec.reading = "Absorption is holding, but an indicator has moved: fix it before scaling further."
    else:
        rec.verdict = SCALE
        rec.rules.append("R0")
        rec.reading = ("Absorption ratio is steady or rising and no indicator has fired: conditions support "
                       "cautiously expanding AI-assisted delivery while monitoring the paired indicators. "
                       "A steady ratio is not proof of safety.")

    for kind in ORDER:
        if fired[kind]:
            rec.rules.append(ACTIONS[kind].split(" ·")[0])
            rec.actions.append(ACTIONS[kind])
    if fired["decision"]:
        rec.rules.append("R6")
        rec.actions.append(ACTIONS["decision"])
    return rec
