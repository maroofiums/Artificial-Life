from agents.organism import Organism
from agents.species import SPECIES_REGISTRY
from core.environment import Environment
from experiments.evolution import EvaluationTrack, extinction_report


def test_record_stores_population_species_fitness_generations_and_resources():
    herbivore = Organism(1, 1)
    herbivore.age = 2
    herbivore.energy = 20
    herbivore.generation = 3
    carnivore = Organism(2, 2, species="carnivore")
    carnivore.age = 4
    carnivore.energy = 30
    carnivore.generation = 5

    environment = Environment(width=2, height=2)
    environment.food.fill(0.5)
    environment.meat.fill(0.25)
    environment.remains.fill(0.1)

    tracker = EvaluationTrack()
    tracker.record([herbivore, carnivore], step=7, environment=environment)
    result = tracker.summary()

    assert result["step"] == 7
    assert result["population"] == 2
    assert result["species_counts"]["herbivore"] == 1
    assert result["species_counts"]["carnivore"] == 1
    assert result["species_counts"]["omnivore"] == 0
    assert result["average_fitness"] == 28
    assert result["max_fitness"] == 34
    assert result["average_age"] == 3
    assert result["max_generation"] == 5
    assert result["average_generation"] == 4
    assert result["resources"] == {
        "plant": 0.5,
        "meat": 0.25,
        "remains": 0.1,
    }


def test_empty_record_has_zero_metrics_and_registered_species_counts():
    tracker = EvaluationTrack()

    tracker.record([], step=1)

    assert tracker.summary()["population"] == 0
    assert tracker.summary()["average_fitness"] == 0
    assert tracker.summary()["max_fitness"] == 0
    assert tracker.summary()["species_counts"] == {
        species_id: 0 for species_id in SPECIES_REGISTRY
    }
    assert tracker.summary()["resources"] == {
        "plant": 0,
        "meat": 0,
        "remains": 0,
    }


def test_summary_returns_empty_mapping_before_any_records():
    assert EvaluationTrack().summary() == {}


def test_extinction_report_finds_first_zero_population_step():
    history = [
        {
            "step": 1,
            "species_counts": {"herbivore": 2, "carnivore": 1},
        },
        {
            "step": 2,
            "species_counts": {"herbivore": 1, "carnivore": 0},
        },
        {
            "step": 3,
            "species_counts": {"herbivore": 0, "carnivore": 0},
        },
    ]

    assert extinction_report(history) == {
        "herbivore": "Extinct at step 3",
        "carnivore": "Extinct at step 2",
    }


def test_extinction_report_handles_empty_history_and_survivors():
    assert extinction_report([]) == {}
    assert extinction_report([
        {"step": 1, "species_counts": {"herbivore": 1}},
        {"step": 2, "species_counts": {"herbivore": 2}},
    ]) == {"herbivore": "Survived"}
