import numpy as np

from core.environment import Environment
from agents.organism import Organism
from agents.predator import Predator

env = Environment()

prey = [
    Organism(np.random.randint(0, 100),
             np.random.randint(0, 100))
    for _ in range(20)
]

predators = [
    Predator(np.random.randint(0, 100),
             np.random.randint(0, 100))
    for _ in range(3)
]

for step in range(100):

    env.regenerate_food()

    for organism in prey:
        if organism.alive:
            organism.step(env)

    for predator in predators:
        if predator.alive:
            predator.step(prey)

    prey = [p for p in prey if p.alive]
    predators = [p for p in predators if p.alive]

    print(
        f"Step {step + 1} | "
        f"Prey: {len(prey)} | "
        f"Predators: {len(predators)}"
    )
