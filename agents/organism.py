import numpy as np

from core.environment import Environment


class Organism:
    def __init__(self, x: int, y: int) -> None:
        self.x = float(x)
        self.y = float(y)

        self.energy = 100.0
        self.age = 0
        self.alive = True

        self.vision_radius = 5
        self.speed = 1.0

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
