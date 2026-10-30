import numpy as np
from scipy.ndimage import gaussian_filter


class Environment:
    def __init__(self, width=100, height=100):
        self.width = width
        self.height = height

        self.food = np.random.rand(height, width)
        self.food = gaussian_filter(self.food, sigma=3)

        self.food /= self.food.max()

    def regenerate_food(self):
        growth = np.random.uniform(
            0, 0.01, self.food.shape
        )

        self.food = np.clip(
            self.food + growth, 0, 1
        )

    def observe(self, x, y, radius=5):
        x_min = max(0, x - radius)
        x_max = max(self.width, x + radius + 1)

        y_min = max(0, y - radius)
        y_max = max(self.height, y + radius + 1)

        return self.food[y_min:y_max, x_min:x_max]


    def consume_food(self, x, y, amount=0.2):
        available = self.food[y, x]
        consumed = min(available, amount)

        self.food[y, x] -= consumed

        return consumed