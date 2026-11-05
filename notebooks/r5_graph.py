import matplotlib.pyplot as plt

boxes = [
    (2, 5, "Previous-year GPA\nand term 1 result"),
    (7, 5, "Referral or request\nfor tutoring"),
    (7, 3, "Recorded session\nattendance"),
    (2, 1, "Failing grade\n(below 60)"),
]

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 9)
ax.set_ylim(0, 6)
ax.axis("off")

for x, y, text in boxes:
    ax.text(x, y, text, ha="center", va="center", fontsize=11,
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#d9ead3", edgecolor="black"))

def arrow(start, end, dashed=False):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="->", lw=1.5, shrinkA=0, shrinkB=0,
                                linestyle="--" if dashed else "-"))

arrow((3.0, 5), (6.0, 5))
arrow((7, 4.55), (7, 3.45))
arrow((2, 4.55), (2, 1.45), dashed=True)
arrow((6.05, 2.75), (2.85, 1.15), dashed=True)

ax.text(3.6, 5.15, "Input #5 (R2 graph)", fontsize=10, weight="bold")
ax.text(7.15, 3.95, "Inputs #2, #3", fontsize=10, weight="bold")
ax.text(2.15, 3.0, "H1: similar start,\nno higher failure", fontsize=10, weight="bold")
ax.text(4.8, 1.25, "H2: more attendance,\nless failure", fontsize=10, weight="bold")

ax.set_title("R5 hypotheses, using labels from the R2 graph")
plt.savefig("figures/R5_hypotheses_graph.png", dpi=150, bbox_inches="tight")
print("saved")
