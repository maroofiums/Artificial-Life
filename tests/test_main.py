import main as simulation


def test_main_runs_simulation_and_passes_history_to_reporting(monkeypatch):
    captured = {}
    monkeypatch.setattr(simulation, "SIMULATION_STEPS", 1)
    monkeypatch.setattr(simulation, "PREDATOR_COUNT", 1)
    monkeypatch.setattr(
        simulation,
        "validate_population",
        lambda history: captured.update(validated_history=history),
    )
    monkeypatch.setattr(
        simulation,
        "plot_evolution",
        lambda history: captured.update(plotted_history=history),
    )

    simulation.main()

    assert captured["validated_history"] is captured["plotted_history"]
    assert len(captured["plotted_history"]) == 1
    record = captured["plotted_history"][0]
    assert record["step"] == 1
    assert record["population"] >= 0
    assert record["resources"]["plant"] > 0
