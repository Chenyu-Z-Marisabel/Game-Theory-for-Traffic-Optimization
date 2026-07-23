"""
STEP 2 — Baseline routing: selfish vs system-optimal.

Goal: write two routing algorithms. The gap between them is the Price of Anarchy.

- run_selfish:        each driver picks the currently shortest path for themselves
                      (converges to Wardrop / Nash equilibrium)
- run_system_optimal: try every possible split of drivers between paths and pick
                      the split with the smallest TOTAL travel time
"""

import networkx as nx
import matplotlib.pyplot as plt
import itertools

# Reuse the graph and helpers from Phase 1.
from step1_network import g, travel_time, update_weights, wrap

def take_path(graph, path):
    for u, v in itertools.pairwise(path):
        graph.edges[u, v]['flow'] += 1
        # print('updated flow for edge ' + u + ' ' + v)

def reset_flow(graph):
    for u, v, d in graph.edges(data = True):
        d['flow'] = 0

# ---------------------------------------------------------------------------
# (1) Selfish routing: each driver greedily picks the fastest path.
# ---------------------------------------------------------------------------
def run_selfish(graph, n_drivers, source="A", target="D", lam=travel_time):
    """Send n_drivers from source to target one at a time. Each driver picks
    the current shortest path. Returns total system travel time."""

    reset_flow(graph)
    for i in range(n_drivers):
        length, path = nx.bidirectional_dijkstra(graph, source, target, weight = wrap(i, lam))
        take_path(graph, path)
    update_weights(graph)

    return sum(d['flow'] * d['weight'] for u, v, d in graph.edges(data = True))


# ---------------------------------------------------------------------------
# (2) System-optimal routing: try every split, return the best.
# ---------------------------------------------------------------------------
def run_system_optimal(graph, n_drivers, source="A", target="D"):
    """Enumerate every split of n_drivers among the available paths and
    return the (total, split, paths) that minimizes total system travel time."""

    # TODO: list every simple path from source to target.
    # Hint: paths = list(nx.all_simple_paths(G, source, target))
    paths = list(nx.all_simple_paths(graph, source, target))
    print("paths: " + str(paths))

    best = (float("inf"), 0)

    for i in range(n_drivers + 1):
        loops = 0
        reset_flow(graph)
        for j in range(i):
            loops += 1
            take_path(graph, paths[0])
        for j in range(i, n_drivers):
            loops += 1
            take_path(graph, paths[1])

        update_weights(graph)
        total = sum(d["flow"] * d["weight"] for u, v, d in graph.edges(data=True))
        best = min(best, (total, i))
        if (loops != n_drivers):
            print(f'error {loops} {n_drivers}')
            assert False

    return best


# ---------------------------------------------------------------------------
# (3) Main: sweep demand and plot.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demands = [i * 10 for i in range(1, 41)]
    selfish_totals = []
    optimal_totals = []

    for i in demands:
        selfish = run_selfish(g, i)
        opt = run_system_optimal(g, i)
        print(f'{i} {selfish} {opt} {selfish / opt[0]}')
        selfish_totals.append(selfish)
        optimal_totals.append(opt[0])

    # Plot the demand sweep.
    plt.plot(demands, selfish_totals, marker="o", label="Selfish")
    plt.plot(demands, optimal_totals, marker="s", label="System optimal")
    plt.xlabel("Number of drivers")
    plt.ylabel("Total system travel time")
    plt.title("Demand sweep — asymmetric diamond")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig("step2_baseline.png", dpi=120)
    plt.show()
