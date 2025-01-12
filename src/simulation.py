from dynamics import Body, Dynamics
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    bodies, N = ([], 10)
    for _ in range(N):
        body = Body(mass=np.random.rand()*20, position=np.random.rand(3) * 30, velocity=np.random.rand(3) * 0)
        bodies.append(body)
    dynamics = Dynamics(bodies)
    for _ in range(100):
        plt.clf()
        kinematics = dynamics(0.1)
        for body in bodies:
            x, y, z = body('x')
            plt.scatter(x, y)
            plt.xlim(-30, 30)
            plt.ylim(-30, 30)
        plt.pause(0.1)
    plt.show()
