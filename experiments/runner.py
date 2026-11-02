import numpy as np

from core.environment import Environment
from agents.organism import Organism
from agents.predator import Predator
from experiments.evolution import EvaluationTrack
from agents.species import SPECIES_REGISTRY


def run_experiment(mutation_rate, seed=42, steps=500):

    np.random.seed(seed)

    env = Environment()

    species_types = list(SPECIES_REGISTRY.values())

    prey = [
        Organism(
            np.random.randint(0, 100),
            np.random.randint(0, 100),
            species=species_types[i % len(species_types)]
        )
        for i in range(20)
    ]

    predators = [
        Predator(
            np.random.randint(0, 100),
            np.random.randint(0, 100)
        )
        for _ in range(3)
    ]

    tracker = EvaluationTrack()
    max_population = 100

    for step in range(steps):
        env.regenerate_food()

        for organism in prey:
            if organism.alive:
                organism.step(env)

        newborns = []

        for organism in prey:
            if organism.alive:
                child = organism.reproduce(mutation_rate)

                if child is not None:
                    newborns.append(child)

        prey.extend(newborns)

        prey = [
            org for org in prey
            if org.alive and org.energy > 0
        ]

        prey.sort(
            key=lambda org: org.calculate_fitness(),
            reverse=True
        )

        prey = prey[:max_population]

        for predator in predators:
            if predator.alive:
                predator.step(prey, env)

        predators = [p for p in predators if p.alive]

        species_counts = {
            species_id: sum(
                1 for org in prey
                if org.species.species_id == species_id
            )
            for species_id in SPECIES_REGISTRY
        }

        tracker.record(prey, step + 1)

    return tracker.history        
        