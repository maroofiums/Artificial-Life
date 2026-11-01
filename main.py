import numpy as np

from agents.brain import NeuralBrain
from agents.organism import Organism
from core.environment import Environment
from experiments.evolution import EvaluationTrack
from visualization.dashboard import plot_evolution

def main() -> None:
    environment = Environment()
    prey = [
        Organism(
            x=int(np.random.randint(0, environment.width)),
            y=int(np.random.randint(0, environment.height)),
            brain=NeuralBrain(),
        )
        for _ in range(20)
    ]
    tracker = EvaluationTrack()

    for step in range(100):
        environment.regenerate_food()

        for organism in prey:
            if organism.alive:
                organism.step(environment)

        prey = [organism for organism in prey if organism.alive]

        newborns = []

        for organism in prey:
            child = organism.reproduce()

            if child is not None:
                newborns.append(child)

        prey.extend(newborns)

        tracker.record(prey, step + 1)

        if (step + 1) % 10 == 0:
            print("Evolution:", tracker.summary())

    plot_evolution(tracker.history)

if __name__ == "__main__":
    main()
    