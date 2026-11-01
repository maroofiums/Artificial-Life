import matplotlib.pyplot as plt


def plot_evolution(history: dict):
    if not history:
        print("No Evolution data available")
        return

    steps = [item["step"] for item in history]
    population = [item["population"] for item in history]
    fitness = [item["average_fitness"] for item in history]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(steps, population, label="Population")
    ax1.set_xlabel("Simulation Step")
    ax1.set_ylabel("Population")


    ax2 = ax1.twinx()
    ax2.plot(steps, fitness, label="Average Fitness")
    ax1.set_ylabel("Average Fitness")

    plt.title("Digital Evolution Laboratory")
    fig.tight_layout()
    plt.show()