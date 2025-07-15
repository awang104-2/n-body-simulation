"""
MIT License

Copyright (c) 2025 awang104
"""
from warnings import deprecated
import numpy as np
import numpy.typing as npt
from typing import Iterable, Tuple, Self, Literal, Annotated, TypeVar, Callable, Union
from nbp import constants


# Typing
_dtype = TypeVar("_dtype", bound=np.generic)
_array3 = Annotated[npt.NDArray[_dtype], Literal[3]]
Vector3D = Union[Tuple[float, float, float], np.typing.ArrayLike]

# RKF4 Tolerance
TOLERANCE = 1e-8


class Body:

    def __init__(self, m: float, x: Vector3D = (0, 0, 0), v: Vector3D = (0, 0, 0), a: Vector3D = (0, 0, 0), q: float = 0):
        """
        Models the kinematics of a point mass.
        :param m: Scalar mass of the point mass
        :param x: 3D vector position of the point mass
        :param v: 3D vector velocity of the point mass
        :param a: 3D vector acceleration of the point mass
        """
        self.mass = m
        self.position = np.array(x).astype(float)
        self.velocity = np.array(v).astype(float)
        self.acceleration = np.array(a).astype(float)
        self.charge = q
        self.color = (255, 0, 0)

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
    def KE(self):
        return 1 / 2 * self.m * self.speed ** 2
    
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
    def KE(self):
        return sum([b.KE for b in self.bodies])

    @property
    def U(self):
        energy = 0
        n = len(self.bodies)
        for i in range(n):
            for j in range(i + 1, n):
                b1, b2 = self.bodies[i], self.bodies[j]
                energy -= gravity(b1, b2, False) * distance(b1, b2)
        return energy

    @property
    def m(self):
        return np.array([b.m for b in self.bodies])
    
    @m.setter
    def m(self, masses):
        for i, b in enumerate(self.bodies):
            b.m = masses[i]

    @property
    def x(self):
        return np.array([b.x for b in self.bodies])
    
    @x.setter
    def x(self, positions):
        for i, b in enumerate(self.bodies):
            b.x = positions[i]
    
    @property
    def v(self):
        return np.array([b.v for b in self.bodies])
    
    @v.setter
    def v(self, velocities):
        for i, b in enumerate(self.bodies):
            b.v = velocities[i]

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
    
    @a.setter
    def a(self, accelerations):
        for i, b in enumerate(self.bodies):
            b.a = accelerations[i]
    
    @property
    def com(self):
        return (self.m @ self.x) / sum(self.m)
    
    def copy(self):
        bodies = []
        for b in self.bodies:
            bodies.append(b.copy())
        return System(bodies)


SystemLike = Union[Iterable[dict], Iterable[Body], System]


def distance(b1: Body, b2: Body) -> float:
    return float(np.linalg.norm(b2.x - b1.x))


def displacement(b1: Body, b2: Body) -> _array3[np.float64]:
    return b2.x - b1.x


def gravity(b1: Body | Vector3D, b2: Body | Vector3D, vector: bool = False) -> float | _array3[np.float64]:
    r = distance(b1, b2)
    if vector:
        return constants.G * b1.m * b2.m / r ** 3 * displacement(b1, b2)
    else:
        return constants.G * b1.m * b2.m / r ** 2


def evaluate_rk4(stage: int, system: System, k=None, dt=None):
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


def rk4(system: System, dt: float):
    """
    Integrate EOM using the Runge-Kutta 4th order method for a list of point masses and forces.
    :param system:
    :param dt:
    :return:
    """
    k1 = evaluate_rk4(1, system)
    k2 = evaluate_rk4(2, system, k1, dt)
    k3 = evaluate_rk4(3, system, k2, dt)
    k4 = evaluate_rk4(4, system, k3, dt)
    system.x += (1/6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) * dt
    system.v += (1/6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) * dt


def leapfrog(system: System, current_time: float, dt: float = 0.01):
    """
    Integrate EOM in place using the leapfrog method for a list of point masses and forces.
    :param system: System instance or list of Body instances
    :param current_time: Current time (s)
    :param dt: Time step (s)
    """
    v_halves = system.v + 1/2 * system.a * dt
    system.x += v_halves * dt
    system.v = v_halves + 1/2 * system.a * dt
    current_time += dt
    return current_time, dt


@deprecated('old_leapfrog(system, dt) is deprecated, use leapfrog(system, dt) instead')
def old_leapfrog(system: System, current_time: float, dt: float):
    """
    Integrate EOM using the leapfrog method for a list of point masses and forces.
    :param system: List of Body instances
    :param current_time: Current time (s)
    :param dt: Time step (s)
    """
    bodies = system.bodies
    v_halves = []
    for i, b1 in enumerate(bodies):
        b1.a = np.zeros(3)
        for b2 in bodies:
            if b2 == b1:
                continue
            b1.a += gravity(b1, b2, True) / b1.mass
    for b in bodies:
        v_half = b.v + 1 / 2 * b.a * dt
        v_halves.append(v_half)
        b.x += v_half * dt
    for i, b1 in enumerate(bodies):
        b1.a = np.zeros(3)
        for b2 in bodies:
            if b2 == b1:
                continue
            b1.a += gravity(b1, b2, True) / b1.mass
        b1.v = v_halves[i] + 1 / 2 * b1.a * dt
    current_time += dt
    return current_time, dt


def evaluate_rkf4(system, delta=None):
    system = system.copy()
    if delta is not None:
        system.x += delta[0]
        system.v += delta[1]
    k_x = system.v
    k_v = system.a
    return np.array([k_x, k_v])


def rkf4(system: System, current_time: float, dt: float):
    """

    :param system:
    :param current_time:
    :param dt:
    """
    # Find the K's
    k1 = evaluate_rkf4(system)
    k2 = evaluate_rkf4(system, 0.25 * k1 * dt)
    k3 = evaluate_rkf4(system, (3/32 * k1 + 9/32 * k2) * dt)
    k4 = evaluate_rkf4(system, (1932/2197 * k1 - 7200/2197 * k2 + 7296/2197 * k3) * dt)
    k5 = evaluate_rkf4(system, (439/216 * k1 - 8 * k2 + 3680/513 * k3 - 845/4104 * k4) * dt)
    k6 = evaluate_rkf4(system, (-8/27 * k1 + 2 * k2 - 3544/2565 * k3 + 1859/4104 * k4  - 11/40 * k5) * dt)

    # Numerically integrate the system's position and velocity by one step
    x1, v1 = system.x, system.v
    system.x += (25/216 * k1[0] + 1408/2565 * k3[0] + 2197/4104 * k4[0] - 1/5 * k5[0]) * dt
    system.v += (16/135 * k1[1] + 66565/12825 * k3[1] + 28561/56430 * k4[1] - 9/50 * k5[1] + 2/55 * k6[1]) * dt
    
    # Find the fourth order error using the RKF4 and RKF5 method.
    tolerance_scale = [None, None]
    tolerance_scale[0] = TOLERANCE + np.maximum(np.abs(x1), np.abs(system.x)) * TOLERANCE
    tolerance_scale[1] = TOLERANCE + np.maximum(np.abs(v1), np.abs(system.v)) * TOLERANCE
    tolerance_scale = np.array(tolerance_scale)
    error_estimation = (25/216 * k1 + 1408/2565 * k3 + 2197/4104 * k4 - 1/5 * k5) * dt - (16/135 * k1 + 66565/12825 * k3 + 28561/56430 * k4 - 9/50 * k5 + 2/55 * k6) * dt
    total = 0
    for i in range(2):
        total += np.average(np.square(error_estimation[i] / tolerance_scale[i]))
    error = np.sqrt(total / 2)

    # Find the next time step based on fourth-order error
    min_power = 4
    safety_min, safety_max = 0.33, 6
    safety_factor = 0.38 ** (1 / (1 + min_power))
    if error < 1e-12:
        error = 1e-12
    dt_next = safety_factor * error ** (-1 / (1 + min_power))
    if dt_next > safety_max * dt:
        dt *= safety_max
    elif dt_next < safety_min * dt:
        dt *= safety_min
    current_time += dt_next
    return current_time, dt_next



def system(*args: SystemLike):
    bodies = []
    for arg in args:
        if isinstance(arg, Iterable) and all(isinstance(b, Body) for b in arg):
            for b in arg:
                bodies.append(b)
        elif isinstance(arg, System):
            for b in arg.bodies:
                bodies.append(b)
        elif isinstance(arg, Iterable) and all(isinstance(kwargs, dict) for kwargs in arg):
            for kwargs in arg:
                b = Body(**kwargs)
                bodies.append(b)
        else:
            raise AttributeError(f'Arguments must be SystemLike: {SystemLike}')
    return System(bodies)
