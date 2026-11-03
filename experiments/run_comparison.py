import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from experiments.runner import run_experiment


EXPERIMENTS = {
    "Baseline": 0.0,
    "Low Mutation": 0.05,
    "High Mutation": 0.20,
}
METRICS = (
    "population",
    "average_fitness",
    "average_age",
    "max_generation",
)


def main() -> None:
    results = {}
    raw_results = []

    for name, rate in EXPERIMENTS.items():
        print(f"Running {name}...")

        runs = []

        for seed in range(5):
            history, _, _, _ = run_experiment(
                rate,
                seed=seed,
                steps=500,
            )

            if history:
                runs.append(history[-1])
                raw_results.append({
                    "strategy": name,
                    "mutation_rate": rate,
                    "seed": seed,
                    **history[-1],
                })

        if not runs:
            print(f"{name}: No surviving organisms!")
            continue

        results[name] = {}

        for key in METRICS:
            values = [run[key] for run in runs]
            results[name][key] = np.mean(values)
            results[name][key + "_std"] = np.std(values, ddof=1)

    if results:
        names = list(results)
        metric_titles = (
            ("population", "Final Population"),
            ("average_fitness", "Average Fitness"),
            ("average_age", "Average Age"),
            ("max_generation", "Maximum Generation"),
        )

        _, axes = plt.subplots(2, 2, figsize=(11, 8))

        for ax, (key, title) in zip(axes.flat, metric_titles):
            values = [results[name][key] for name in names]
            errors = [results[name][key + "_std"] for name in names]

            ax.bar(names, values, yerr=errors, capsize=5)
            ax.set_title(title)
            ax.set_ylabel(title)
            ax.tick_params(axis="x", rotation=15)
            ax.grid(axis="y", alpha=0.3)

        plt.suptitle("Artificial Life - Experiment Comparison")
        plt.tight_layout()
        plt.show()

        for name, result in results.items():
            print(f"\n{name}")

            for key in METRICS:
                mean = result[key]
                std = result[key + "_std"]
                print(f"{key}: {mean:.2f} ± {std:.2f}")

    with open("experiment_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Strategy",
            "Metric",
            "Mean",
            "Standard Deviation",
        ])

        for name, result in results.items():
            for key in METRICS:
                writer.writerow([
                    name,
                    key,
                    result[key],
                    result[key + "_std"],
                ])

    print("\nResults saved to experiment_results.csv")
    pd.DataFrame(raw_results).to_csv("experiment_runs.csv", index=False)
    print("Individual runs saved to experiment_runs.csv")


if __name__ == "__main__":
    main()
