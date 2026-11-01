import matplotlib.pyplot as plt


def plot_evolution(history):
    if not history:
        print("No evolution data.")
        return

    steps = [x["step"] for x in history]
    population = [x["population"] for x in history]
    fitness = [x["average_fitness"] for x in history]
    age = [x["average_age"] for x in history]

    fig, axes = plt.subplots(3, 1, figsize=(10, 10))

    axes[0].plot(steps, population)
    axes[0].set_title("Population Over Time")
    axes[0].set_ylabel("Organisms")
    axes[0].grid(True)

    axes[1].plot(steps, fitness)
    axes[1].set_title("Average Fitness Over Time")
    axes[1].set_ylabel("Fitness")
    axes[1].grid(True)

    axes[2].plot(steps, age)
    axes[2].set_title("Average Age Over Time")
    axes[2].set_ylabel("Age")
    axes[2].set_xlabel("Simulation Steps")
    axes[2].grid(True)

    plt.tight_layout()
    plt.show()