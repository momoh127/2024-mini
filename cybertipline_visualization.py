"""
CyberTipline Reports Visualization
Generates professional charts for presentations to teachers and investors
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as mpatches

# Set style for professional look
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#f8f9fa'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

# Data
years = ['CY 2021', 'CY 2022', 'CY 2023']
total_reports = [29_397_681, 32_059_029, 36_210_368]
public_reports = [240_598, 256_504, 265_542]
esp_reports = [29_157_083, 31_802_525, 35_944_826]

# Color palette - professional and accessible
colors = {
    'total': '#2E4057',      # Dark blue-gray
    'public': '#048A81',     # Teal
    'esp': '#D64545',        # Red
    'growth': '#F77F00',     # Orange
}


def format_large_number(x, pos):
    """Format large numbers with M (millions) suffix"""
    if x >= 1_000_000:
        return f'{x/1_000_000:.1f}M'
    elif x >= 1_000:
        return f'{x/1_000:.0f}K'
    return f'{x:.0f}'


def add_value_labels(ax, bars, format_as_millions=True):
    """Add value labels on top of bars"""
    for bar in bars:
        height = bar.get_height()
        if format_as_millions and height >= 1_000_000:
            label = f'{height/1_000_000:.2f}M'
        elif height >= 1_000:
            label = f'{height/1_000:.0f}K'
        else:
            label = f'{height:,.0f}'
        
        ax.text(bar.get_x() + bar.get_width()/2., height,
                label,
                ha='center', va='bottom',
                fontsize=10, fontweight='bold',
                color='#2c3e50')


def calculate_growth_rate(data):
    """Calculate year-over-year growth rates"""
    growth_rates = []
    for i in range(1, len(data)):
        rate = ((data[i] - data[i-1]) / data[i-1]) * 100
        growth_rates.append(rate)
    return growth_rates


# Create figure with multiple subplots
fig = plt.figure(figsize=(20, 12))
fig.suptitle('CyberTipline Reports Analysis (2021-2023)', 
             fontsize=24, fontweight='bold', y=0.98, color='#2c3e50')

# Subplot 1: Total Reports Trend (Top Left)
ax1 = plt.subplot(2, 3, 1)
x_pos = np.arange(len(years))
bars1 = ax1.bar(x_pos, total_reports, color=colors['total'], alpha=0.8, edgecolor='white', linewidth=2)
add_value_labels(ax1, bars1)

ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Reports', fontsize=12, fontweight='bold')
ax1.set_title('Total CyberTipline Reports', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(years, fontsize=11)
ax1.yaxis.set_major_formatter(FuncFormatter(format_large_number))
ax1.grid(axis='y', alpha=0.3)

# Subplot 2: Stacked Bar Chart (Top Middle)
ax2 = plt.subplot(2, 3, 2)
bars_public = ax2.bar(x_pos, public_reports, color=colors['public'], alpha=0.85, 
                       label='Public Reports', edgecolor='white', linewidth=2)
bars_esp = ax2.bar(x_pos, esp_reports, bottom=public_reports, 
                    color=colors['esp'], alpha=0.85, label='ESP Reports',
                    edgecolor='white', linewidth=2)

ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Reports', fontsize=12, fontweight='bold')
ax2.set_title('Reports Breakdown: Public vs ESP', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(years, fontsize=11)
ax2.yaxis.set_major_formatter(FuncFormatter(format_large_number))
ax2.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax2.grid(axis='y', alpha=0.3)

# Subplot 3: Grouped Bar Chart (Top Right)
ax3 = plt.subplot(2, 3, 3)
bar_width = 0.25
x_pos = np.arange(len(years))

bars3_1 = ax3.bar(x_pos - bar_width, total_reports, bar_width, 
                   label='Total', color=colors['total'], alpha=0.85, edgecolor='white', linewidth=1.5)
bars3_2 = ax3.bar(x_pos, public_reports, bar_width,
                   label='Public', color=colors['public'], alpha=0.85, edgecolor='white', linewidth=1.5)
bars3_3 = ax3.bar(x_pos + bar_width, esp_reports, bar_width,
                   label='ESP', color=colors['esp'], alpha=0.85, edgecolor='white', linewidth=1.5)

ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
ax3.set_ylabel('Number of Reports', fontsize=12, fontweight='bold')
ax3.set_title('Side-by-Side Comparison', fontsize=14, fontweight='bold', pad=15)
ax3.set_xticks(x_pos)
ax3.set_xticklabels(years, fontsize=11)
ax3.yaxis.set_major_formatter(FuncFormatter(format_large_number))
ax3.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax3.grid(axis='y', alpha=0.3)

# Subplot 4: Growth Rate Analysis (Bottom Left)
ax4 = plt.subplot(2, 3, 4)
total_growth = calculate_growth_rate(total_reports)
public_growth = calculate_growth_rate(public_reports)
esp_growth = calculate_growth_rate(esp_reports)

growth_years = ['2021→2022', '2022→2023']
x_pos_growth = np.arange(len(growth_years))
bar_width = 0.25

bars4_1 = ax4.bar(x_pos_growth - bar_width, total_growth, bar_width,
                   label='Total', color=colors['total'], alpha=0.85, edgecolor='white', linewidth=1.5)
bars4_2 = ax4.bar(x_pos_growth, public_growth, bar_width,
                   label='Public', color=colors['public'], alpha=0.85, edgecolor='white', linewidth=1.5)
bars4_3 = ax4.bar(x_pos_growth + bar_width, esp_growth, bar_width,
                   label='ESP', color=colors['esp'], alpha=0.85, edgecolor='white', linewidth=1.5)

# Add percentage labels
for bars in [bars4_1, bars4_2, bars4_3]:
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom' if height > 0 else 'top',
                fontsize=9, fontweight='bold')

ax4.set_xlabel('Period', fontsize=12, fontweight='bold')
ax4.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax4.set_title('Year-over-Year Growth Rate', fontsize=14, fontweight='bold', pad=15)
ax4.set_xticks(x_pos_growth)
ax4.set_xticklabels(growth_years, fontsize=11)
ax4.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
ax4.grid(axis='y', alpha=0.3)

# Subplot 5: Public Reports Detailed View (Bottom Middle)
ax5 = plt.subplot(2, 3, 5)
bars5 = ax5.bar(x_pos, public_reports, color=colors['public'], alpha=0.85, 
                edgecolor='white', linewidth=2)
add_value_labels(ax5, bars5, format_as_millions=False)

ax5.set_xlabel('Year', fontsize=12, fontweight='bold')
ax5.set_ylabel('Number of Reports', fontsize=12, fontweight='bold')
ax5.set_title('Public CyberTipline Reports', fontsize=14, fontweight='bold', pad=15)
ax5.set_xticks(x_pos)
ax5.set_xticklabels(years, fontsize=11)
ax5.yaxis.set_major_formatter(FuncFormatter(format_large_number))
ax5.grid(axis='y', alpha=0.3)

# Subplot 6: ESP Reports Detailed View (Bottom Right)
ax6 = plt.subplot(2, 3, 6)
bars6 = ax6.bar(x_pos, esp_reports, color=colors['esp'], alpha=0.85,
                edgecolor='white', linewidth=2)
add_value_labels(ax6, bars6)

ax6.set_xlabel('Year', fontsize=12, fontweight='bold')
ax6.set_ylabel('Number of Reports', fontsize=12, fontweight='bold')
ax6.set_title('ESP CyberTipline Reports', fontsize=14, fontweight='bold', pad=15)
ax6.set_xticks(x_pos)
ax6.set_xticklabels(years, fontsize=11)
ax6.yaxis.set_major_formatter(FuncFormatter(format_large_number))
ax6.grid(axis='y', alpha=0.3)

# Add key insights text box
insights_text = f"""Key Insights:
• Total reports increased by {((total_reports[-1] - total_reports[0])/total_reports[0]*100):.1f}% from 2021 to 2023
• ESP reports comprise {(esp_reports[-1]/total_reports[-1]*100):.1f}% of all reports in 2023
• Public reports show steady growth: {public_growth[0]:.1f}% then {public_growth[1]:.1f}%
• Average annual growth: {(sum(total_growth)/len(total_growth)):.1f}%"""

fig.text(0.5, 0.02, insights_text, 
         ha='center', fontsize=11, 
         bbox=dict(boxstyle='round', facecolor='#e8f4f8', alpha=0.8, edgecolor='#2c3e50', linewidth=2),
         family='monospace')

plt.tight_layout(rect=[0, 0.06, 1, 0.96])

# Save the figure
output_file = 'cybertipline_reports_visualization.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Visualization saved as: {output_file}")

# Create a second figure with a line chart for trends
fig2, ax_line = plt.subplots(figsize=(14, 8), facecolor='white')

# Plot lines
ax_line.plot(years, total_reports, marker='o', linewidth=3, markersize=10, 
             label='Total Reports', color=colors['total'], alpha=0.8)
ax_line.plot(years, esp_reports, marker='s', linewidth=3, markersize=10,
             label='ESP Reports', color=colors['esp'], alpha=0.8)
ax_line.plot(years, public_reports, marker='^', linewidth=3, markersize=10,
             label='Public Reports', color=colors['public'], alpha=0.8)

# Add value annotations
for i, year in enumerate(years):
    ax_line.annotate(f'{total_reports[i]/1_000_000:.2f}M', 
                     (i, total_reports[i]), textcoords="offset points",
                     xytext=(0,10), ha='center', fontsize=10, fontweight='bold')
    ax_line.annotate(f'{esp_reports[i]/1_000_000:.2f}M',
                     (i, esp_reports[i]), textcoords="offset points",
                     xytext=(0,-20), ha='center', fontsize=10, fontweight='bold')

ax_line.set_xlabel('Year', fontsize=14, fontweight='bold')
ax_line.set_ylabel('Number of Reports', fontsize=14, fontweight='bold')
ax_line.set_title('CyberTipline Reports Trend Analysis (2021-2023)', 
                  fontsize=18, fontweight='bold', pad=20, color='#2c3e50')
ax_line.yaxis.set_major_formatter(FuncFormatter(format_large_number))
ax_line.legend(loc='upper left', fontsize=12, framealpha=0.95)
ax_line.grid(True, alpha=0.3, linestyle='--')
ax_line.set_facecolor('#f8f9fa')

plt.tight_layout()

# Save the trend chart
trend_file = 'cybertipline_trend_chart.png'
plt.savefig(trend_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Trend chart saved as: {trend_file}")

# Create a third figure - Pie chart for 2023 breakdown
fig3, (ax_pie1, ax_pie2) = plt.subplots(1, 2, figsize=(16, 7), facecolor='white')

# 2023 Distribution
sizes_2023 = [public_reports[2], esp_reports[2]]
labels_2023 = ['Public Reports', 'ESP Reports']
colors_pie = [colors['public'], colors['esp']]
explode = (0.05, 0)

wedges, texts, autotexts = ax_pie1.pie(sizes_2023, explode=explode, labels=labels_2023,
                                         colors=colors_pie, autopct='%1.1f%%',
                                         shadow=True, startangle=90,
                                         textprops={'fontsize': 12, 'fontweight': 'bold'})

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(14)

ax_pie1.set_title('2023 Report Distribution', fontsize=16, fontweight='bold', pad=20)

# Add absolute numbers
centre_circle = plt.Circle((0,0), 0.70, fc='white')
ax_pie1.add_artist(centre_circle)
ax_pie1.text(0, 0, f'Total\n{total_reports[2]:,}', 
             ha='center', va='center', fontsize=14, fontweight='bold')

# ESP vs Public comparison across years
ax_pie2.axis('off')
comparison_text = f"""
Report Type Comparison (2021-2023)

Public Reports:
  2021: {public_reports[0]:,}
  2022: {public_reports[1]:,}
  2023: {public_reports[2]:,}
  Growth: +{((public_reports[2]-public_reports[0])/public_reports[0]*100):.1f}%

ESP Reports:
  2021: {esp_reports[0]:,}
  2022: {esp_reports[1]:,}
  2023: {esp_reports[2]:,}
  Growth: +{((esp_reports[2]-esp_reports[0])/esp_reports[0]*100):.1f}%

Total Reports:
  2021: {total_reports[0]:,}
  2022: {total_reports[1]:,}
  2023: {total_reports[2]:,}
  Growth: +{((total_reports[2]-total_reports[0])/total_reports[0]*100):.1f}%
"""

ax_pie2.text(0.5, 0.5, comparison_text, 
             ha='center', va='center', fontsize=13,
             bbox=dict(boxstyle='round', facecolor='#f8f9fa', 
                      alpha=0.9, edgecolor='#2c3e50', linewidth=2),
             family='monospace', fontweight='bold')

fig3.suptitle('CyberTipline Reports: Distribution & Summary', 
              fontsize=18, fontweight='bold', y=0.98, color='#2c3e50')

plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save the distribution chart
distribution_file = 'cybertipline_distribution.png'
plt.savefig(distribution_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Distribution chart saved as: {distribution_file}")

print("\n" + "="*60)
print("All visualizations created successfully!")
print("="*60)
print(f"\nFiles generated:")
print(f"  1. {output_file} - Comprehensive 6-panel analysis")
print(f"  2. {trend_file} - Line chart showing trends")
print(f"  3. {distribution_file} - Pie chart and summary")
print("\nThese charts are presentation-ready at 300 DPI resolution.")
