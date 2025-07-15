"""
MIT License

Copyright (c) 2025 awang104
"""

from nbp import dynamics
from nbp import simulation
from nbp import constants
import random


max_mass = 100
constants.G = 1


def main(n):
    bodies = []
    for i in range(n):
        body = dynamics.Body(
            random.randint(1, 20),
            (random.random() * 1280, random.random() * 720, 0),
            (random.random() * 200 - 100, random.random() * 200 - 100, 0)
        )
        bodies.append(body)
    body = dynamics.Body(
        1e7,
        (690, 360, 0),
        (0, 0, 0)
    )
    bodies.append(body)
    system = dynamics.system(bodies)
    simulation.simulate(system, dynamics.rkf4)


if __name__ == '__main__':
    main(3)

