"""
MIT License

Copyright (c) 2025 awang104
"""
import numpy as np
import numpy.typing as npt
from typing import Iterable, Tuple, Self, Literal, Annotated, TypeVar, Callable, Union
from nbp.constants import G
import random


# Typing
_dtype = TypeVar("_dtype", bound=np.generic)
_array3 = Annotated[npt.NDArray[_dtype], Literal[3]]
Vector3D = Tuple[float, float, float]


class Body:

    def __init__(self, mass: float, position: Vector3D = (0, 0, 0), velocity: Vector3D = (0, 0, 0), acceleration: Vector3D = (0, 0, 0), charge: float = 0):
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
    def x(self, position: Vector3D):
        self.position = position

    @property
    def v(self) -> _array3[np.float64]:
        return self.velocity

    @v.setter
    def v(self, velocity: Vector3D):
        self.velocity = velocity

    @property
    def a(self) -> _array3[np.float64]:
        return self.acceleration

    @a.setter
    def a(self, acceleration: Vector3D):
        self.acceleration = acceleration

    @property
    def v_dir(self) -> _array3[np.float64]:
        return self.velocity / np.linalg.norm(self.velocity)

    @property
    def a_dir(self) -> _array3[np.float64]:
        return self.acceleration / np.linalg.norm(self.acceleration)
    
    @property
    def speed(self) -> float:
        return float(np.linalg.norm(self.v))
    
    def copy(self):
        return Body(self.mass, self.x.copy(), self.v.copy(), self.a.copy(), self.charge)
        
    def dict(self):
        return {'m': self.m, 'x': self.x, 'v': self.v, 'a': self.a}
    
    def __repr__(self):
        return str(self.dict())
    
    def __str__(self):
        return f'Mass: {self.m} | Position: {self.x} | Velocity: {self.v} | Acceleration: {self.a}'
    
    
class System:

    def __init__(self, bodies, gravity=True, electric_force=False):
        self.bodies = bodies
        self.forces = {'gravity': gravity, 'electric': electric_force}

    @property
    def m(self):
        return np.array([b.m for b in self.bodies])

    @property
    def x(self):
        return np.array([b.x for b in self.bodies])
    
    @property
    def v(self):
        return np.array([b.v for b in self.bodies])

    @property
    def a(self):
        if self.forces['gravity']:
            for i, b1 in enumerate(self.bodies):
                b1.a = np.zeros(3)
                for b2 in self.bodies:
                    if b2 == b1:
                        continue
                    b1.a += gravity(b1, b2, True) / b1.mass
        return np.array([b.a for b in self.bodies])
    
    @property
    def com(self):
        return (self.mass * self.position) / sum(self.mass)
    
    def copy(self):
        bodies = []
        for b in self.bodies:
            bodies.append(b.copy())
        return System(bodies)


def gravity_pe_body(b1: Body, b2: Body) -> float:
    return -G * b1.m * b2.m / distance(b1, b2)


def distance(b1: Body, b2: Body) -> float:
    return float(np.linalg.norm(b2.x - b1.x))


def displacement(b1: Body, b2: Body) -> _array3[np.float64]:
    return b2.x - b1.x


def n_bodies(n: int) -> Iterable[Body]:
    bodies = []
    for _ in range(n):
        bodies.append(Body())
    return bodies


def gravity(b1: Body | Vector3D, b2: Body | Vector3D, vector: bool = False) -> float | _array3[np.float64]:
    r = distance(b1, b2)
    if vector:
        return G * b1.m * b2.m / r ** 3 * displacement(b1, b2)
    else:
        return G * b1.m * b2.m / r ** 2


def leapfrog(system: System | Iterable[Body], dt: float, forces: Iterable[Callable]):
    """
    Integrate EOM using the leapfrog method for a list of point masses and forces.
    :param bodies: System instance or list of Body instances
    :param dt: Time step (s)
    :param forces: List of functions returning forces between two Body instances.
    """
    if isinstance(system, Iterable):
        bodies = system
    else:
        bodies = system.bodies

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


def evaluate_grav(stage: int, system: System, k=None, dt=None):
    system = system.copy()
    match stage:
        case 1:
            pass
        case 2:
            system.x += 0.5 * k[0] * dt
            system.v += 0.5 * k[1] * dt
        case 3:
            system.x += 0.5 * k[0] * dt
            system.v += 0.5 * k[1] * dt
        case 4:
            system.x += k[0] * dt
            system.v += k[1] * dt
    k_x = system.v
    k_v = system.a
    return k_x, k_v


def rk4(system: System, dt: float, forces: Iterable[Callable]):
    """
    Integrate EOM using the Runge-Kutta 4th order method for a list of point masses and forces.
    :param bodies:
    :param dt:
    :param forces:
    :return:
    """
    k1 = evaluate_grav(1, system)
    k2 = evaluate_grav(2, system, k1, dt)
    k3 = evaluate_grav(3, system, k2, dt)
    k4 = evaluate_grav(4, system, k3, dt)
    system.x += (1/6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) * dt
    system.v += (1/6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) * dt


def boundary(bodies, xlim, ylim):
    for b in bodies:
        b.bounce(xlim, ylim)
    

