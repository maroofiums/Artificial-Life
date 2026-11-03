import matplotlib.pyplot as plt

from experiments.mutation_test import compare_mutations


def test_compare_mutations_plots_each_configured_rate(monkeypatch):
    shown = []
    monkeypatch.setattr(plt, "show", lambda: shown.append(plt.gcf()))
    plt.close("all")

    compare_mutations()

    try:
        assert len(shown) == 1
        axis = shown[0].axes[0]
        assert axis.get_xlabel() == "Mutation Rate"
        assert axis.get_ylabel() == "Average Weight Difference"
        assert list(axis.lines[0].get_xdata()) == [0.01, 0.05, 0.1, 0.2, 0.5]
        assert len(axis.lines[0].get_ydata()) == 5
    finally:
        plt.close("all")
