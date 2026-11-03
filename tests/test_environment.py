import numpy as np
import pytest

from core.environment import Environment


def test_environment_initialization():
    env = Environment(width=100, height=100)

    assert env.food.shape == (100, 100)
    assert np.all(env.food >= 0)
    assert np.all(env.food <= 1)


def test_food_consumption():
    env = Environment(width=10, height=10)

    env.food[5, 5] = 0.8

    consumed = env.consume_food(5, 5, amount=0.2)

    assert np.isclose(consumed, 0.2)
    assert np.isclose(env.food[5, 5], 0.6)


def test_food_observation():
    env = Environment(width=20, height=20)

    observation = env.observe(10, 10, radius=3)

    assert observation.shape == (7, 7)


def test_observation_is_clipped_at_environment_edges():
    env = Environment(width=8, height=6)

    observation = env.observe(0, 0, radius=2)

    assert observation.shape == (3, 3)
    np.testing.assert_array_equal(observation, env.food[:3, :3])


def test_food_regeneration_stays_within_resource_limits():
    env = Environment(width=10, height=10)
    env.food.fill(0.99)

    env.regenerate_food()

    assert np.all(env.food >= 0)
    assert np.all(env.food <= 1)


def test_animal_resources_decay():
    env = Environment(width=4, height=4)
    env.meat.fill(0.8)
    env.remains.fill(0.4)

    env.decay_resources()

    np.testing.assert_allclose(env.meat, 0.8 * 0.995)
    np.testing.assert_allclose(env.remains, 0.4 * 0.995)


def test_add_resource_caps_amount_and_rejects_plant():
    env = Environment(width=4, height=4)
    env.meat[1, 2] = 0.8

    env.add_resource(2, 1, "meat", 0.5)

    assert env.meat[1, 2] == 1.0
    with pytest.raises(ValueError, match="Unknown resource"):
        env.add_resource(2, 1, "plant", 0.2)


def test_consume_resource_caps_at_available_amount_and_rejects_unknown():
    env = Environment(width=4, height=4)
    env.remains[1, 2] = 0.1

    consumed = env.consume_resource(2, 1, "remains", amount=0.2)

    assert consumed == 0.1
    assert env.remains[1, 2] == 0
    with pytest.raises(ValueError, match="Unknown resource"):
        env.consume_resource(2, 1, "unknown")


def test_observe_resources_includes_only_diet_resources():
    env = Environment(width=5, height=5)
    env.food[2, 2] = 0.8
    env.meat[2, 2] = 0.6
    env.remains[2, 2] = 0.4

    maps = env.observe_resources(2, 2, radius=1, diet=("meat",))

    assert maps.shape == (3, 3, 3)
    assert maps[0, 1, 1] == 0
    assert maps[1, 1, 1] == 0.6
    assert maps[2, 1, 1] == 0