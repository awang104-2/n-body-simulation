import numpy as np


gravitational_constant = 1  # Gravitational constant
G = gravitational_constant  # Gravitational constant


class Body:

    def __init__(self, mass, position, velocity, acceleration):
        self._mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)


def define_body(mass, position, velocity=None, acceleration=None):
    """
    Creates a dictionary representing a point mass with the parameters as properties.
    :param mass: Mass (kg)
    :param position: Position (m)
    :param velocity: Velocity (m/s)
    :param acceleration: Acceleration (m/s^2)
    :return: A dictionary with the point mass's properties
    """
    N = len(position)
    if velocity is None:
        velocity = np.zeros(N)
    if acceleration is None:
        acceleration = np.zeros(N)
    position, velocity, acceleration = np.array(position), np.array(velocity), np.array(acceleration)
    return {'m': mass, 'x': position, 'v': velocity, 'a': acceleration}


def gravity(bodies):
    """
    Returns the force and acceleration of gravity between a group of point masses.
    :param bodies: List of dictionaries with 'x' (m), 'v' (m/s), 'a' (m/s^2), and 'm' (kg)
    :return: List, 1st element is force of gravity (N), 2nd is acceleration of gravity (m/s^2)
    """
    N = len(bodies)
    dimensions = len(bodies[-1]['x'])
    fg = np.zeros((N, dimensions))
    g = np.zeros((N, dimensions))
    for i, b1 in enumerate(bodies):
        for j, b2 in list(enumerate(bodies))[i+1:]:
            r = b1['x'] - b2['x']
            mg = -G * b1['m'] * b2['m'] / np.linalg.norm(r) ** 3 * r
            fg[i] += mg
            fg[j] -= mg
            g[i] += mg / b1['m']
            g[j] -= mg / b2['m']
    return fg, g


def get_kinematic_quantity(bodies, name):
    """
    Returns the specified kinematic quantity of the point masses as a list in corresponding order to the inputted dictionaries.
    :param bodies: List of dictionaries
    :param name: String 'x', 'v', 'a', etc.
    :return: Numpy array of the specified physical quantity (m, m/s, m/s^2, etc.)
    """
    return np.array([np.copy(b[name]) for b in bodies])


def leapfrog(bodies, force, dt, is_a0, steps=1):
    """
    Use leapfrog method to integrate EOM and find the kinematic quantities of point masses after some time.
    :param bodies: List of dictionaries representing point masses
    :param force: Function representing the coupled EOM-ODE
    :param dt: Time step (s)
    :param is_a0: True if initial acceleration hasn't been set #
    :param steps: Number of integration steps
    :return: List of dictionaries representing point masses
    """
    if is_a0:
        a = force(bodies)[1]
    else:
        a = get_kinematic_quantity(bodies, 'a')
    v = get_kinematic_quantity(bodies, 'v')
    x = get_kinematic_quantity(bodies, 'x')
    v = v + a * dt / 2
    x = x + v * dt
    a = force(bodies)[1]
    v = v + a * dt / 2
    new_bodies = []
    for i, b in enumerate(bodies):
        mass, position, velocity, acceleration = (np.copy(b['m']), x[i], v[i], a[i])
        new_bodies.append({'m': mass, 'x': position, 'v': velocity, 'a': acceleration})
    return new_bodies


def boundary(body, xlim, ylim):
    x, y = body['x']
    velocity = body['v']
    if x <= min(xlim) or x >= max(xlim):
        velocity[0] *= -1
    if y <= min(ylim) or y >= max(ylim):
        velocity[1] *= -1


