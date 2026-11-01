from agents.organism import Organism


class EvaluationTrack:
    def __init__(self) -> None:
        self.generation = 1
        self.history: list[dict[str, int | float]] = []


    def record(self, organisms: list[Organism], step: int) -> None:
        if not organisms:
            return
    
        fitness = [org.age + org.energy for org in organisms]


        result = {
            "step": step,
            "population": len(organisms),
            "average_fitness": sum(fitness) / len(fitness),
            "max_fitness": max(fitness),
            "average_age": sum(org.age for org in organisms) / len(organisms),
        }

        self.history.append(result)


    def summary(self) -> dict[str, int | float]:
        if not self.history:
            return {}

        return self.history[-1]