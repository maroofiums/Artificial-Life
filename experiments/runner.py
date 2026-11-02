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

    births = {sid: 0 for sid in SPECIES_REGISTRY}
    deaths = {sid: 0 for sid in SPECIES_REGISTRY}
    
    max_population = 100

    for step in range(steps):
        env.regenerate_food()
        
        for organism in prey:
            if organism.alive:
                organism.step(env, prey)

        newborns = []

        for organism in prey:
            if organism.alive:
                child = organism.reproduce(mutation_rate)

                if child is not None:
                    newborns.append(child)
                    births[organism.species.species_id] += 1

        prey.extend(newborns)

        dead = [
            org for org in prey
            if not org.alive or org.energy <= 0
        ]

        for org in dead:
            deaths[org.species.species_id] += 1

        prey = [
            org for org in prey
            if org.alive and org.energy > 0
        ]

        prey.sort(
            key=lambda org: org.calculate_fitness(),
            reverse=True
        )

        removed = prey[max_population:]

        for org in removed:
            deaths[org.species.species_id] += 1

        prey = prey[:max_population]

        for predator in predators:
            if predator.alive:
                predator.step(prey, env)

        predator_kills = [
            org for org in prey
            if not org.alive or org.energy <= 0
        ]

        for org in predator_kills:
            deaths[org.species.species_id] += 1

        prey = [
            org for org in prey
            if org.alive and org.energy > 0
        ]
        
        predators = [p for p in predators if p.alive]

        tracker.record(prey, step + 1)

    tracker.final_resources = {
        "plant": float(env.food.mean()),
        "meat": float(env.meat.mean()),
        "remains": float(env.remains.mean()),
    }

    tracker.births = births
    tracker.deaths = deaths

    return tracker.history, tracker.final_resources, tracker.births, tracker.deaths        