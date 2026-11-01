import matplotlib.pyplot as plt
from experiments.runner import run_experiment

experiments = {
    "Baseline": 0.0,
    "Low Mutation": 0.05,
    "High Mutation": 0.20
}

results = {}

for name, rate in experiments.items():
    print(f"Running {name}...")

    history = run_experiment(rate, seed=42, steps=500)

    if not history:
        print(f"{name}: No surviving organisms!")
        continue

    results[name] = history[-1]

# Comparison dashboard
if results:
    names = list(results.keys())

    metrics = [
        ("population", "Final Population"),
        ("average_fitness", "Average Fitness"),
        ("average_age", "Average Age"),
        ("max_generation", "Maximum Generation")
    ]

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    for ax, (key, title) in zip(axes.flat, metrics):
        values = [results[name][key] for name in names]

        ax.bar(names, values)
        ax.set_title(title)
        ax.set_ylabel(title)
        ax.tick_params(axis="x", rotation=15)
        ax.grid(axis="y", alpha=0.3)

    plt.suptitle("Artificial Life — Experiment Comparison")
    plt.tight_layout()
    plt.show()

    for name, result in results.items():
        print(
            f"{name}: Population={result['population']}, "
            f"Fitness={result['average_fitness']:.2f}, "
            f"Age={result['average_age']:.2f}, "
            f"Generation={result['max_generation']}"
        )