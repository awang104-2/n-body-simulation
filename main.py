"""
MIT License

Copyright (c) 2025 awang104
"""

import dynamics
import simulation


def test_function(x=0, y=0, z=0):
    print(x, y, z)


if __name__ == '__main__':
    bodies = []
    for i in range(3):
        bodies.append(dynamics.Body(position=(i, 1, 1)))
    for body in bodies:
        print(body)