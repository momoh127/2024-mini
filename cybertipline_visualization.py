import matplotlib.pyplot as plt
import numpy as np

# Data from the table
years = ['CY 2021', 'CY 2022', 'CY 2023']
total_reports = [29_397_681, 32_059_029, 36_210_368]
public_reports = [240_598, 256_504, 265_542]
esp_reports = [29_157_083, 31_802_525, 35_944_826]

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Color scheme
colors = ['#8B2335', '#87CEEB', '#4169E1']  # Dark red, Sky blue, Royal blue

# Plot 1: Grouped Bar Chart showing all three categories
x = np.arange(len(years))
width = 0.25

bars1 = ax1.bar(x - width, total_reports, width, label='Total Reports', color=colors[0], alpha=0.8)
bars2 = ax1.bar(x, public_reports, width, label='Public Reports', color=colors[1], alpha=0.8)
bars3 = ax1.bar(x + width, esp_reports, width, label='ESP Reports', color=colors[2], alpha=0.8)

ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Reports', fontsize=12, fontweight='bold')
ax1.set_title('CyberTipline Reports by Category (2021-2023)', fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.legend(fontsize=10)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontsize=7, rotation=0)

# Format y-axis with commas
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

# Plot 2: Line Chart showing trends
ax2.plot(years, total_reports, marker='o', linewidth=2.5, markersize=8, 
         label='Total Reports', color=colors[0])
ax2.plot(years, public_reports, marker='s', linewidth=2.5, markersize=8, 
         label='Public Reports', color=colors[1])
ax2.plot(years, esp_reports, marker='^', linewidth=2.5, markersize=8, 
         label='ESP Reports', color=colors[2])

ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Reports', fontsize=12, fontweight='bold')
ax2.set_title('CyberTipline Reports Trends (2021-2023)', fontsize=14, fontweight='bold', pad=20)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, linestyle='--')

# Add value labels on points
for i, year in enumerate(years):
    ax2.text(i, total_reports[i], f'{total_reports[i]:,}', 
            ha='center', va='bottom', fontsize=8)
    ax2.text(i, public_reports[i], f'{public_reports[i]:,}', 
            ha='center', va='bottom', fontsize=8)
    ax2.text(i, esp_reports[i], f'{esp_reports[i]:,}', 
            ha='center', va='bottom', fontsize=8)

# Format y-axis with commas
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

# Adjust layout and save
plt.tight_layout()
plt.savefig('cybertipline_reports_visualization.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'cybertipline_reports_visualization.png'")

# Create a second visualization focusing on Public vs ESP breakdown
fig2, ax3 = plt.subplots(figsize=(12, 7))

x = np.arange(len(years))
width = 0.35

bars_public = ax3.bar(x - width/2, public_reports, width, label='Public Reports', 
                      color=colors[1], alpha=0.9)
bars_esp = ax3.bar(x + width/2, esp_reports, width, label='ESP Reports', 
                   color=colors[2], alpha=0.9)

ax3.set_xlabel('Year', fontsize=13, fontweight='bold')
ax3.set_ylabel('Number of Reports', fontsize=13, fontweight='bold')
ax3.set_title('CyberTipline Reports: Public vs ESP (2021-2023)', 
             fontsize=16, fontweight='bold', pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(years)
ax3.legend(fontsize=11)
ax3.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels
for bar in bars_public:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

for bar in bars_esp:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height):,}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

plt.tight_layout()
plt.savefig('cybertipline_public_vs_esp.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'cybertipline_public_vs_esp.png'")

print("\nSummary Statistics:")
print(f"Total increase from 2021 to 2023: {total_reports[2] - total_reports[0]:,} ({((total_reports[2] - total_reports[0]) / total_reports[0] * 100):.1f}%)")
print(f"Public increase from 2021 to 2023: {public_reports[2] - public_reports[0]:,} ({((public_reports[2] - public_reports[0]) / public_reports[0] * 100):.1f}%)")
print(f"ESP increase from 2021 to 2023: {esp_reports[2] - esp_reports[0]:,} ({((esp_reports[2] - esp_reports[0]) / esp_reports[0] * 100):.1f}%)")
