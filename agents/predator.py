
import numpy as np

from agents.organism import Organism


class Predator:
    def __init__(self, x: int, y: int) -> None:
        self.x: float = float(x)
        self.y: float = float(y)

        self.energy: float = 120.0
        self.speed: float = 1.5
        self.vision_radius: int = 12

        self.alive: bool = True
        self.age: int = 0

    def perceive(
        self, organisms: list[Organism]
    ) -> list[tuple[float, Organism]]:
        visible = []

        for prey in organisms:
            if not prey.alive:
                continue

            distance = np.hypot(
                prey.x - self.x,
                prey.y - self.y
            )

            if distance <= self.vision_radius:
                visible.append((distance, prey))

        return visible

    def decide(
        self, visible: list[tuple[float, Organism]]
    ) -> np.ndarray[tuple[int], np.dtype[np.float64]]:
        if not visible:
            return np.random.uniform(-1, 1, 2)

        _, target = min(visible, key=lambda item: item[0])

        direction = np.array([
            target.x - self.x,
            target.y - self.y
        ])

        magnitude = np.linalg.norm(direction)

        return direction / magnitude if magnitude > 0 else direction

    def act(
        self,
        direction: np.ndarray[tuple[int], np.dtype[np.float64]],
        organisms: list[Organism],
        environment,
    ) -> None:
        self.x += direction[0] * self.speed
        self.y += direction[1] * self.speed

        self.energy -= 1.5
        self.age += 1

        for prey in organisms:
            if not prey.alive:
                continue

            distance = np.hypot(
                prey.x - self.x,
                prey.y - self.y
            )

            if distance < 2:
                prey.alive = False
                environment.add_resource(
                    int(prey.x),
                    int(prey.y),
                    "meat",
                    1.0
                )
                self.energy += 40
                break

        if self.energy <= 0:
            self.alive = False

    def step(self, organisms: list[Organism], environment) -> None:
        visible = self.perceive(organisms)
        direction = self.decide(visible)
        self.act(direction, organisms, environment)
