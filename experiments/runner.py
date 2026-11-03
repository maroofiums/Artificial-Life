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
        env.decay_resources()
        
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
        if (step + 1) % 100 == 0:
            print(f"\nStep: {step + 1}")

            for species_id in SPECIES_REGISTRY:
                members = [
                    org for org in prey
                    if org.species.species_id == species_id
                ]

                avg_energy = (
                    np.mean([org.energy for org in members])
                    if members else 0
                )

                avg_food = (
                    np.mean([org.last_food_consumed for org in members])
                    if members else 0
                )

                avg_resources = {
                    resource: np.mean([
                        org.last_food_by_resource[resource]
                        for org in members
                    ]) if members else 0.0
                    for resource in ("plant", "meat", "remains")
                }

                print(
                    f"{species_id}: "
                    f"Count={len(members)}, "
                    f"Energy={avg_energy:.2f}, "
                    f"Food={avg_food:.4f}, "
                    f"Plant={avg_resources['plant']:.4f}, "
                    f"Meat={avg_resources['meat']:.4f}, "
                    f"Remains={avg_resources['remains']:.4f}"
                )
        tracker.record(prey, step + 1, env)

    tracker.final_resources = {
        "plant": float(env.food.mean()),
        "meat": float(env.meat.mean()),
        "remains": float(env.remains.mean()),
    }

    tracker.births = births
    tracker.deaths = deaths

    return tracker.history, tracker.final_resources, tracker.births, tracker.deaths        