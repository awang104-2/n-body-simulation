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
    for i in range(10):
        bodies.append(dynamics.Body(1 / constants.G, (random.random() * 1280, random.random() * 720, 0), (random.random() * 100, random.random() * 100, 0)))
    bodies.append(dynamics.Body(1e7 / constants.G, (690, 360, 0)))
    system = dynamics.system(bodies)
    simulation.simulate(system, dynamics.rk4)


if __name__ == '__main__':
    main(3)

