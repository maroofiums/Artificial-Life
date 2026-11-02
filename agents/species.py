from dataclasses import dataclass


@dataclass(frozen=True)
class Species:
    species_id: str
    name: str
    diet: tuple
    speed: float
    vision_radius: int
    starting_energy: float
    reproduction_energy: float
    food_gain: float
    attack_strength: float


SPECIES_REGISTRY = {

    "herbivore": Species(
        species_id="herbivore",
        name="Herbivore",
        diet=("plant",),
        speed=1.0,
        vision_radius=8,
        starting_energy=100.0,
        reproduction_energy=150.0,
        food_gain=50.0,
        attack_strength=0.0
    ),

    "carnivore": Species(
        species_id="carnivore",
        name="Carnivore",
        diet=("meat",),
        speed=1.5,
        vision_radius=12,
        starting_energy=120.0,
        reproduction_energy=180.0,
        food_gain=70.0,
        attack_strength=10.0
    ),

    "omnivore": Species(
        species_id="omnivore",
        name="Omnivore",
        diet=("plant", "meat"),
        speed=1.2,
        vision_radius=10,
        starting_energy=110.0,
        reproduction_energy=160.0,
        food_gain=55.0,
        attack_strength=5.0
    ),

    "scavenger": Species(
        species_id="scavenger",
        name="Scavenger",
        diet=("meat", "remains"),
        speed=0.9,
        vision_radius=14,
        starting_energy=100.0,
        reproduction_energy=150.0,
        food_gain=60.0,
        attack_strength=0.0
    )
}


def get_species(species_id: str) -> Species:
    if species_id not in SPECIES_REGISTRY:
        raise ValueError(f"Unknown species: {species_id}")

    return SPECIES_REGISTRY[species_id]