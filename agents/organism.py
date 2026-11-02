import numpy as np

from core.environment import Environment
from agents.brain import NeuralBrain
from agents.species import SPECIES_REGISTRY, Species, get_species


class Organism:
    def __init__(
        self,
        x: int,
        y: int,
        brain: NeuralBrain | None = None,
        species: Species | str | None = None,
    ) -> None:
        self.x: float = float(x)
        self.y: float = float(y)

        if isinstance(species, str):
            self.species = get_species(species)
        else:
            self.species = species or SPECIES_REGISTRY["herbivore"]

        self.energy: float = self.species.starting_energy
        self.age: int = 0
        self.alive: bool = True

        self.vision_radius: int = self.species.vision_radius
        self.speed: float = self.species.speed

        self.brain: NeuralBrain | None = (
            brain if brain is not None else NeuralBrain()
        )
        self.generation: int = 1

    def perceive(
        self, environment: Environment
    ) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        return environment.observe(
            int(self.x),
            int(self.y),
            self.vision_radius
        )

    def decide(
        self, observation: np.ndarray[tuple[int, int], np.dtype[np.float64]]
    ) -> np.ndarray[tuple[int], np.dtype[np.float64]]:

        return self.brain.forward(observation, self.energy)

    def act(
        self,
        direction: np.ndarray[tuple[int], np.dtype[np.float64]],
        environment: Environment,
    ) -> None:
        self.x = np.clip(
            self.x + direction[0] * self.speed,
            0, environment.width - 1
        )

        self.y = np.clip(
            self.y + direction[1] * self.speed,
            0, environment.height - 1
        )

        consumed = environment.consume_food(
            int(self.x),
            int(self.y)
          )

        self.energy += consumed * self.species.food_gain
        self.energy -= 0.5

        self.age += 1

        if self.energy <= 0:
            self.alive = False

    def step(self, environment: Environment) -> None:
        observation = self.perceive(environment)
        direction = self.decide(observation)
        self.act(direction, environment)

    def reproduce(self, mutation_rate=0.1):
        if self.energy < self.species.reproduction_energy or not self.alive:
            return None

        self.energy -= self.species.reproduction_energy

        child_brain = self.brain.clone_mutated(
            mutation_rate=mutation_rate,
            mutation_scale=0.1
        )

        child = Organism(
            self.x,
            self.y,
            brain=child_brain,
            species=self.species
        )

        child.energy = 60
        child.generation = self.generation + 1

        return child

    def calculate_fitness(self) -> float:
        return self.age + self.energy