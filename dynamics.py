import numpy as np


gravitational_constant = 1  # Gravitational constant


class Body:

    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.positions = [position]
        self.velocities = [velocity]
        self.accelerations = [np.zeros(3)]
        self.time = [0]

    def calculate_gravitational_force(self, bodies):
        """
        Calculates the current gravitational force between this body and a set of bodies.
        :param body: A list of Body objects
        :return: Total Gravitational force
        """
        force = 0
        for body in bodies:
            r = self.positions[-1] - body.positions[-1]
            if np.all(np.abs(r) < np.abs([1, 1, 1])):
                force += 0
            else:
                force += -1 * r * gravitational_constant * self.mass * body.mass / np.linalg.norm(r) ** 3
        return force


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
        match method:
            case 'verlet':
                self.verlet_method(steps, dt)
        for body in self.bodies:
            history.append({'x': np.array(body.positions), 'v': np.array(body.velocities), 'a': np.array(body.accelerations), 't': np.array(body.time)})
        return history

    def verlet_method(self, steps, dt):
        for body in self.bodies:
            other_bodies = [b for b in self.bodies if not b == body]
            acceleration = body.calculate_gravitational_force(other_bodies) / body.mass
            body.accelerations[-1] = acceleration
        for _ in range(steps):
            for kinematic in ['x', 'a', 'v']:
                for body in self.bodies:
                    match kinematic:
                        case 'x':
                            position = body.positions[-1] + body.velocities[-1] * dt + 0.5 * body.accelerations[-1] * dt ** 2
                            body.positions.append(position)
                        case 'a':
                            other_bodies = [b for b in self.bodies if not b == body]
                            acceleration = body.calculate_gravitational_force(other_bodies) / body.mass
                            body.accelerations.append(acceleration)
                        case 'v':
                            velocity = body.velocities[-1] + 0.5 * (body.accelerations[-2] + body.accelerations[-1]) * dt
                            body.velocities.append(velocity)
            for body in self.bodies:
                prev_time = body.time[-1]
                body.time.append(prev_time + dt)

