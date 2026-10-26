"""
Generate publication-quality charts for the UrbanGen AI IEEE conference paper:
1. fig_multimodel_loss_bars.png - Grouped bar chart comparing initial vs 50-epoch final loss (log scale).
2. fig_energy_carbon_breakdown.png - Combined donut pie chart + bar chart for Green AI energy/carbon audit.
3. fig_landuse_distribution.png - Comprehensive urban zoning functional cluster pie chart for UCMerced dataset.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Set IEEE conference styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.size'] = 9
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8.5
plt.rcParams['ytick.labelsize'] = 8.5
plt.rcParams['legend.fontsize'] = 8.5
plt.rcParams['figure.titlesize'] = 11

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Multi-Model Loss Convergence Bar Chart (fig_multimodel_loss_bars.png)
# ---------------------------------------------------------------------------
def generate_loss_bars():
    models = [
        'Denoising\nU-Net AE',
        'Spatial\nVAE',
        'ResNet-18\nClassifier',
        'Residual\ncDCGAN',
        'Conditional\nDDPM',
        'MiniGPT\nTransformer'
    ]
    initial_loss = [0.1155, 0.2042, 3.0607, 3.9044, 0.3623, 4.2387]
    final_loss = [0.00617, 0.0483, 0.0615, 1.1890, 0.0304, 0.1043]
    
    x = np.arange(len(models))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=300)
    
    rects1 = ax.bar(x - width/2, initial_loss, width, label='Initial Epoch Loss', color='#4A90E2', edgecolor='#2B6CB0', alpha=0.9, zorder=3)
    rects2 = ax.bar(x + width/2, final_loss, width, label='Final 50-Epoch Loss', color='#2ECC71', edgecolor='#27AE60', alpha=0.95, zorder=3)

    ax.set_ylabel('Objective Loss (Log Scale)')
    ax.set_title('Empirical Convergence: Initial vs. 50-Epoch Benchmark Loss across Specialized Architectures')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_yscale('log')
    ax.set_ylim(0.002, 10.0)
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax.legend(frameon=True, facecolor='white', framealpha=0.95, loc='upper right')

    # Add numeric labels on top of bars
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=7.5, color='#1A365D', weight='bold')

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.4f}' if height < 0.01 else f'{height:.3f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=7.5, color='#145A32', weight='bold')

    plt.tight_layout()
    out_path = OUTPUT_DIR / "fig_multimodel_loss_bars.png"
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


# ---------------------------------------------------------------------------
# 2. Green AI Energy & Carbon Breakdown (fig_energy_carbon_breakdown.png)
# ---------------------------------------------------------------------------
def generate_energy_carbon_breakdown():
    models = ['U-Net AE', 'Spatial VAE', 'Classifier', 'cDCGAN', 'DDPM', 'MiniGPT']
    energy_kwh = [0.030, 0.013, 0.029, 0.030, 0.029, 0.002]
    time_min = [15.2, 6.7, 14.2, 15.0, 14.0, 1.2]
    co2_g = [21.2, 9.2, 20.5, 21.2, 20.5, 1.4]
    
    colors = ['#3498DB', '#9B59B6', '#E67E22', '#E74C3C', '#1ABC9C', '#F1C40F']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.1), dpi=300)

    # Subplot 1: Donut Pie Chart of Energy Footprint
    wedges, texts, autotexts = ax1.pie(
        energy_kwh, 
        labels=models, 
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=1.5),
        pctdistance=0.75,
        textprops=dict(fontsize=8)
    )
    for at in autotexts:
        at.set_fontsize(7.5)
        at.set_weight('bold')
        at.set_color('white')
    ax1.set_title('(a) Energy Footprint by Model\nTotal: 0.133 kWh (94.0 g CO₂e)', pad=10)

    # Subplot 2: Bar Chart of Training Time & Carbon
    y_pos = np.arange(len(models))
    bars = ax2.barh(y_pos, time_min, color=colors, edgecolor='#333333', linewidth=0.5, alpha=0.9, zorder=3)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(models)
    ax2.invert_yaxis()  # Top-down order
    ax2.set_xlabel('Training Duration (minutes)')
    ax2.set_title('(b) Training Time per Architecture\nUniform 50-Epoch Horizon (Total: 66.3 min)', pad=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)

    # Add numeric annotations with time and carbon
    for i, bar in enumerate(bars):
        w = bar.get_width()
        ax2.annotate(f'{w:.1f} m ({co2_g[i]:.1f}g)',
                     xy=(w, bar.get_y() + bar.get_height() / 2),
                     xytext=(4, 0), textcoords="offset points",
                     ha='left', va='center', fontsize=7.5, color='#2C3E50', weight='bold')

    ax2.set_xlim(0, 20)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "fig_energy_carbon_breakdown.png"
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


# ---------------------------------------------------------------------------
# 3. UCMerced Land-Use Functional Cluster Pie Chart (fig_landuse_distribution.png)
# ---------------------------------------------------------------------------
def generate_landuse_pie():
    # 21 classes x 100 images = 2,100 tiles total
    categories = [
        'Natural & Ecological\n(Agri, Beach, Forest, etc.)',
        'Transportation\n(Freeway, Overpass, Runway)',
        'Commercial & Civic\n(Buildings, Storage, Parking)',
        'Residential Living\n(Dense, Medium, Sparse)',
        'Sports & Recreation\n(Golf, Tennis, Diamond)'
    ]
    counts = [600, 500, 400, 300, 300] # 6, 5, 4, 3, 3 classes * 100
    percentages = [c / 2100 * 100 for c in counts]
    
    cluster_colors = ['#27AE60', '#2980B9', '#D35400', '#8E44AD', '#16A085']
    explode = (0.04, 0.02, 0.02, 0.02, 0.02)

    fig, ax = plt.subplots(figsize=(6.2, 3.2), dpi=300)
    wedges, texts, autotexts = ax.pie(
        counts, 
        explode=explode, 
        labels=categories, 
        autopct='%1.1f%%',
        startangle=120,
        colors=cluster_colors,
        wedgeprops=dict(edgecolor='white', linewidth=1.5),
        pctdistance=0.65,
        textprops=dict(fontsize=8)
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_weight('bold')
        at.set_color('white')

    ax.set_title('UCMerced Benchmark Functional Zoning Categorization\n(21 Distinct Classes, 2,100 High-Resolution Remote Sensing Parcels)', fontsize=9.5, pad=12)

    plt.tight_layout()
    out_path = OUTPUT_DIR / "fig_landuse_distribution.png"
    plt.savefig(out_path, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    generate_loss_bars()
    generate_energy_carbon_breakdown()
    generate_landuse_pie()
