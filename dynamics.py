"""
MIT License

Copyright (c) 2025 awang104
"""

import numpy as np


gravitational_constant = 1  # Gravitational constant
G = gravitational_constant  # Gravitational constant


def gravitational_potential_energy(b1, b2):
    return -G * b1.m * b2.m / distance(b1, b2)

def distance(b1, b2):
    return np.linalg.norm(b2.x - b1.x)


def displacement(b1, b2):
    return b2.x - b1.x


def n_bodies(n):
    bodies = []
    for _ in range(n):
        bodies.append(Body())
    return bodies


def gravity(b1, b2, vector=False):
    r = distance(b1, b2)
    if vector:
        return G * b1.m * b2.m / r ** 3 * displacement(b1, b2)
    else:
        return G * b1.m * b2.m / r ** 2


def leapfrog(bodies, dt, forces=tuple([gravity])):
    """
    Use leapfrog method to integrate EOM for a list of Body instances using list of forces.
    :param bodies: List of Body instances
    :param dt: Time step (s)
    :param force: Function of the force, gravity by default
    """
    v_halves = []
    for b in bodies:
        v_half = b.v + 1/2 * b.a * dt
        v_halves.append(v_half)
        b.x += v_half * dt
    for i, b1 in enumerate(bodies):
        b1.a = np.zeros(3)
        for b2 in bodies:
            if b2 == b1:
                continue
            for force in forces:
                b1.a += force(b1, b2, True) / b1.mass
        b1.v = v_halves[i] + 1/2 * b1.a * dt


def boundary(bodies, xlim, ylim):
    for b in bodies:
        b.bounce(xlim, ylim)


class Body:

    def __init__(self, mass=100, position=(0, 0, 0), velocity=(0, 0, 0), acceleration=(0, 0, 0)):
        """
        Models the kinematics of a point mass.
        :param mass: Scalar mass of the point mass
        :param position: 3D vector position of the point mass
        :param velocity: 3D vector velocity of the point mass
        :param acceleration: 3D vector acceleration of the point mass
        """
        self.mass = mass
        self.position = np.array(position).astype(float)
        self.velocity = np.array(velocity).astype(float)
        self.acceleration = np.array(acceleration).astype(float)

    @property
    def m(self):
        return self.mass

    @m.setter
    def m(self, mass):
        self.mass = mass

    @property
    def x(self):
        return self.position
    
    @x.setter
    def x(self, position):
        self.position = position

    @property
    def v(self):
        return self.velocity

    @v.setter
    def v(self, velocity):
        self.velocity = velocity

    @property
    def a(self):
        return self.acceleration

    @a.setter
    def a(self, acceleration):
        self.acceleration = acceleration

    @property
    def v_dir(self):
        return self.velocity / np.linalg.norm(self.velocity)

    @property
    def a_dir(self):
        return self.acceleration / np.linalg.norm(self.acceleration)
    
    @property
    def speed(self):
        return np.linalg.norm(self.v)
    
    @property
    def KE(self):
        return (1/2) * self.m * self.speed ** 2
    
    def U(self, bodies):
        energy = 0
        for b in bodies:
            if b == self:
                continue
            energy += gravitational_potential_energy(self, b)
        return energy
    
    def total_mechanical_energy(self, bodies):
        return self.U(bodies) + self.KE
    
    def bounce(self, xlim, ylim):
        if self.x[0] <= xlim[0]:
            self.v[0] = np.abs(self.v[0])
        elif self.x[0] >= xlim[1]:
            self.v[0] = -np.abs(self.v[0])
        if self.x[1] <= ylim[0]:
            self.v[1] = np.abs(self.v[1])
        elif self.x[1] >= ylim[1]:
            self.v[1] = -np.abs(self.v[1])
        
    def dict(self):
        return {'m': self.m, 'x': self.x, 'v': self.v, 'a': self.a}
    
    def __repr__(self):
        return str(self.dict())
    
    def __str__(self):
        return f'Mass: {self.m} | Position: {self.x} | Velocity: {self.v} | Acceleration: {self.a}'
    



