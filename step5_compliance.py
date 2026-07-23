"""
STEP 5 — Partial compliance: what if only some drivers obey the toll?

The policy question: real cities can't force 100% compliance. How much do
we actually need to recover most of the benefit?

For each compliance rate p in {0.0, 0.1, ..., 1.0}, each driver independently:
  - with probability p:    routes on travel_time + toll  (the "complier")
  - with probability 1-p:  routes on plain travel_time   (the "selfish" driver)

Sweep p, average over multiple trials, plot PoA(p).
"""

import random
import statistics

import networkx as nx
import matplotlib.pyplot as plt

from step1_network import travel_time, update_weights
from step2_baseline import run_system_optimal, run_selfish
from step3_tolls import travel_time_with_toll, build_asymmetric_diamond, travel_time_alpha


# ---------------------------------------------------------------------------
# Main: sweep p, average, plot.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    random.seed(44)   # reproducible results
    n = 400
    t = 1       # average over this many trials per p

    # Compute the optimal benchmark once.
    g = build_asymmetric_diamond()
    optimal_total = run_system_optimal(g, n)[0]

    temp = run_system_optimal(g, n);
    print(temp)

    print(f"Optimal total (benchmark): {optimal_total:.2f}\n")
    print(f"{'p':>5} {'avg_total':>12} {'PoA':>8}")

    # compliance rates
    ps = [1]   # 0.0, 0.1, ..., 1.0

    f = open("test.txt", "w")
    f.write(f"16 {len(ps)}\n")

    temp = list()

    alphas = [1];

    # toll multipliers
    for i in alphas:
        alpha = list()
        for j in ps:
            tot = 0
            for k in range(t):
                tot += run_selfish(g, n, lam = travel_time_alpha(i, j))
                    
            alpha.append(tot / t / optimal_total)
            f.write(f'{alpha[-1]}\n')
            print(f"i = {i}, j = {j}, avg = {tot / t}")
        # plt.plot(ps, alpha, color='#' + hex(i)[-1] * 4 + "00")
        print("done with i = " + str(i))
        temp.append(alpha[-1])

    f.close()

    # Plot.
    # plt.plot(ps, poa_curve, marker="o", color="#A78BFA")
    plt.figure(figsize=(8, 4.5))
    plt.plot(alphas, temp, marker="o", color="#F6A351")
    plt.axhline(1.0, linestyle="--", color="gray", label="Optimal (PoA=1)")
    plt.xlabel("Compliance rate p")
    plt.ylabel("Price of Anarchy")
    plt.title(f"Partial compliance on asymmetric diamond (N={n}, {t} trials)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("compliance.png", dpi=120)
    plt.close()
    print("\nSaved compliance.png")

    # TODO (analysis): find the compliance rate p* that captures 80% of the
    # toll benefit. Hint: target_poa = selfish_poa - 0.8 * (selfish_poa - 1.0).
    # Loop through ps and poa_curve and print the first p where poa <= target.
    pass  # TODO
