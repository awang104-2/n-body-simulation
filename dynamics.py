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


if __name__ == '__main__':
    b1 = Body(mass=1, position=np.array([1000, 0, 0]), velocity=np.array([0, 5, 0]))
    b3 = Body(mass=1, position=np.array([1000, 0, 0]), velocity=np.array([0, 0, 5]))
    b2 = Body(mass=25000, position=np.zeros(3), velocity=np.zeros(3))
    dynamics = Dynamics([b1, b2, b3])
    kinematics = dynamics(10000, 0.5)
    x1, y1, z1 = kinematics[0]['x'].T
    x2, y2, z2 = kinematics[1]['x'].T
    x3, y3, z3 = kinematics[2]['x'].T
    import matplotlib.pyplot as plt
    plt.plot(x1, y1, color='red')
    plt.plot(x2, y2, color='blue')
    plt.plot(x3, y3, color='green')
    plt.show()

