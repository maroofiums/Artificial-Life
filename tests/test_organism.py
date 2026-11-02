import numpy as np

from agents.organism import Organism
from agents.species import SPECIES_REGISTRY
from core.environment import Environment


def test_organism_initialization():
    organism = Organism(10, 20)

    assert organism.alive is True
    assert organism.energy > 0
    assert organism.age == 0


def test_organism_initialization_with_species():
    carnivore = SPECIES_REGISTRY["carnivore"]

    organism = Organism(10, 20, species=carnivore)
    organism_from_id = Organism(10, 20, species="carnivore")

    assert organism.species is carnivore
    assert organism.energy == carnivore.starting_energy
    assert organism.vision_radius == carnivore.vision_radius
    assert organism.speed == carnivore.speed
    assert organism_from_id.species is carnivore

    organism.energy = 200
    child = organism.reproduce()

    assert child is not None
    assert child.species is carnivore
    assert child.generation == organism.generation + 1
    assert child.energy == 60


def test_organism_reproduction():
    parent = Organism(10, 20)
    parent.energy = 200

    child = parent.reproduce(mutation_rate=0.1)

    assert child is not None
    assert child.generation == parent.generation + 1
    assert parent.energy == 140
    assert child.energy == 60


def test_organism_dies_when_energy_depleted():
    organism = Organism(10, 20)
    organism.energy = 0.5

    env = Environment(width=100, height=100)
    env.food[:] = 0

    organism.step(env)

    assert organism.alive is False