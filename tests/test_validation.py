from experiments.validation import validate_population


def test_validate_population_handles_insufficient_history(capsys):
    validate_population([])
    validate_population([{"step": 1}])

    assert "Not enough experiment data." in capsys.readouterr().out


def test_validate_population_reports_metrics_and_survival_change(capsys):
    history = [
        {
            "population": 4,
            "average_fitness": 10.126,
            "average_age": 2.0,
            "max_generation": 1,
        },
        {
            "population": 5,
            "average_fitness": 12.345,
            "average_age": 3.5,
            "max_generation": 4,
        },
    ]

    validate_population(history)
    output = capsys.readouterr().out

    assert "Initial population: 4" in output
    assert "Final population: 5" in output
    assert "Initial fitness: 10.13" in output
    assert "Final fitness: 12.35" in output
    assert "Maximum generation: 4" in output
    assert "Survival duration increased." in output


def test_validate_population_reports_no_improvement(capsys):
    validate_population([
        {
            "population": 1,
            "average_fitness": 1.0,
            "average_age": 2.0,
            "max_generation": 1,
        },
        {
            "population": 1,
            "average_fitness": 1.0,
            "average_age": 2.0,
            "max_generation": 1,
        },
    ])

    assert "No survival improvement detected." in capsys.readouterr().out
