from dataclasses import dataclass, field


@dataclass
class SocialProfile:
    organism_id: int
    dominance: float = 0.5
    rank: int = 0
    group_id: int | None = None
    relationships: dict[int, float] = field(default_factory=dict)

    def update_relationship(self, other_id: int, interaction_score: float):
        current = self.get_relationship(other_id)
        self.relationships[other_id] = max(
            -1.0,
            min(1.0, current + interaction_score)
        )

    def get_relationship(self, other_id: int) -> float:
        return self.relationships.get(other_id, 0.0)

    def adjust_dominance(self, amount: float):
        self.dominance = max(
            0.0,
            min(1.0, self.dominance + amount)
        )