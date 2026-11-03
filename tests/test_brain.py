import numpy as np

from agents.brain import NeuralBrain


def test_forward_prioritizes_resource_direction():
    brain = NeuralBrain()
    brain.W1.fill(0)
    brain.b1.fill(0)
    brain.W2.fill(0)
    brain.b2.fill(0)

    observation = np.zeros((3, 4, 4))
    observation[0, :, 2:] = 1.0

    direction = brain.forward(observation, energy=100)

    np.testing.assert_allclose(direction, [1.0, 0.0])


def test_forward_returns_neural_direction_when_resources_are_absent():
    brain = NeuralBrain()
    brain.W1.fill(0)
    brain.b1.fill(0)
    brain.W2.fill(0)
    brain.b2[:] = [0.2, -0.1]

    direction = brain.forward(np.zeros((3, 4, 4)), energy=100)

    assert np.isclose(np.linalg.norm(direction), 1.0)
    assert direction[0] > 0
    assert direction[1] < 0


def test_mutation_rate_zero_clones_weights_without_sharing_arrays():
    np.random.seed(0)
    parent = NeuralBrain()

    child = parent.clone_mutated(mutation_rate=0.0, mutation_scale=1.0)

    for name in ("W1", "b1", "W2", "b2"):
        parent_weights = getattr(parent, name)
        child_weights = getattr(child, name)
        np.testing.assert_array_equal(child_weights, parent_weights)
        assert child_weights is not parent_weights


def test_mutation_rate_one_changes_all_weight_arrays():
    np.random.seed(1)
    parent = NeuralBrain()

    child = parent.clone_mutated(mutation_rate=1.0, mutation_scale=0.1)

    for name in ("W1", "b1", "W2", "b2"):
        assert not np.array_equal(getattr(child, name), getattr(parent, name))
