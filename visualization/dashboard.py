
import matplotlib.pyplot as plt


def plot_evolution(history):
    if not history:
        print("No evolution data.")
        return

    steps = [x["step"] for x in history]

    species_ids = list(history[0]["species_counts"])

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    # 1. Total population
    population = [x["population"] for x in history]

    axes[0, 0].plot(steps, population)
    axes[0, 0].set_title("Total Population")
    axes[0, 0].set_ylabel("Organisms")
    axes[0, 0].grid(True)

    # 2. Population by species
    for species in species_ids:
        counts = [
            x["species_counts"][species]
            for x in history
        ]

        axes[0, 1].plot(
            steps, counts, label=species.capitalize()
        )

    axes[0, 1].set_title("Species Population Dynamics")
    axes[0, 1].set_ylabel("Organisms")
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    # 3. Average fitness
    fitness = [x["average_fitness"] for x in history]

    axes[1, 0].plot(steps, fitness)
    axes[1, 0].set_title("Average Fitness")
    axes[1, 0].set_xlabel("Simulation Steps")
    axes[1, 0].grid(True)

    # 4. Average age
    age = [x["average_age"] for x in history]

    axes[1, 1].plot(steps, age)
    axes[1, 1].set_title("Average Age")
    axes[1, 1].set_xlabel("Simulation Steps")
    axes[1, 1].grid(True)

    fig.suptitle("Artificial Life — Ecosystem Dashboard")
    plt.tight_layout()
    plt.show()
