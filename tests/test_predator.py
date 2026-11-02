import numpy as np

from agents.predator import Predator
from agents.organism import Organism


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

    predator.step([prey])

    assert prey.alive is False
    assert predator.energy > 120