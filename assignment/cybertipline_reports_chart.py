"""Generate a grouped bar chart for CyberTipline report counts."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


YEARS = np.array(["CY 2021", "CY 2022", "CY 2023"])
TOTAL_REPORTS = np.array([29_397_681, 32_059_029, 36_210_368])
PUBLIC_REPORTS = np.array([240_598, 256_504, 265_542])
ESP_REPORTS = np.array([29_157_083, 31_802_525, 35_944_826])

OUTPUT_PATH = Path(__file__).with_name("cybertipline_reports.png")


def main() -> None:
    bar_width = 0.25
    x = np.arange(len(YEARS))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - bar_width, TOTAL_REPORTS, width=bar_width, label="Total Reports", color="#0f4c5c")
    ax.bar(x, PUBLIC_REPORTS, width=bar_width, label="Public Reports", color="#8ecae6")
    ax.bar(x + bar_width, ESP_REPORTS, width=bar_width, label="ESP Reports", color="#219ebc")

    ax.set_title("CyberTipline Reports Submitted by Members of the Public and ESPs")
    ax.set_ylabel("Number of reports")
    ax.set_xticks(x)
    ax.set_xticklabels(YEARS)
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.ticklabel_format(style="plain", axis="y")
    ax.legend()
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

    # Annotate each bar with its value for quicker reading.
    for bars in ax.containers:
        ax.bar_label(bars, label_type="edge", fontsize=8, padding=3, fmt="{:,.0f}")

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=300)
    print(f"Chart saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
