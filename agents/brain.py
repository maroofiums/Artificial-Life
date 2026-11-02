
import numpy as np


class NeuralBrain:
    def __init__(self) -> None:
        self.W1 = np.random.randn(13, 8) * 0.3
        self.b1 = np.zeros(8)

        self.W2 = np.random.randn(8, 2) * 0.3
        self.b2 = np.zeros(2)

    def forward(
        self,
        observation: np.ndarray,
        energy: float,
    ) -> np.ndarray:

        features = []
        resource_direction = np.zeros(2)

        for resource_map in observation:
            h, w = resource_map.shape

            left = resource_map[:, :w//2].mean()
            right = resource_map[:, w//2:].mean()
            top = resource_map[:h//2, :].mean()
            bottom = resource_map[h//2:, :].mean()

            features.extend([left, right, top, bottom])

            resource_direction += np.array([
                right - left,
                bottom - top
            ])

        features.append(energy / 100)

        features = np.array(features)

        hidden = np.tanh(features @ self.W1 + self.b1)
        neural_direction = np.tanh(hidden @ self.W2 + self.b2)

        # Normalize both directions
        resource_magnitude = np.linalg.norm(resource_direction)
        neural_magnitude = np.linalg.norm(neural_direction)

        if resource_magnitude > 1e-8:
            resource_direction /= resource_magnitude

            if neural_magnitude > 1e-8:
                neural_direction /= neural_magnitude

            # Prioritize resource-seeking over random neural movement
            output = (
                0.8 * resource_direction
                + 0.2 * neural_direction
            )
        else:
            output = neural_direction

        magnitude = np.linalg.norm(output)

        if magnitude > 1e-8:
            output /= magnitude

        return output


    def clone_mutated(
        self, mutation_rate: float = 0.1, mutation_scale: float = 0.1
    ) -> NeuralBrain:
        child = NeuralBrain()

        for name in ("W1", "b1", "W2", "b2"):
            weights = getattr(self, name)

            mask = np.random.random(weights.shape) < mutation_rate
            noise = np.random.randn(*weights.shape) * mutation_scale

            setattr(child, name, weights + mask * noise)

        return child