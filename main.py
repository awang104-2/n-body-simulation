"""
MIT License

Copyright (c) 2025 awang104
"""

import dynamics
import simulation


def main():
    bodies = []
    bodies.append(dynamics.Body(mass=1, position=(340, 360, 0), velocity=(0, 258, 0)))
    bodies.append(dynamics.Body(mass=2e7, position=(640, 360, 0), velocity=(0, 0, 0)))
    time, energy = simulation.simulate(bodies)
    simulation.energy_plot(time, energy)


if __name__ == '__main__':
    main()