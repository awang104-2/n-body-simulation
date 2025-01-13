from dynamics import *
import numpy as np
import matplotlib.pyplot as plt


def randomly_define_nbody(N):
    bodies = []
    for _ in range(N):
        mass, position = (np.random.rand(), -10 + np.random.rand(3) * 20)
        bodies.append(define_body(mass, position))
    return bodies


def main():
    N = 100
    nbody = randomly_define_nbody(N)
    print('original\n', nbody)
    nbody = leapfrog(nbody, gravity, 5, True)
    print('new\n', nbody)


if __name__ == '__main__':
    main()
    pass
