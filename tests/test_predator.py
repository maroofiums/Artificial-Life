import numpy as np

from agents.predator import Predator
from agents.organism import Organism
from core.environment import Environment


def test_predator_initialization():
    predator = Predator(10, 20)

    assert predator.alive is True
    assert predator.energy == 120
    assert predator.speed == 1.5


def test_predator_detects_nearby_prey():
    predator = Predator(10, 10)
    prey = Organism(12, 10)

    visible = predator.perceive([prey])

    assert visible == [(2.0, prey)]


def test_predator_ignores_dead_and_out_of_range_prey():
    predator = Predator(10, 10)
    dead_prey = Organism(11, 10)
    dead_prey.alive = False
    distant_prey = Organism(30, 30)

    assert predator.perceive([dead_prey, distant_prey]) == []


def test_predator_decides_toward_nearest_visible_prey():
    predator = Predator(10, 10)
    visible = [
        (4.0, Organism(10, 14)),
        (2.0, Organism(12, 10)),
    ]

    direction = predator.decide(visible)

    np.testing.assert_allclose(direction, [1.0, 0.0])


def test_predator_random_direction_is_bounded_when_no_prey_is_visible():
    predator = Predator(10, 10)

    direction = predator.decide([])

    assert direction.shape == (2,)
    assert np.all(direction >= -1)
    assert np.all(direction <= 1)


def test_predator_hunts_prey():
    predator = Predator(10, 10)
    prey = Organism(11, 10)
    environment = Environment(width=100, height=100)

    predator.step([prey], environment)

    assert prey.alive is False
    assert predator.energy > 120
    assert environment.meat[10, 11] == 1.0


def test_predator_step_ages_and_loses_energy_without_prey():
    predator = Predator(10, 10)
    environment = Environment(width=100, height=100)

    predator.step([], environment)

    assert predator.age == 1
    assert predator.energy == 118.5