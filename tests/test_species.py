import pytest

from agents.species import SPECIES_REGISTRY, Species, get_species


def test_registry_contains_expected_species_and_diets():
    assert set(SPECIES_REGISTRY) == {
        "herbivore",
        "carnivore",
        "omnivore",
        "scavenger",
    }
    assert get_species("herbivore").diet == ("plant",)
    assert get_species("carnivore").diet == ("meat",)
    assert get_species("omnivore").diet == ("plant", "meat")
    assert get_species("scavenger").diet == ("meat", "remains")


def test_get_species_rejects_unknown_id():
    with pytest.raises(ValueError, match="Unknown species"):
        get_species("unknown")


def test_species_is_immutable():
    species = SPECIES_REGISTRY["herbivore"]

    with pytest.raises(AttributeError):
        species.speed = 2.0

    assert isinstance(species, Species)
