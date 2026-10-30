from core.environment import Environment
from agents.organism import Organism

env = Environment()

organism = Organism(50, 50)

for step in range(20):
    organism.step(env)

    print(
        f"Step: {step + 1} | "
        f"Position: ({organism.x:.2f}, {organism.y:.2f}) | "
        f"Energy: {organism.energy:.2f}"
    )

    if not organism.alive:
        print("Organism died!")
        break
