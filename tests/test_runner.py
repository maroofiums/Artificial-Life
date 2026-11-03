import numpy as np

from agents.species import SPECIES_REGISTRY
import experiments.runner as runner
from experiments.runner import run_experiment


def test_run_experiment_returns_history_resources_births_and_deaths():
    history, resources, births, deaths = run_experiment(
        mutation_rate=0.0,
        seed=3,
        steps=2,
    )

    assert len(history) == 2
    assert [record["step"] for record in history] == [1, 2]
    assert all(record["population"] >= 0 for record in history)
    assert all(set(record["species_counts"]) == set(SPECIES_REGISTRY) for record in history)
    assert set(resources) == {"plant", "meat", "remains"}
    assert set(births) == set(SPECIES_REGISTRY)
    assert set(deaths) == set(SPECIES_REGISTRY)
    assert all(count >= 0 for count in births.values())
    assert all(count >= 0 for count in deaths.values())


def test_run_experiment_counts_births_and_deaths(monkeypatch):
    class StubEnvironment:
        def __init__(self):
            self.food = np.array([[0.5]])
            self.meat = np.zeros((1, 1))
            self.remains = np.zeros((1, 1))

        def regenerate_food(self):
            pass

        def decay_resources(self):
            pass

    class StubOrganism:
        instances = 0

        def __init__(self, _x, _y, species):
            del _x, _y
            self.species = species
            self.alive = True
            self.energy = 200.0
            self.age = 0
            self.generation = 1
            self.instance_id = StubOrganism.instances
            StubOrganism.instances += 1

        def step(self, _environment, _organisms):
            del _environment, _organisms
            if self.instance_id == 0:
                self.alive = False

        def reproduce(self, _mutation_rate):
            del _mutation_rate
            return StubOrganism(0, 0, self.species)

        def calculate_fitness(self):
            return self.energy + self.age

    class StubPredator:
        def __init__(self, _x, _y):
            del _x, _y
            self.alive = True

        def step(self, _prey, _environment):
            del _prey, _environment

    monkeypatch.setattr(runner, "Environment", StubEnvironment)
    monkeypatch.setattr(runner, "Organism", StubOrganism)
    monkeypatch.setattr(runner, "Predator", StubPredator)

    history, _, births, deaths = run_experiment(0.0, steps=1)

    assert history[0]["population"] == 38
    assert sum(births.values()) == 19
    assert deaths["herbivore"] == 1


def test_run_experiment_prints_periodic_species_diagnostics(
    monkeypatch,
    capsys,
):
    class StubEnvironment:
        def __init__(self):
            self.food = np.array([[0.5]])
            self.meat = np.zeros((1, 1))
            self.remains = np.zeros((1, 1))

        def regenerate_food(self):
            pass

        def decay_resources(self):
            pass

    class StubOrganism:
        def __init__(self, _x, _y, species):
            del _x, _y
            self.species = species
            self.alive = True
            self.energy = 100.0
            self.age = 0
            self.generation = 1
            self.last_food_consumed = 0.25
            self.last_food_by_resource = {
                "plant": 0.25,
                "meat": 0.0,
                "remains": 0.0,
            }

        def step(self, _environment, _organisms):
            del _environment, _organisms

        def reproduce(self, _mutation_rate):
            del _mutation_rate
            return None

        def calculate_fitness(self):
            return self.energy

    class StubPredator:
        def __init__(self, _x, _y):
            del _x, _y
            self.alive = True

        def step(self, _prey, _environment):
            del _prey, _environment

    monkeypatch.setattr(runner, "Environment", StubEnvironment)
    monkeypatch.setattr(runner, "Organism", StubOrganism)
    monkeypatch.setattr(runner, "Predator", StubPredator)

    run_experiment(0.0, steps=100)

    output = capsys.readouterr().out
    assert "Step: 100" in output
    assert "herbivore: Count=5" in output
    assert "Food=0.2500" in output
