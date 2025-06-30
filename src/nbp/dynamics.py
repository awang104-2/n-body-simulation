"""
MIT License

Copyright (c) 2025 awang104
"""

import numpy as np
import numpy.typing as npt
from typing import Iterable, Tuple, Self, Literal, Annotated, TypeVar, Callable


# Typing
_dtype = TypeVar("DType", bound=np.generic)
_array3 = Annotated[npt.NDArray[_dtype], Literal[3]]



class Body:

    def __init__(self, mass: float, position: Tuple[float, float, float] = (0, 0, 0), velocity: Tuple[float, float, float] = (0, 0, 0), acceleration: Tuple[float, float, float] = (0, 0, 0), charge: float = 0):
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
        self.color = (255, 0, 0)
        self.charge = charge

    @property
    def q(self) -> float:
        return self.charge
    
    @q.setter
    def q(self, q: float):
        self.charge = q

    @property
    def m(self) -> float:
        return self.mass

    @m.setter
    def m(self, mass: float):
        self.mass = mass

    @property
    def x(self) -> _array3[np.float64]:
        return self.position
    
    @x.setter
    def x(self, position: Tuple[float, float, float]):
        self.position = position

    @property
    def v(self) -> _array3[np.float64]:
        return self.velocity

    @v.setter
    def v(self, velocity: Tuple[float, float, float]):
        self.velocity = velocity

    @property
    def a(self) -> _array3[np.float64]:
        return self.acceleration

    @a.setter
    def a(self, acceleration: Tuple[float, float, float]):
        self.acceleration = acceleration

    @property
    def v_dir(self) -> _array3[np.float64]:
        return self.velocity / np.linalg.norm(self.velocity)

    @property
    def a_dir(self) -> _array3[np.float64]:
        return self.acceleration / np.linalg.norm(self.acceleration)
    
    @property
    def speed(self) -> float:
        return np.linalg.norm(self.v)
    
    @property
    def KE(self) -> float:
        return (1/2) * self.m * self.speed ** 2
    
    def U(self, bodies: Iterable[Self]) -> float:
        energy = 0
        for b in bodies:
            if b == self:
                continue
            energy += gravitational_potential_energy(self, b)
        return energy
    
    def total_mechanical_energy(self, bodies: Iterable[Self]) -> float:
        return self.U(bodies) + self.KE
    
    def bounce(self, xlim: Tuple[float, float], ylim: Tuple[float, float]):
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
    

def gravitational_potential_energy(b1: Body, b2: Body) -> float:
    return -G * b1.m * b2.m / distance(b1, b2)


def distance(b1: Body, b2: Body) -> float:
    return np.linalg.norm(b2.x - b1.x)


def displacement(b1: Body, b2: Body) -> _array3[np.float64]:
    return b2.x - b1.x


def n_bodies(n: int) -> Iterable[Body]:
    bodies = []
    for _ in range(n):
        bodies.append(Body())
    return bodies


def electric_force(b1: Body, b2: Body) -> float:
    return 


def gravity(b1: Body, b2: Body, vector: bool = False) -> float | _array3[np.float64]:
    r = distance(b1, b2)
    if vector:
        return G * b1.m * b2.m / r ** 3 * displacement(b1, b2)
    else:
        return G * b1.m * b2.m / r ** 2


def leapfrog(bodies: Iterable[Self], dt: float, forces: Tuple[Callable] = tuple([gravity])):
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
    

class System:

    def __init__(self, bodies, forces, integrator):
        self.bodies = bodies
        self.forces = forces
        self.integrator = integrator
        self._history = [[], False]
        self.time = 0
        for b1 in enumerate(bodies):
            b1.a = np.zeros(3)
            for b2 in bodies:
                if b2 == b1:
                    continue
                for force in forces:
                    b1.a += force(b1, b2, True) / b1.mass

    @property
    def t(self) -> float:
        return self.time

    @property
    def history(self) -> bool:
        return self._history[1]

    @history.setter
    def history(self, on):
        self._history[1] = on
        
    def __call__(self, dt, n=1):
        for _ in range(n):
            self.integrator(self.bodies, dt, forces=self.forces)
            self.time += dt
        
