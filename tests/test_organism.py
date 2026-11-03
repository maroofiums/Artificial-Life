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
    assert parent.energy == 200 - parent.species.reproduction_energy
    assert child.energy == 60


def test_organism_movement_uses_integer_coordinates_and_clamps_to_bounds():
    organism = Organism(98, 1)
    environment = Environment(width=100, height=100)
    direction = np.array([1.0, -1.0])

    organism.act(direction, environment)

    assert organism.x == 99
    assert organism.y == 0
    assert isinstance(organism.x, int)
    assert isinstance(organism.y, int)


def test_organism_tracks_consumption_by_resource():
    organism = Organism(5, 5, species="omnivore")
    environment = Environment(width=10, height=10)
    environment.food[5, 5] = 0.5
    environment.meat[5, 5] = 0.4
    environment.remains[5, 5] = 0.3
    initial_energy = organism.energy

    organism.act(np.array([0.0, 0.0]), environment)

    assert organism.last_food_consumed == 0.4
    assert organism.last_food_by_resource == {
        "plant": 0.2,
        "meat": 0.2,
        "remains": 0.0,
    }
    assert organism.food_consumed == 0.4
    assert np.isclose(
        organism.energy,
        initial_energy + 0.4 * organism.species.food_gain - 0.5,
    )
    assert np.isclose(environment.food[5, 5], 0.3)
    assert np.isclose(environment.meat[5, 5], 0.2)
    assert np.isclose(environment.remains[5, 5], 0.3)


def test_organism_dies_when_energy_depleted():
    organism = Organism(10, 20)
    organism.energy = 0.5

    env = Environment(width=100, height=100)
    env.food[:] = 0

    organism.step(env)

    assert organism.alive is False


def test_perception_masks_resources_outside_species_diet():
    organism = Organism(5, 5, species="herbivore")
    environment = Environment(width=10, height=10)
    environment.food[5, 5] = 0.8
    environment.meat[5, 5] = 0.6
    environment.remains[5, 5] = 0.4

    observation = organism.perceive(environment)

    assert observation.shape == (3, 10, 10)
    assert observation[0, 5, 5] == 0.8
    assert observation[1, 5, 5] == 0
    assert observation[2, 5, 5] == 0


def test_carnivore_hunts_other_species_and_tracks_meat():
    carnivore = Organism(5, 5, species="carnivore")
    prey = Organism(6, 5, species="herbivore")
    environment = Environment(width=10, height=10)
    initial_energy = carnivore.energy

    carnivore.hunt([carnivore, prey], environment)

    assert prey.alive is False
    assert environment.meat[5, 6] == 0.8
    assert carnivore.last_food_by_resource["meat"] == 0.2
    assert carnivore.last_food_consumed == 0.2
    assert carnivore.food_consumed == 0.2
    assert carnivore.energy == initial_energy + 0.2 * carnivore.species.food_gain + 10


def test_hunt_skips_same_species_and_non_attacking_species():
    herbivore = Organism(5, 5, species="herbivore")
    same_species = Organism(6, 5, species="herbivore")
    environment = Environment(width=10, height=10)
    initial_energy = herbivore.energy

    herbivore.hunt([same_species], environment)

    assert same_species.alive is True
    assert herbivore.energy == initial_energy


def test_step_runs_movement_and_hunting():
    hunter = Organism(5, 5, species="carnivore")
    prey = Organism(6, 5, species="herbivore")
    environment = Environment(width=10, height=10)
    hunter.brain.forward = lambda observation, energy: (
        np.zeros(2) + observation.sum() * 0 + energy * 0
    )

    hunter.step(environment, [hunter, prey])

    assert hunter.age == 1
    assert prey.alive is False
    assert environment.meat[5, 6] > 0


def test_scavenger_consumes_meat_and_remains_separately():
    scavenger = Organism(5, 5, species="scavenger")
    environment = Environment(width=10, height=10)
    environment.meat[5, 5] = 0.1
    environment.remains[5, 5] = 0.5

    scavenger.act(np.zeros(2), environment)

    assert scavenger.last_food_by_resource == {
        "plant": 0.0,
        "meat": 0.1,
        "remains": 0.2,
    }
    assert np.isclose(scavenger.last_food_consumed, 0.3)
    assert np.isclose(environment.meat[5, 5], 0)
    assert np.isclose(environment.remains[5, 5], 0.3)


def test_dead_organism_is_not_reproduced():
    organism = Organism(5, 5)
    organism.energy = 200
    organism.alive = False

    assert organism.reproduce() is None


def test_organism_below_species_reproduction_threshold_is_not_reproduced():
    organism = Organism(5, 5, species="carnivore")
    organism.energy = organism.species.reproduction_energy - 0.1

    assert organism.reproduce() is None


def test_fitness_is_age_plus_energy():
    organism = Organism(5, 5)
    organism.age = 12
    organism.energy = 34.5

    assert organism.calculate_fitness() == 46.5