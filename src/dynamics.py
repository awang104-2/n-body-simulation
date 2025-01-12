import numpy as np


gravitational_constant = 1  # Gravitational constant


class Body:

    def __init__(self, mass: float, position, velocity):
        """
        Creates a Body instance representing a point mass with the specified parameters.
        :param mass: Mass (kg)
        :param position: Position vector in Cartesian coordinates (m)
        :param velocity: Velocity vector in Cartesian coordinates (m/s)
        """
        self.mass = mass
        self.positions = [position]
        self.velocities = [velocity]
        self.accelerations = [np.zeros(3)]
        self.time = [0]

    def calculate_gravitational_force(self, body):
        """
        Calculates the current gravitational force between this and another Body/point mass.
        :param body: A separate Body instance
        :return: Gravitational force (vector)
        """
        r = self.calculate_displacement(body)
        if np.all(np.linalg.norm(r) < 1):
            force = np.zeros(3)
        else:
            force = -1 * r * gravitational_constant * self.mass * body.mass / np.linalg.norm(r) ** 3
        return force

<<<<<<< Updated upstream
    def __call__(self, kinematic: str):
=======
    def calculate_displacement(self, body):
        return self.positions[-1] - body.positions[-1]

    def calculate_potential_energy(self, body):
        return np.sum(self.calculate_gravitational_force(body) * self.calculate_displacement(body))

    def calculate_kinetic_energy(self):
        return (1 / 2) * self.mass * np.linalg.norm(self.velocities[-1]) ** 2

    def calculate_total_gravity(self, bodies):
        force = np.zeros(3)
        for body in bodies:
            force += self.calculate_gravitational_force(body)
        return force

    def calculate_total_energies(self, bodies):
        PE, KE, total = (0, 0, 0)
        KE = self.calculate_kinetic_energy()
        for body in bodies:
            PE += self.calculate_potential_energy(body)
        total = KE + PE
        return {'PE': PE, 'KE': KE, 'E': total}

    def __call__(self, kinematic: str, history=False):
>>>>>>> Stashed changes
        """
        Returns a history of the kinematic property of the point mass as a list of tuples, where the first element is time and the second element is the kinematic property at that time.
        :param kinematic:
        :return: List of tuples: (time (s), kinematic)
        """
        match kinematic:
            case 'x' | 'position':
                return list(zip(np.array(self.time), np.array(self.positions)))
            case 'v' | 'velocity':
                return list(zip(np.array(self.time), np.array(self.velocities)))
            case 'a' | 'acceleration':
                return list(zip(np.array(self.time), np.array(self.accelerations)))
        error_message = 'Could not find \'' + kinematic + '\' kinematic. Use lowercase singular name or \'x\', \'v\', \'a\'.'
        raise ValueError(error_message)

class Dynamics:

    def __init__(self, bodies):
        self.bodies = bodies

    def __call__(self, steps, dt, method='verlet'):
        """
        Applies dynamics for gravity using a specific numerical integration method across a certain number of steps with a specific step size.
        :param steps: Number of steps for numerical integration
        :param dt: Step size for numerical integration
        :param method: Type of integration
        :return: A list of dictionaries representing the properties of each Body
        """
        history = []
        for body in self.bodies:
            other_bodies = [b for b in self.bodies if not b == body]
            acceleration = body.calculate_total_gravity(other_bodies) / body.mass
            body.accelerations[-1] = acceleration
        match method:
            case 'verlet':
                self.verlet_method(steps, dt)
        for body in self.bodies:
            history.append({'x': np.array(body.positions), 'v': np.array(body.velocities), 'a': np.array(body.accelerations), 't': np.array(body.time)})
        return history

    def verlet_method(self, steps, dt):
<<<<<<< Updated upstream
        for body in self.bodies:
            other_bodies = [b for b in self.bodies if not b == body]
            acceleration = body.calculate_gravitational_force(other_bodies) / body.mass
            body.accelerations[-1] = acceleration
=======
        """
        Numerically integrates differential equation dynamics using the verlet integration method.
        :param steps: Total number of integration steps.
        :param dt: Integration step size.
        :return:
        """
>>>>>>> Stashed changes
        for _ in range(steps):
            for kinematic in ['x', 'a', 'v']:
                for body in self.bodies:
                    match kinematic:
                        case 'x':
                            position = body.positions[-1] + body.velocities[-1] * dt + 0.5 * body.accelerations[-1] * dt ** 2
                            body.positions.append(position)
                        case 'a':
                            other_bodies = [b for b in self.bodies if not b == body]
                            acceleration = body.calculate_total_gravity(other_bodies) / body.mass
                            body.accelerations.append(acceleration)
                        case 'v':
                            velocity = body.velocities[-1] + 0.5 * (body.accelerations[-2] + body.accelerations[-1]) * dt
                            body.velocities.append(velocity)
            for body in self.bodies:
                prev_time = body.time[-1]
                body.time.append(prev_time + dt)

<<<<<<< Updated upstream
=======
    def gauss_legendre(self, steps, dt):
        """

        :param steps:
        :param dt:
        :return:
        """
        pass





>>>>>>> Stashed changes
