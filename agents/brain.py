
import numpy as np


class NeuralBrain:
    def __init__(self):
        self.W1 = np.random.randn(5, 8) * 0.3
        self.b1 = np.zeros(8)

        self.W2 = np.random.randn(8, 2) * 0.3
        self.b2 = np.zeros(2)

    def forward(self, observation, energy):

        h, w = observation.shape

        features = np.array([
            observation[:, :w//2].mean(),
            observation[:, w//2:].mean(),
            observation[:h//2, :].mean(),
            observation[h//2:, :].mean(),
            energy / 100
        ])

        hidden = np.tanh(features @ self.W1 + self.b1)

        output = np.tanh(hidden @ self.W2 + self.b2)

        magnitude = np.linalg.norm(output)

        if magnitude > 0:
            output /= magnitude

        return output
