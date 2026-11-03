import csv

import matplotlib.pyplot as plt

from experiments import run_comparison


def test_importing_comparison_module_does_not_run_experiments():
    assert callable(run_comparison.main)


def test_comparison_runs_strategies_and_writes_csv_outputs(
    monkeypatch,
    tmp_path,
):
    calls = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(plt, "show", lambda: None)

    def fake_run_experiment(mutation_rate, seed, steps):
        calls.append((mutation_rate, seed, steps))
        value = float(seed + 1)
        history = [{
            "population": int(value),
            "average_fitness": value * 10,
            "average_age": value * 2,
            "max_generation": int(value),
            "species_counts": {"herbivore": int(value)},
            "resources": {"plant": 0.5, "meat": 0.2, "remains": 0.1},
        }]
        return history, {}, {}, {}

    monkeypatch.setattr(run_comparison, "run_experiment", fake_run_experiment)

    try:
        run_comparison.main()
    finally:
        plt.close("all")

    assert len(calls) == 15
    assert {steps for _, _, steps in calls} == {500}
    assert {rate for rate, _, _ in calls} == {0.0, 0.05, 0.2}
    assert (tmp_path / "experiment_results.csv").exists()
    assert (tmp_path / "experiment_runs.csv").exists()

    with (tmp_path / "experiment_results.csv").open(newline="") as file:
        rows = list(csv.reader(file))

    assert rows[0] == [
        "Strategy",
        "Metric",
        "Mean",
        "Standard Deviation",
    ]
    assert len(rows) == 1 + 3 * len(run_comparison.METRICS)
