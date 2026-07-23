"""
STEP 3 — Game-theoretic routing with marginal-cost tolls.

THE MAIN CONTRIBUTION OF THE PROJECT.

The toll on a road equals the slowdown one extra car imposes on others.
For BPR  t(x) = t0 * (1 + 0.15 * (x/cap)^4):

    t'(x)   = t0 * 0.6 * x^3 / cap^4
    toll(x) = x * t'(x) = t0 * 0.6 * x^4 / cap^4

A driver minimizes (travel_time + toll) instead of just travel_time. With
this tweak, selfish drivers happen to produce the system optimum.
"""

import networkx as nx
import matplotlib.pyplot as plt
import random

from step1_network import travel_time, update_weights
from step2_baseline import run_selfish, run_system_optimal, reset_flow
from step3_braess import build_braess


# ---------------------------------------------------------------------------
# (1) The tolled cost function.
# ---------------------------------------------------------------------------
def travel_time_with_toll(u, v, d, id):
    """Returns travel_time(t0, flow, cap) + toll, where
        toll = t0 * 0.6 * flow^4 / cap^4
    The toll is the marginal externality of adding one more car."""
    base = travel_time(u, v, d, id)  # TODO

    toll = d['t0'] * 0.6 * (d['flow'] / d['cap']) ** 4  # TODO

    return base + toll


def travel_time_alpha(a, p):
    def alpha_wrapper(u, v, d, id):
        copy = random.Random()
        copy.seed(id ^ random.randint(0, 1_000_000_000))
        if (copy.random() < p):
            return travel_time(u, v, d, id) + a * d['t0'] * 0.6 * (d['flow'] / d['cap']) ** 4
        else:
            return travel_time(u, v, d, id)
    return alpha_wrapper

# ---------------------------------------------------------------------------
# (4) An asymmetric network where PoA > 1 will actually show up.
# ---------------------------------------------------------------------------
def build_asymmetric_diamond():
    """Pigou-style asymmetric diamond. Path A-B-D is narrow but attractive at
    low load; path A-C-D is a constant slow highway. Selfish drivers all pile
    onto A-B-D; the optimum spreads some onto A-C-D."""
    graph = nx.DiGraph()
    # TODO: add 4 edges with these parameters:
    #   A -> B: t0=1,   cap=200          (narrow congesting)
    #   B -> D: t0=1,   cap=200
    #   A -> C: t0=2.5, cap=1_000_000    (constant slow highway)
    #   C -> D: t0=2.5, cap=1_000_000
    graph.add_edge('A', 'B', t0 = 1, cap = 200)
    graph.add_edge('B', 'D', t0 = 1, cap = 200)

    graph.add_edge('A', 'C', t0 = 2.5, cap = 1e9)
    graph.add_edge('C', 'D', t0 = 2.5, cap = 1e9)
    return graph


# ---------------------------------------------------------------------------
# (5) Main: compare selfish vs tolled vs optimal at several demand levels.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for i in [100, 200, 400, 800, 1600]:
        g = build_asymmetric_diamond()

        selfish = run_selfish(g, i)
        reset_flow(g)
        tolled = run_selfish(g, i, lam=travel_time_with_toll)
        reset_flow(g)
        opt = run_system_optimal(g, i)
        print(f'{selfish} {tolled} {opt} {selfish / opt[0]} {tolled / opt[0]}')
        # Expected at N=400: selfish PoA ~ 1.40, tolled PoA ~ 1.00
