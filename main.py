import numpy as np

from agents.brain import NeuralBrain
from agents.organism import Organism
from agents.predator import Predator
from core.environment import Environment
from experiments.evolution import EvaluationTrack
from visualization.dashboard import plot_evolution
from experiments.validation import validate_population

MAX_POPULATION = 100
SIMULATION_STEPS = 500
PREDATOR_COUNT = 3
MUTATION_RATE = 0.1

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
    predators = [
        Predator(
            x=int(np.random.randint(0, environment.width)),
            y=int(np.random.randint(0, environment.height)),
        )
        for _ in range(PREDATOR_COUNT)
    ]
    tracker = EvaluationTrack()

    for step in range(SIMULATION_STEPS):
        environment.regenerate_food()

        for organism in prey:
            if organism.alive:
                organism.step(environment)

        newborns = []

        for organism in prey:
            if organism.alive:
                child = organism.reproduce(mutation_rate=MUTATION_RATE)

                if child is not None:
                    newborns.append(child)

        prey.extend(newborns)

        prey = [
            organism for organism in prey
            if organism.alive and organism.energy > 0
        ]

        prey.sort(
            key=lambda organism: organism.calculate_fitness(),
            reverse=True,
        )
        prey = prey[:MAX_POPULATION]

        for predator in predators:
            if predator.alive:
                predator.step(prey, environment)

        predators = [predator for predator in predators if predator.alive]
        prey = [
            organism for organism in prey
            if organism.alive and organism.energy > 0
        ]

        tracker.record(prey, step + 1, environment)

        if (step + 1) % 50 == 0:
            max_generation = max(
                (organism.generation for organism in prey),
                default=0,
            )
            print(
                f"Step: {step + 1} | "
                f"Population: {len(prey)} | "
                f"Generation: {max_generation}"
            )

    validate_population(tracker.history)

    plot_evolution(tracker.history)

if __name__ == "__main__":
    main()
    