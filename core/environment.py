import numpy as np
from scipy.ndimage import gaussian_filter


class Environment:
    def __init__(self, width: int = 100, height: int = 100) -> None:
        self.width = width
        self.height = height

        self.food: np.ndarray[
            tuple[int, int], np.dtype[np.float64]
        ] = np.random.rand(height, width)
        self.food = gaussian_filter(self.food, sigma=3)

        self.food /= self.food.max()

    def regenerate_food(self) -> None:
        growth = np.random.uniform(
            0, 0.01, self.food.shape
        )

        self.food = np.clip(
            self.food + growth, 0, 1
        )

    def observe(
        self, x: int, y: int, radius: int = 5
    ) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        x_min = max(0, x - radius)
        x_max = max(self.width, x + radius + 1)

        y_min = max(0, y - radius)
        y_max = max(self.height, y + radius + 1)

        return self.food[y_min:y_max, x_min:x_max]


    def consume_food(self, x: int, y: int, amount: float = 0.2) -> float:
        available = self.food[y, x]
        consumed = min(available, amount)

        self.food[y, x] -= consumed

        return consumed