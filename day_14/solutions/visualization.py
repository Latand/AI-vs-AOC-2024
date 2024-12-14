import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from gemini_1206 import parse_robots, read_input, simulate_robots

# Set up the plot with a dark background for better Christmas light effect
plt.style.use("dark_background")


def create_animation():
    # Read and parse the input
    data = read_input()
    robots = parse_robots(data)
    width, height = 101, 103

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(15, 18))
    ax.set_facecolor("#0C1445")  # Dark blue background for night sky effect
    fig.patch.set_facecolor("#0C1445")

    # Initialize empty scatter plot with Christmas colors
    scatter = ax.scatter([], [], c=[], cmap="RdYlBu_r", s=150, alpha=0.8)
    title = ax.set_title(
        "Robot Christmas Formation\nTime: 0", color="white", fontsize=14
    )

    # Add some stars in the background
    stars_x = np.random.uniform(0, width, 100)
    stars_y = np.random.uniform(0, height, 100)
    ax.scatter(stars_x, stars_y, color="white", alpha=0.3, s=2)

    # Add some bright stars
    bright_stars_x = np.random.uniform(0, width, 20)
    bright_stars_y = np.random.uniform(0, height, 20)
    bright_stars = ax.scatter(
        bright_stars_x, bright_stars_y, color="white", alpha=0.8, s=4
    )

    # Add grid and labels
    ax.grid(True, alpha=0.2)
    ax.set_xlabel("X Position", color="white")
    ax.set_ylabel("Y Position", color="white")

    # Invert Y axis to flip the plot
    ax.invert_yaxis()

    def init():
        ax.set_xlim(-1, width + 1)
        ax.set_ylim(height + 1, -1)  # Flipped Y limits
        return scatter, title, bright_stars

    def update(frame):
        # Calculate real time (we want to reach 6512 in 1 second at 120 FPS)
        # 1 second * 120 FPS = 120 frames total
        # So each frame should advance by: 6512/120 ≈ 54.3 iterations
        time = int(frame * (6512 / 120))  # Scale to reach 6512 in 1 second

        # Simulate robots
        grid = simulate_robots(robots, width, height, time)

        # Extract positions and counts
        positions = np.array(list(grid.keys()))
        counts = np.array(list(grid.values()))

        if len(positions) > 0:
            # Update scatter plot
            scatter.set_offsets(positions)
            # Normalize counts for color mapping
            colors = np.log1p(counts)  # Using log scale for better color distribution
            scatter.set_array(colors)

        # Make stars twinkle (adjusted for higher FPS)
        bright_stars.set_alpha(0.5 + 0.3 * np.sin(frame * 0.1))

        # Special title for final formation
        if time >= 6512:
            title.set_text(
                "Robot Christmas Formation\nTime: 6512 - Merry Christmas! 🎄"
            )
            ani.event_source.stop()
        else:
            title.set_text(f"Robot Christmas Formation\nTime: {time}")

        return scatter, title, bright_stars

    # Create animation (120 FPS)
    ani = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=None,
        interval=1000 / 120,  # Exactly 120 FPS (8.33ms per frame)
        blit=True,
    )

    # Add colorbar
    plt.colorbar(scatter, label="Log(Robot Count + 1)")
    plt.show()


if __name__ == "__main__":
    create_animation()
