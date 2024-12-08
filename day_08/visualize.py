import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from collections import defaultdict


def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def visualize_wavefronts(data: str | None = None, save_path: str = "wavefronts.png"):
    """Visualize the wavefronts created by the antennas."""
    if data is None:
        data = read_input()

    grid = data.split("\n")
    height = len(grid)
    width = max(len(row) for row in grid)

    # Set up the plot with dark background
    plt.style.use("dark_background")
    # Increased figure size for more detail
    fig, ax = plt.subplots(figsize=(24, 24))
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    # Define distinct colors for different frequencies
    distinct_colors = [
        "#FF0000",  # Red
        "#00FF00",  # Green
        "#0000FF",  # Blue
        "#FFFF00",  # Yellow
        "#FF00FF",  # Magenta
        "#00FFFF",  # Cyan
        "#FFA500",  # Orange
        "#800080",  # Purple
        "#FFC0CB",  # Pink
        "#40E0D0",  # Turquoise
    ]

    freq_map = defaultdict(list)

    # Collect antenna positions
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c != ".":
                freq_map[c].append((x, y))

    # Assign colors to frequencies
    freq_colors = {
        freq: distinct_colors[i % len(distinct_colors)]
        for i, freq in enumerate(sorted(freq_map.keys()))
    }

    # Plot antennas and wavefronts
    for freq, antennas in freq_map.items():
        color = freq_colors[freq]

        # Plot antenna positions as stars
        for x, y in antennas:
            ax.plot(
                x,
                height - y - 1,
                "*",
                color=color,
                markersize=5,
                markeredgecolor="white",
                markeredgewidth=0.4,
                label=f"Antenna {freq}" if (x, y) == antennas[0] else "",
            )

        n = len(antennas)
        if n < 2:
            continue

        for i in range(n):
            for j in range(i + 1, n):
                A = antennas[i]
                B = antennas[j]

                # Calculate midpoint between antennas
                mid_x = (A[0] + B[0]) / 2
                mid_y = (A[1] + B[1]) / 2

                # Calculate antinode positions
                # Antinode C: 2 * B - A
                Cx = 2 * B[0] - A[0]
                Cy = 2 * B[1] - A[1]

                # Calculate distance from midpoint to antinode
                radius = np.sqrt((Cx - mid_x) ** 2 + (Cy - mid_y) ** 2)

                # Draw circle at the midpoint
                circle = Circle(
                    (mid_x, height - mid_y - 1),
                    radius,
                    color=color,
                    fill=False,
                    alpha=0.8,
                    linestyle="--",
                    linewidth=0.3,
                )
                ax.add_patch(circle)

                # Draw additional circles with increasing radii
                for multiplier in range(2, 4):
                    circle_outer = Circle(
                        (mid_x, height - mid_y - 1),
                        radius * multiplier,
                        color=color,
                        fill=False,
                        alpha=0.6,
                        linestyle=":",
                        linewidth=0.2,
                    )
                    ax.add_patch(circle_outer)

    # Adjust plot limits and styling
    margin = max(width, height)
    ax.set_xlim(-margin, width + margin)
    ax.set_ylim(-margin, height + margin)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.1)
    ax.set_title("Antenna Wavefronts Visualization", color="white", pad=20, fontsize=16)

    # Add legend with unique entries
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    legend = ax.legend(
        handles=list(by_label.values()),
        labels=list(by_label.keys()),
        loc="upper right",
        facecolor="black",
        edgecolor="white",
        labelcolor="white",
        fontsize=12,
    )

    # Save the plot with high DPI
    plt.savefig(save_path, dpi=1200, bbox_inches="tight", facecolor="black")
    plt.close()


if __name__ == "__main__":
    # Can be run standalone or imported
    visualize_wavefronts()
    print("Visualization saved as 'wavefronts.png'")
