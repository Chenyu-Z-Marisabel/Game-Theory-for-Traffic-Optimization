import pandas as pd
import matplotlib.pyplot as plt
if __name__ == "__main__":
    csv = pd.read_csv("data_sparse.csv")
    xaxis = [i / 1 for i in range(41)]
    data = [[0] * 41 for i in range(11)]

    for x in csv.itertuples(index=False):
        data[x[0]][x[1]] = x[3]


    plt.figure(figsize=(8, 4.5))
    for i, row in enumerate(data):
        color = "#0000" + (hex(i + 5)[-1] * 2)
        plt.plot(xaxis, row, marker=".", color=color, label=f"p = {i / 10:.1f}")
    # temp = list()
    # for i in range(11):
        # temp.append(data[i][10])
    # plt.plot(xaxis, temp, marker="o", color="#0000ff")

    plt.axhline(1.0, linestyle="--", color="gray", label="Optimal (PoA=1)")
    # plt.xlabel("Compliance rate p")
    plt.xlabel("Toll multiplier alpha")
    plt.ylabel("Price of Anarchy")
    # plt.title(f"Partial compliance on asymmetric diamond (N={n}, {t} trials)")
    plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=8, ncol=4)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("compliance.png", dpi=120, bbox_inches="tight")
    plt.show()
    plt.close()
    print(data)