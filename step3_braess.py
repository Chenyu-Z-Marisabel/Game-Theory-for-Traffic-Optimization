"""
STEP 3 (bonus) — Braess's Paradox.

Adding a road to a network can make EVERY driver slower under selfish routing.
Discovered by Dietrich Braess in 1968.

Network:
       B ----> D              Without shortcut:
      / \                     - Drivers split between S-A-T and S-B-T
     A   ?                    With shortcut A->B:
      \ /                     - Drivers pile onto S-A-B-T because it looks free,
       C ----> D                congesting both bottleneck legs
"""

import networkx as nx
import matplotlib.pyplot as plt

from step1_network import travel_time, update_weights
from step2_baseline import run_selfish


# ---------------------------------------------------------------------------
# Build the Braess network. The `with_shortcut` flag toggles the A->B edge.
# ---------------------------------------------------------------------------
def build_braess(with_shortcut: bool):
    graph = nx.DiGraph()
    # TODO: add 4 edges with these parameters:
    #   S -> A : t0 = 10,   cap = 2000           (bottleneck — congests at full load)
    #   B -> T : t0 = 10,   cap = 2000           (bottleneck — congests at full load)
    #   A -> T : t0 = 50,   cap = 1_000_000      (long highway, ~constant)
    #   S -> B : t0 = 50,   cap = 1_000_000      (long highway, ~constant)

    graph.add_edge("A", "B", t0=10, cap=20, flow=0)
    graph.add_edge("B", "D", t0=50, cap=1e4, flow=0)

    graph.add_edge("A", "C", t0=50, cap=1e4, flow=0)
    graph.add_edge("C", "D", t0=10, cap=20, flow=0)

    # TODO: if with_shortcut is True, also add:
    #   A -> B : t0 = 0.01, cap = 1_000_000     (the "free" shortcut)
    if bool(with_shortcut):
        graph.add_edge("B", "C", t0=1e-2, cap=1e4, flow=0)

    return graph


# ---------------------------------------------------------------------------
# Main: run selfish routing both with and without the shortcut.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    n = 40  # number of drivers

    # TODO: build the network WITHOUT the shortcut, run selfish, store total
    g_no = build_braess(0)     # TODO
    no_total = run_selfish(g_no, n)    # TODO

    print(f"Without shortcut:  total = {no_total:.2f}  (avg = {no_total / n:.2f})")

    # TODO: build the network WITH the shortcut, run selfish, store total
    g_yes = build_braess(1)    # TODO
    yes_total = run_selfish(g_yes, n)   # TODO

    print(f"With shortcut:     total = {yes_total:.2f}  (avg = {yes_total / n:.2f})")

    # The famous result: with_shortcut > without_shortcut.
    pct = 100 * (yes_total - no_total) / no_total
    print(f"\nAdding the A->B shortcut changed total travel time by {pct:+.2f}%")
    if yes_total > no_total:
        print("=> Braess's Paradox: the extra road made traffic WORSE!")
    else:   
        print("(No paradox observed - try tuning t0 or cap.)")

    # Simple comparison chart.
    plt.bar(["Without shortcut", "With shortcut"], [no_total, yes_total],
            color=["#34D399", "#F87171"])
    plt.ylabel("Total system travel time")
    plt.title(f"Braess's Paradox (N={n} drivers)")
    plt.savefig("step3_braess.png", dpi=120)
    plt.show()
