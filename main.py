import numpy as np
from agents.brain import NeuralBrain

brain = NeuralBrain()

observation = np.random.rand(11, 11)

action = brain.forward(observation, 100)

print("Movement:", action)
print("Direction magnitude:", np.linalg.norm(action))