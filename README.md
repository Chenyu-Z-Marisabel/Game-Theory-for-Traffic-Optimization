# Game Theory for Traffic Optimization

**A computational study of selfish routing, congestion tolls, and partial compliance.**

## What this project is about

Traffic congestion is not just an engineering problem - it's a **multi-player game**. Every driver picks a route to
minimize their own travel time, but every driver added to a road slows down everyone else on it. When drivers act
selfishly, the network can settle into a state that is *collectively* worse than what a coordinated planner could
achieve, even though every individual is doing the best they can given everyone else's choices.

This project builds a small but complete simulation of that game - a 4-node road network, a congestion-aware
travel-time model, and two competing routing regimes (selfish vs. system-optimal) - and uses it to answer three
questions:

1. **How much worse is selfish routing than optimal routing?** (The Price of Anarchy.)
2. **Can a toll fix it?** (Marginal-cost / Pigouvian tolling.)
3. **What happens when the toll doesn't have full compliance** - and does the toll itself need to be resized to
   compensate?

The third question is this project's original contribution: real cities can't force 100% of drivers to obey a
routing incentive, so we study how the *optimal toll size* should change as compliance drops, and find that it does
so in a non-trivial way - including a case where the toll can be **too large**, not just too small.

---

## Core concepts

| Concept                        | Meaning in this project                                                                                                                    |
|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| **Player**                     | A driver choosing a route from A to D                                                                                                      |
| **Nash / Wardrop equilibrium** | Selfish outcome: no driver can save time by switching routes alone                                                                         |
| **Social optimum**             | The route split a central planner would choose to minimize *total* travel time                                                             |
| **Price of Anarchy (PoA)**     | `selfish_total_time / optimal_total_time`. PoA = 1 means selfish routing is already optimal; PoA > 1 quantifies the waste from selfishness |
| **Externality**                | The slowdown one driver imposes on everyone else sharing their road - selfish drivers ignore it, which is *why* PoA > 1                    |
| **Marginal-cost toll**         | A per-road charge equal to the externality; makes selfish optimization coincide with social optimization                                   |
| **Compliance rate (p)**        | Fraction of drivers who actually route on `travel_time + toll` instead of ignoring the toll entirely                                       |
| **Toll multiplier (alpha)**    | A scaling factor on the toll (alpha = 1 is the textbook marginal-cost toll; this project asks what alpha should be when p < 1)             |

---

## Network model

A 4-node directed graph (`A -> B -> D` and `A -> C -> D`), with travel time on each edge given by the standard
Bureau of Public Roads (1964) formula:

```
t(flow) = t0 * (1 + 0.15 * (flow / cap)^4)
```

Two network configurations are used throughout:

- **Symmetric diamond** (`step1_network.py`) - both paths identical. Selfish and optimal routing coincide here
  (PoA = 1.0 exactly at every demand level). This is a real, useful finding: it shows PoA depends on network
  *asymmetry*, not merely on whether drivers are selfish (a small-scale echo of Roughgarden's 2003 topology-
  independence result).
- **Asymmetric diamond** (`build_asymmetric_diamond()` in `step3_tolls.py`) - a narrow, congesting road (`A->B->D`,
  `t0=1, cap=200`) competing with a constant-time highway (`A->C->D`, `t0=2.5, cap~infinity`). This is where a
  genuine Price-of-Anarchy gap appears, and it's the network used for every toll and compliance experiment below.

---

## Results

### 1. Selfish routing wastes real travel time

On the asymmetric diamond at N = 400 drivers:

| Regime         | Total travel time | PoA        |
|----------------|-------------------|------------|
| Selfish        | ~2004             | **1.4023** |
| System-optimal | ~1429             | 1.0000     |

Selfish drivers overload the fast, narrow road because each one ignores the congestion they add to it. ~40% of
total travel time is wasted relative to what a coordinated assignment could achieve.

### 2. A correctly-sized marginal-cost toll closes the gap completely

`step3_tolls.py` adds a per-road toll equal to the externality (`toll(x) = t0 * 0.6 * x^4/cap^4`, the derivative-
based marginal cost under BPR). With full compliance and the standard toll multiplier (alpha = 1), the tolled
equilibrium matches the system optimum: **PoA -> 1.0000**. Drivers remain entirely selfish - the toll simply makes
their private incentive align with the social one.

### 3. Braess's Paradox: adding a road can make everyone slower

`step3_braess.py` reproduces the classic counterexample - adding a free shortcut edge to the network *increases*
total selfish travel time, because it tempts every driver onto a path that shares both bottlenecks at once. This
demonstrates that "more capacity always helps" is false once routing is selfish rather than coordinated.

### 4. Partial compliance: the toll needs to be resized, not just applied

`step5_compliance.py` models each driver as independently compliant with probability p (routes on
`travel_time + alpha*toll`) or non-compliant (routes on raw `travel_time`, ignoring the toll completely). Sweeping
both p (0.0-1.0) and the toll multiplier alpha (0.0-4.0 and 0.0-40.0 respectively, see `data_dense.csv` / `data_sparse.csv`) produces the
project's central extension result:

| Compliance p | Optimal multiplier alpha*                                | Minimum PoA achieved |
|--------------|----------------------------------------------------------|----------------------|
| 0.0 - 0.1    | none (toll has no effect at all)                         | 1.4023               |
| 0.2          | 3.5                                                      | 1.386                |
| 0.3 - 0.7    | ~3.9-4.0 (still falling at the edge of the tested range) | 1.00 - 1.26          |
| 0.8          | 3.05                                                     | 1.0000               |
| 0.9          | 1.75                                                     | 1.0000               |
| 1.0          | 1.00 (textbook Pigou value)                              | 1.0000               |

Two findings stand out:

- **As compliance falls, the toll has to be charged more aggressively.** Only the compliant fraction of drivers
  responds to the price signal, so they must individually overcorrect to pull the *overall* traffic split back
  toward the optimum. At full compliance the textbook toll (alpha = 1) is exactly right; below ~80% compliance,
  the required multiplier climbs sharply.
- **The toll can be overcharged.** At high compliance (p >= 0.8), PoA vs. alpha is a convex bowl, not a
  monotonically decreasing curve - past the optimal alpha, PoA rises again because *too many* compliant drivers
  are pushed onto the slow road, overshooting the optimal split. This means "charge a bigger toll" is not a
  universally safe policy; there is a correct alpha for a given compliance level, and overshooting it costs
  efficiency in the opposite direction.
- **Limitation:** for p = 0.3-0.7, the search never found an interior minimum - PoA was still decreasing at
  alpha = 4.0, the edge of the tested range. The true optimal multiplier for that band is unknown and likely
  higher than 4; extending the sweep further is natural follow-up work.

### 5. Real-world grounding

The mechanism modeled here (marginal-cost congestion tolls) is the same one used by London's Congestion Charge
(2003), Singapore's Electronic Road Pricing (1998), Stockholm's Congestion Tax (2007), and New York City's
Congestion Relief Zone (2025). NYC's first year of data shows an 11% drop in vehicles entering the tolled zone and
a 15% increase in average speed - a real-world instance of the same selfish-to-optimal correction this project
demonstrates in miniature. Compliance/adoption thresholds also show up in independent research on navigation-app
routing (Cornacchia et al., 2024), where optimal adoption for one eco-routing service in Rome was found to be ~70%


---

## Project files

| File                                          | Role                                                                                                                                      |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| `step1_network.py`                            | Builds the road network graph and the BPR travel-time formula                                                                             |
| `step2_baseline.py`                           | `run_selfish` (Wardrop equilibrium) and `run_system_optimal` (social planner) - the two routing regimes whose gap is the Price of Anarchy |
| `step3_tolls.py`                              | Marginal-cost toll formula, tolled routing, and the asymmetric-diamond network used for every toll/compliance experiment                  |
| `step3_braess.py`                             | Braess's Paradox demonstration network                                                                                                    |
| `step4_compare.py`                            | Demand sweeps and comparison charts (selfish vs. tolled vs. optimal)                                                                      |
| `step5_compliance.py`                         | Partial-compliance simulation: mixes compliant and non-compliant drivers, sweeps compliance rate p                                        |
| `data/data_sparse.csv`, `data/data_dense.csv` | Precomputed PoA(p, alpha) grids over p in [0, 1], alpha in [0, 4] - the data behind the compliance/toll-multiplier charts                 |
| `step5_dp.py`                                 | Reads `data_sparse.csv` and plots PoA vs. toll multiplier alpha as a fan-out of curves, one per compliance rate p                          |
| `graphs/comparison.png`                       | Total travel time vs. number of drivers on the (small) asymmetric diamond - selfish vs. tolled vs. system-optimal                          |
| `graphs/compliance.png`                       | **Mislabeled** - despite the filename, this is the alpha fan-out chart (x-axis = toll multiplier, one curve per p), not PoA vs. compliance rate. `step5_compliance.py` and `step5_dp.py` both write to `compliance.png`, so whichever ran last overwrote the other's output |
| `graphs/poa_curve.png`                        | Selfish Price of Anarchy vs. number of drivers, peaking near 1.47 around N=360 before declining; only the selfish curve is present, the tolled-PoA curve from `step4_compare.py` is missing from this particular run |
| `graphs/step1_network.png`                    | Diagram of the road network - **5 edges**, not 4: A to D via B or C, plus a B-to-C shortcut edge (t0=0.01), so this is actually the Braess-shortcut network, not the plain diamond |
| `graphs/step2_baseline.png`                   | Demand sweep on the true symmetric diamond - selfish and optimal curves overlap exactly (PoA = 1.0), as expected |
| `graphs/step2_baseline_alt.png`               | Labeled "symmetric diamond" but the selfish and optimal curves visibly diverge past N~275 (PoA > 1) - inconsistent with a true symmetric network; source script not found, worth double-checking before citing |
| `graphs/step3_braess.png`                     | Bar chart: total travel time with vs. without the Braess shortcut edge at N=40 drivers - "with shortcut" is higher, confirming the paradox |



---

## Reproducing the results

```powershell
python step1_network.py       # network diagram
python step2_baseline.py      # selfish vs optimal, symmetric diamond (PoA = 1.0)
python step3_tolls.py         # asymmetric diamond: selfish PoA ~ 1.40, tolled PoA ~ 1.00
python step3_braess.py        # Braess's Paradox
python step4_compare.py       # comparison + PoA-vs-demand charts
python step5_compliance.py    # partial-compliance sweep
python heatmap.py             # PoA(p, alpha) heatmap + alpha*(p) curve
python graph_alpha.py         # per-p fan-out curves
```

---

## Flow Demo
[Demo Video](https://drive.google.com/file/d/1-Sl0DEr6oh_rp5XQRFkjlyeWr5jL2vK5/view).

## References

1. Tim Roughgarden, *The Price of Anarchy Is Independent of the Network Topology*, JCSS 2003.
2. Tim Roughgarden, *Routing Games*, in *Algorithmic Game Theory*, Cambridge UP, 2007.
3. R. Cominetti et al., *The Price of Anarchy in Routing Games as a Function of the Demand*, Math. Programming, 2024.
4. J.G. Wardrop, *Some Theoretical Aspects of Road Traffic Research*, 1952.
5. A.C. Pigou, *The Economics of Welfare*, 1920.
6. D. Braess, *Uber ein Paradoxon aus der Verkehrsplanung*, 1968.
7. Bureau of Public Roads, *Traffic Assignment Manual*, 1964 (BPR travel-time function).
8. G. Cornacchia, M. Nanni, D. Pedreschi, L. Pappalardo, *Navigation services amplify concentration of traffic and
   emissions in our cities*, arXiv:2407.20004, 2024.
9. H. Bang, J.-H. Cho, C. Wu, A.A. Malikopoulos, *Route Recommendations for Traffic Management Under Learned
   Partial Driver Compliance*, arXiv:2504.02993, 2025.
