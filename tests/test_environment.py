import numpy as np
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