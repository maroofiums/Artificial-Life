from agents.organism import Organism
from agents.species import SPECIES_REGISTRY


class EvaluationTrack:
    def __init__(self) -> None:
        self.generation = 1
        self.history: list[dict[str, int | float | dict[str, int]]] = []


    def record(self, organisms: list[Organism], step: int) -> None:
        fitness = [org.age + org.energy for org in organisms]

        result = {
            "step": step,
            "population": len(organisms),
            "species_counts": {
                species_id: sum(
                    1 for org in organisms
                    if org.species.species_id == species_id
                )
                for species_id in SPECIES_REGISTRY
            },
            "average_fitness": sum(fitness) / len(organisms) if organisms else 0.0,
            "max_fitness": max(fitness, default=0.0),
            "average_age": (
                sum(org.age for org in organisms) / len(organisms)
                if organisms else 0.0
            ),
            "max_generation": max(
                (org.generation for org in organisms),
                default=0,
            ),
            "average_generation": (
                sum(org.generation for org in organisms) / len(organisms)
                if organisms else 0.0
            ),

        }

        self.history.append(result)


    def summary(self) -> dict[str, int | float | dict[str, int]]:
        if not self.history:
            return {}

        return self.history[-1]