"""
Generate Professional Academic System Workflow Diagram for HousePrice AI
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_workflow():
    fig, ax = plt.subplots(figsize=(13.5, 4.5), dpi=300)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.axis('off')

    # Workflow nodes
    nodes = [
        ("Curated House Price\nDataset (1,800 records)", "#0f172a", "#38bdf8", "Database / CSV"),
        ("Data Cleaning &\nValidation", "#0f172a", "#94a3b8", "Data Preprocessing"),
        ("Feature Selection &\nPartitioning (80:20)", "#0f172a", "#94a3b8", "Feature Engineering"),
        ("ColumnTransformer\n(OneHot + Scaler)", "#1e3a8a", "#60a5fa", "Categorical Encoding"),
        ("Multiple Linear\nRegression Model", "#064e3b", "#34d399", "Supervised ML (OLS)"),
        ("Price Estimation\nPipeline (₹ INR)", "#701a75", "#f472b6", "Inference Engine"),
        ("Dynamic Charts &\nResidual Diagnostics", "#854d0e", "#facc15", "Results Visualization"),
        ("Interactive Web\nDashboard (Flask)", "#1e293b", "#10b981", "User Presentation")
    ]

    n = len(nodes)
    box_width = 1.25
    box_height = 1.3
    spacing = 0.42
    start_x = 0.4
    y = 1.6

    for i, (title, bg_color, border_color, subtitle) in enumerate(nodes):
        x = start_x + i * (box_width + spacing)
        
        # Rounded rectangle
        rect = patches.FancyBboxPatch(
            (x, y), box_width, box_height,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            linewidth=2.2,
            edgecolor=border_color,
            facecolor=bg_color,
            zorder=3
        )
        ax.add_patch(rect)

        # Step badge number
        badge = patches.Circle((x + 0.18, y + box_height - 0.18), 0.13, color=border_color, zorder=4)
        ax.add_patch(badge)
        ax.text(x + 0.18, y + box_height - 0.18, str(i + 1), ha='center', va='center',
                fontsize=9, fontweight='bold', color='#000000', zorder=5)

        # Category/subtitle
        ax.text(x + box_width / 2.0 + 0.08, y + box_height - 0.18, subtitle.upper(), ha='center', va='center',
                fontsize=6.5, fontweight='bold', color=border_color, zorder=4, fontfamily='sans-serif')

        # Node title text
        ax.text(x + box_width / 2.0, y + box_height / 2.0 - 0.12, title, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='#ffffff', zorder=4, fontfamily='sans-serif')

        # Connector arrow to next node
        if i < n - 1:
            arrow_start_x = x + box_width + 0.02
            arrow_end_x = arrow_start_x + spacing - 0.04
            arrow_y = y + box_height / 2.0
            ax.annotate(
                '', xy=(arrow_end_x, arrow_y), xytext=(arrow_start_x, arrow_y),
                arrowprops=dict(
                    arrowstyle="->,head_width=0.35,head_length=0.45",
                    color='#0284c7',
                    lw=2.2
                ),
                zorder=2
            )

    # Frame boundaries
    ax.set_xlim(0, start_x + n * (box_width + spacing) - spacing + 0.4)
    ax.set_ylim(0.8, 3.6)

    # Title on top
    ax.text((start_x + (start_x + n * (box_width + spacing) - spacing)) / 2, 3.3,
            "HOUSEPRICE AI: END-TO-END MACHINE LEARNING ARCHITECTURAL PIPELINE",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0f172a', fontfamily='serif')

    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), "workflow_diagram.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Workflow diagram successfully generated at {output_path}")

if __name__ == "__main__":
    generate_workflow()
