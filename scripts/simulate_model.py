"""Illustrative stock-and-flow model of delivery debt (paper, Figure 1).

The parameters are illustrative, not fitted to data. The model shows the
mechanism: when production outruns absorption, unabsorbed change becomes latent
debt; latent debt surfaces after a delay as rework; rework takes capacity away
from new work. One feedback loop with a delay is enough to turn a step up in
production into a spike, a dip and a slow recovery.

Usage: python scripts/simulate_model.py [output.dat]
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import List


@dataclass
class Params:
    months: int = 36
    adopt_at: int = 6          # month AI adoption starts
    ramp: int = 3              # months for production to reach its new level
    p_before: float = 100.0    # production capacity before adoption (changes/month)
    p_after: float = 160.0     # production capacity after adoption
    a_before: float = 105.0    # absorption capacity
    a_growth: float = 0.0      # absorption added per month after adoption (CATS investment)
    a_max: float = 175.0
    surface_delay: float = 3.0 # mean months before latent debt surfaces
    repay_share: float = 0.5   # share of surfaced rework repaid each month
    rework_cost: float = 1.0   # production lost per unit of rework


def simulate(p: Params) -> List[dict]:
    latent = rework = 0.0
    rows = []
    for t in range(p.months + 1):
        if t < p.adopt_at:
            capacity = p.p_before
        else:
            capacity = p.p_before + (p.p_after - p.p_before) * min(1.0, (t - p.adopt_at + 1) / p.ramp)
        absorb = p.a_before + (p.a_growth * max(0, t - p.adopt_at + 1) if t >= p.adopt_at else 0.0)
        absorb = min(absorb, p.a_max)

        surfaced = latent / p.surface_delay
        latent -= surfaced
        rework += surfaced
        repaid = p.repay_share * rework
        rework -= repaid

        shipped = max(0.0, capacity - p.rework_cost * repaid)   # what deployment metrics see
        absorbed = min(shipped, absorb)
        latent += shipped - absorbed

        rows.append({
            "t": t,
            "capacity": round(capacity, 2),
            "absorb": round(absorb, 2),
            "shipped": round(shipped, 2),
            "ar": round(absorbed / shipped, 4) if shipped else 1.0,
            "debt": round(latent + rework, 2),
        })
    return rows


def main(argv: List[str]) -> int:
    out = argv[1] if len(argv) > 1 else "paper/model.dat"
    without = simulate(Params())
    with_cats = simulate(Params(a_growth=6.0))
    with open(out, "w") as fh:
        fh.write("t capacity absorbNo shippedNo arNo debtNo absorbCats shippedCats arCats debtCats\n")
        for a, b in zip(without, with_cats):
            fh.write(f"{a['t']} {a['capacity']} {a['absorb']} {a['shipped']} {a['ar']} {a['debt']} "
                     f"{b['absorb']} {b['shipped']} {b['ar']} {b['debt']}\n")
    print(f"wrote {out}")
    for label, rows in (("without CATS", without), ("with CATS", with_cats)):
        peak = max(rows[:12], key=lambda r: r["shipped"])
        final = rows[-1]
        print(f"{label:13s} early peak {peak['shipped']:.0f} (month {peak['t']}); "
              f"final shipped {final['shipped']:.0f}, AR {final['ar']:.2f}, debt {final['debt']:.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
