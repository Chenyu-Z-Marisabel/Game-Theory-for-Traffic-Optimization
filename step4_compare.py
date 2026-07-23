"""
STEP 4 — Compare routing strategies across demand levels.

Goal: produce the plots and table that go in the paper.

Outputs:
  - comparison.png   total travel time vs demand for selfish/tolled/optimal
  - poa_curve.png    Price of Anarchy vs demand
"""

import matplotlib.pyplot as plt

from step2_baseline import run_selfish, run_system_optimal, reset_flow
from step3_tolls import build_asymmetric_diamond, travel_time_with_toll


# ---------------------------------------------------------------------------
# Sweep helper: run all three algorithms at each demand level.
# ---------------------------------------------------------------------------
def sweep(demands):
    """For each demand level, build a fresh network and run all three
    algorithms. Returns three parallel lists of totals."""
    selfish = []
    tolled = []
    optimal = []

    graph = build_asymmetric_diamond()
    for i in demands:
        selfish.append(run_selfish(graph, i))
        reset_flow(graph)
        tolled.append(run_selfish(graph, i, lam=travel_time_with_toll))
        reset_flow(graph)
        optimal.append(run_system_optimal(graph, i)[0])
        reset_flow(graph)

    return selfish, tolled, optimal


# ---------------------------------------------------------------------------
# Main: sweep, print, plot.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demands = list(range(50, 601, 10))
    # demands = [i for i in range(1, 11)]
    selfish, tolled, optimal = sweep(demands)

    # TODO: print a table with columns: N, Selfish, Tolled, Optimal, PoA_self, PoA_toll
    pass  # TODO

    # --- comparison.png ---
    plt.figure(figsize=(8, 4.5))
    plt.plot(demands, selfish, marker="o", color="#F87171", label="Selfish")
    plt.plot(demands, tolled,  marker="s", color="#FBBF24", label="With tolls")
    plt.plot(demands, optimal, marker="^", color="#34D399", label="System optimal")
    plt.xlabel("Number of drivers")
    plt.ylabel("Total system travel time")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.title("Routing strategies — Small asymmetric diamond")
    plt.tight_layout()
    plt.savefig("comparison.png", dpi=120)
    plt.close()

    # --- poa_curve.png ---
    # TODO: compute poa_selfish = [s/o for s, o in zip(selfish, optimal)]
    poa_selfish = [s/o for s, o in zip(selfish, optimal)]  # TODO
    # TODO: compute poa_tolled  = [t/o for t, o in zip(tolled, optimal)]
    poa_tolled = [t/o for t, o in zip(tolled, optimal)]   # TODO

    plt.figure(figsize=(8, 4.5))
    plt.plot(demands, poa_selfish, marker="o", color="#F87171", label="Selfish PoA")
    # plt.plot(demands, poa_tolled,  marker="s", color="#FBBF24", label="Tolled PoA")
    plt.axhline(1.0, linestyle="--", color="gray", label="Optimal (PoA=1)")
    plt.xlabel("Number of drivers")
    plt.ylabel("Price of Anarchy")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.title("Price of Anarchy vs demand")
    plt.tight_layout()
    plt.savefig("poa_curve.png", dpi=120)
    plt.close()

    print("Saved comparison.png and poa_curve.png")
