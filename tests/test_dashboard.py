import matplotlib.pyplot as plt

from visualization.dashboard import plot_evolution


def test_plot_evolution_draws_dashboard_and_resource_figures(monkeypatch):
    shown_figures = []
    monkeypatch.setattr(plt, "show", lambda: shown_figures.append(plt.gcf()))
    history = [
        {
            "step": 1,
            "population": 3,
            "species_counts": {"herbivore": 2, "carnivore": 1},
            "average_fitness": 12.5,
            "average_age": 2.0,
            "resources": {"plant": 0.8, "meat": 0.2, "remains": 0.1},
        },
        {
            "step": 2,
            "population": 4,
            "species_counts": {"herbivore": 2, "carnivore": 2},
            "average_fitness": 15.0,
            "average_age": 2.5,
            "resources": {"plant": 0.7, "meat": 0.3, "remains": 0.15},
        },
    ]

    try:
        plot_evolution(history)

        assert len(shown_figures) == 2
        assert len(shown_figures[0].axes) == 4
        resource_axis = shown_figures[1].axes[0]
        assert resource_axis.get_title() == "Ecosystem Resource Availability"
        assert [line.get_label() for line in resource_axis.lines] == [
            "Plant",
            "Meat",
            "Remains",
        ]
        assert list(resource_axis.lines[0].get_ydata()) == [0.8, 0.7]
    finally:
        plt.close("all")


def test_plot_evolution_handles_empty_history(capsys, monkeypatch):
    monkeypatch.setattr(plt, "show", lambda: None)

    plot_evolution([])

    assert "No evolution data." in capsys.readouterr().out
