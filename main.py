"""
MIT License

Copyright (c) 2025 awang104
"""

import dynamics
import simulation
import random

max_mass = 100


def main(n=10, graph=True):
    bodies = []
    for i in range(n):
        b = dynamics.Body(mass=random.random() * max_mass, position=[random.randint(5, 1275), random.randint(5, 715), random.randint(-1000, 1000)], velocity=[random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)])
        bodies.append(b)
    bodies.append(dynamics.Body(mass=2e7, position=(640, 360, 0), velocity=(0, 0, 0)))
    time, energy = simulation.simulate(bodies, bounded=True)
    if graph:
        simulation.energy_plot(time, energy)


if __name__ == '__main__':
    main(50, False)