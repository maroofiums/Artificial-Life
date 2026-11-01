import numpy as np

from core.environment import Environment
from agents.brain import NeuralBrain
class Organism:
    def __init__(self, x: int, y: int, brain: NeuralBrain=None) -> None:
        self.x: float = float(x)
        self.y: float = float(y)

        self.energy: float = 100.0
        self.age: int = 0
        self.alive: bool = True

        self.vision_radius: int = 5
        self.speed: float = 1.0

        self.brain: NeuralBrain | None = brain if brain is not None else None

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
        if observation.max() <= 0.05:
            return np.random.uniform(-1, 1, 2)

        target_y, target_x = np.unravel_index(
            np.argmax(observation),
            observation.shape
        )

        center = self.vision_radius

        direction = np.array([
            target_x - center,
            target_y - center
        ], dtype=float)

        magnitude = np.linalg.norm(direction)

        if magnitude > 0:
            direction /= magnitude

        return direction

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

        self.energy += consumed * 50
        self.energy -= 1.0

        self.age += 1

        if self.energy <= 0:
            self.alive = False

    def step(self, environment: Environment) -> None:
        observation = self.perceive(environment)
        direction = self.decide(observation)
        self.act(direction, environment)

    def reproduce(self) -> Organism | None:
        if self.energy < 150:
            return None

        self.energy -= 60

        child_brain = self.brain.clone_mutated()

        child = Organism(
            x = self.x,
            y = self.y,
            brain = child_brain
        )

        child.energy = 60

        return child
