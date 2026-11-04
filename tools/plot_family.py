"""Plot GFL family spread rates against published comparators (dark theme, English labels)."""
import json
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

res = json.load(open(sys.argv[1]))["runs"]
out = sys.argv[2]
o2 = {"B1": 22.2, "B3": 22.2, "B6": 21.0, "B9": 21.0, "B15": 21.0, "B16": 17.3, "B19": 17.3, "B20": 17.4}
col = {"GMT50": "#e0af68", "GMT188": "#7aa2f7", "GMT183": "#9ece6a"}
fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
fig.patch.set_facecolor("#0d1117"); ax.set_facecolor("#0d1117")
for i, (t, r) in enumerate(sorted(res.items(), key=lambda kv: (o2[kv[0]], kv[0]))):
    c = col[r["session"]]
    if r.get("status") == "measured":
        ax.errorbar(i, r["value_mm_s"], yerr=r["standard_uncertainty_mm_s"], fmt="o", color=c, capsize=4, ms=7)
    else:
        ax.plot(i, 0.2, "x", color="#f7768e", ms=10)
        ax.text(i, 0.35, "abstain", color="#f7768e", ha="center", fontsize=8)
    ax.text(i, -0.35, f"{t}\n{o2[t]}% O₂", color="#c9d1d9", ha="center", fontsize=8)
ax.axhspan(1.9, 2.1, color="#bb9af7", alpha=0.18)
ax.text(len(res) - 0.4, 2.0, "Carmignani 2019: B6 ≈ 2 mm/s", color="#bb9af7", ha="right", va="center", fontsize=8)
ax.axhline(2.2, color="#f7768e", ls="--", lw=1)
ax.text(len(res) - 0.4, 2.27, "NASA TM §2.3: ≈2.2 mm/s max (no run join)", color="#f7768e", ha="right", fontsize=8)
for s, c in col.items():
    ax.plot([], [], "o", color=c, label=f"session {s}")
ax.legend(facecolor="#161b22", edgecolor="#30363d", labelcolor="#c9d1d9", loc="upper left", fontsize=8)
ax.set_xlim(-0.6, len(res) - 0.4); ax.set_ylim(-0.6, max(3.2, ax.get_ylim()[1])); ax.set_xticks([])
ax.set_ylabel("leading-edge spread rate (mm/s)", color="#c9d1d9")
ax.set_title("Gravity Fire Ledger · BASS-II 100-µm PMMA family, measured from original NASA stills", color="white", fontsize=10)
ax.tick_params(colors="#c9d1d9")
for sp in ax.spines.values():
    sp.set_color("#30363d")
plt.tight_layout(); plt.savefig(out, facecolor=fig.get_facecolor())
