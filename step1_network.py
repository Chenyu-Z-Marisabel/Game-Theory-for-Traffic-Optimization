"""
STEP 1 — Build the traffic-network simulation.

Goal: turn a city into a graph and write the formula that says how long
each road takes given how many cars are on it.

Fill in every TODO below. Lines that already have code are scaffolding —
leave them alone unless a TODO says otherwise.
"""

# Imports: NetworkX gives us the graph; matplotlib draws it.
import networkx as nx
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# (1) Build the network: 4 intersections (A, B, C, D) connected as a diamond.
# ---------------------------------------------------------------------------
# Create a directed graph. (Roads have direction.)
g = nx.DiGraph()

# TODO: add 4 edges to form a diamond:
#       A -> B,  A -> C,  B -> D,  C -> D
# Each edge needs THREE attributes:
#   t0   = free-flow travel time when the road is empty
#   cap  = capacity (how many cars the road handles comfortably)
#   flow = current cars on the road (start at 0)
#
# Use t0 = 10 for A->B and C->D (the "short" roads),
#     t0 = 15 for A->C and B->D (the "long" roads),
#     cap = 100 for all four.
#
# Example syntax:  g.add_edge("A", "B", t0=10, cap=100, flow=0)

# g.add_edge("A", "B", t0=10, cap=100, flow=0)
# g.add_edge("A", "C", t0=10, cap=100, flow=0)
# g.add_edge("B", "D", t0=10, cap=100, flow=0)
# g.add_edge("C", "D", t0=10, cap=100, flow=0)


# g.add_edge('A', 'B', t0 = 1, cap = 200)
# g.add_edge('B', 'D', t0 = 1, cap = 200)
# g.add_edge('A', 'C', t0 = 2.5, cap = 1e9)
# g.add_edge('C', 'D', t0 = 2.5, cap = 1e9)

g.add_edge("A", "B", t0=10, cap=20, flow=0) 
g.add_edge("B", "D", t0=50, cap=1e4, flow=0)
g.add_edge("A", "C", t0=50, cap=1e4, flow=0)
g.add_edge("C", "D", t0=10, cap=20, flow=0)
g.add_edge("B", "C", t0=1e-2, cap=1e4, flow=0)

# ---------------------------------------------------------------------------
# (2) The BPR travel-time formula.
# ---------------------------------------------------------------------------
# Bureau of Public Roads, 1964. The standard congestion model:
#
#       travel_time = t0 * (1 + 0.15 * (flow / cap) ^ 4)
#
# At flow = 0   -> travel_time = t0       (empty road, free flow)
# At flow = cap -> travel_time = 1.15*t0  (15% slower at capacity)
# At flow >> cap -> the ^4 makes it explode
def travel_time(u, v, d, id):
    # TODO: return the BPR formula above.
    return d['t0'] * (1 + 0.15 * (d['flow'] / d['cap']) ** 4)

def wrap(id, lam):
    return lambda u, v, d: lam(u, v, d, id)



# ---------------------------------------------------------------------------
# (3) Update edge weights from the current flows.
# ---------------------------------------------------------------------------
# NetworkX uses an edge attribute called "weight" when computing shortest paths.
# This helper recomputes every edge's "weight" using the BPR formula.
def update_weights(graph, lam = travel_time):
    # TODO: loop over g.edges(data=True). For each edge, set
    #       d["weight"] = travel_time(d["t0"], d["flow"], d["cap"])
    for u, v, d in graph.edges(data = True):
        d['weight'] = travel_time(u, v, d, -1);

def get_label(d):
    return f"t0={d['t0']}, cap={d['cap']}"


# ---------------------------------------------------------------------------
# (4) Print and draw the network.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # TODO: print one line per edge showing u -> v, t0, cap, and the current
    # weight. Example:  "  A -> B: t0=10, cap=100, weight=10.00"
    for u, v, d in g.edges(data=True):
        pass  # TODO

    # Fixed positions so the diagram looks the same every run.
    pos = {"A": (0, 1), "B": (1, 2), "C": (1, 0), "D": (2, 1)}

    # TODO: build a dict of edge labels of the form
    #       {(u, v): f"t0={d['t0']}, cap={d['cap']}" for u, v, d in g.edges(data=True)}
    edge_labels = {(u, v): get_label(d) for u, v, d in g.edges(data = True)}  # TODO

    # Draw the graph.
    nx.draw(g, pos, with_labels=True, node_color="lightblue",
            node_size=800, arrows=True, arrowsize=20)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=9)
    plt.title("Step 1: Traffic network (A -> D)")
    plt.savefig("step1_network.png", dpi=120)
    plt.show()
