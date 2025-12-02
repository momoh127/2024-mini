import matplotlib.pyplot as plt
import numpy as np

years = ["CY 2021", "CY 2022", "CY 2023"]
total_reports = [29397681, 32059029, 36210368]
public_reports = [240598, 256504, 265542]
esp_reports = [29157083, 31802525, 35944826]

x = np.arange(len(years))
width = 0.25

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(x - width, total_reports, width, label="Total", color="#333f50")
ax.bar(x, public_reports, width, label="Public", color="#b94141")
ax.bar(x + width, esp_reports, width, label="ESP", color="#0a77d5")

ax.set_ylabel("Reports")
ax.set_title("CyberTipline Reports Submitted (CY 2021-2023)")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.3)

fig.tight_layout()
fig.savefig("cybertipline_reports.png", dpi=200)
plt.close(fig)
