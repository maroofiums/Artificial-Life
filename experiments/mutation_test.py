import numpy as np
import matplotlib.pyplot as plt

from agents.brain import NeuralBrain


def compare_mutations():
    rates = [0.01, 0.05, 0.1, 0.2, 0.5]
    results = []

    parent = NeuralBrain()

    for rate in rates:
        differences = []

        for _ in range(100):
            child = parent.clone_mutated(
                mutation_rate=rate,
                mutation_scale=0.1
            )

            difference = np.mean(
                np.abs(parent.W1 - child.W1)
            )

            differences.append(difference)

        results.append(np.mean(differences))

    plt.plot(rates, results, marker="o")
    plt.xlabel("Mutation Rate")
    plt.ylabel("Average Weight Difference")
    plt.title("Mutation Rate vs Genetic Variation")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    compare_mutations()