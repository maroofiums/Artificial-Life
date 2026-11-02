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

    assert len(visible) == 1


def test_predator_hunts_prey():
    predator = Predator(10, 10)
    prey = Organism(11, 10)
    environment = Environment(width=100, height=100)

    predator.step([prey], environment)

    assert prey.alive is False
    assert predator.energy > 120