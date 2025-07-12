"""
MIT License

Copyright (c) 2025 awang104
"""
import numpy as np
import numpy.typing as npt
from typing import Iterable, Tuple, Self, Literal, Annotated, TypeVar, Callable, Union
from nbp.constants import G


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
    
    @property
    def KE(self) -> float:
        return (1/2) * self.m * self.speed ** 2
    
    def U(self, bodies: Iterable[Self]) -> float:
        energy = 0
        for b in bodies:
            if b == self:
                continue
            energy += gravity_pe_body(self, b)
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


def gravity_pe_nobody(m1: float, m2: float, d: Vector3D or float):
    if not isinstance(d, float):
        d = np.linalg.norm(d)
    return -G * m1 * m2 / d


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


def electric_force(b1: Body, b2: Body) -> float:
    return 0


def gravity(b1: Body or Vector3D, b2: Body or Vector3D, vector: bool = False) -> float | _array3[np.float64]:
    r = distance(b1, b2)
    if vector:
        return G * b1.m * b2.m / r ** 3 * displacement(b1, b2)
    else:
        return G * b1.m * b2.m / r ** 2


def leapfrog(bodies: Iterable[Body], dt: float, forces: Iterable[Callable]):
    """
    Integrate EOM using the leapfrog method for a list of point masses and forces.
    :param bodies: List of Body instances
    :param dt: Time step (s)
    :param forces: List of functions returning forces between two Body instances.
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


def evaluate(forces, t, x: Vector3D = None, v: Vector3D = None):
    if x is None and v is None:
        raise AttributeError('arguments \'x\' and \'v\' cannot both be None')
    if x is not None:
        x = 3
    if v is not None:
        pass


def rk4(bodies: Iterable[Body], dt: float, forces: Iterable[Callable]):
    """
    Integrate EOM using the Runge-Kutta 4th order method for a list of point masses and forces.
    :param bodies:
    :param dt:
    :param forces:
    :return:
    """
    coeff = [0, 0.5, 0.5, 1]
    x0 = np.array(list(map(lambda b: b.x, bodies)))
    v0 = np.array(list(map(lambda b: b.v, bodies)))
    for stage in range(4):
        for b in bodies:
            b.x += b.v * coeff[stage] * dt
            b.v += b.a * coeff[stage] * dt
            x0[0] += coeff[stage] * b.v * dt
        for i, b1 in enumerate(bodies):
            b1.a = np.zeros(3)
            for b2 in bodies:
                if b2 == b1:
                    continue
                for force in forces:
                    b1.a += force(b1, b2, True) / b1.mass
    for i, b in enumerate(bodies):
        b.x = x0[i]
        b.v = v0[i]


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

