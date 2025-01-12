from dynamics import Body, Dynamics
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    bodies, N = ([], 3)
    bodies.append(Body(mass=1, position=np.zeros(3), velocity=np.zeros(3)))
    bodies.append(Body(mass=1, position=np.array([1, 1, 0]), velocity=np.array([0, 0, 0])))
    bodies.append(Body(mass=1, position=np.array([-5, -5, 0]), velocity=np.array([0, 0, 0])))
    dynamics = Dynamics(bodies)
    energies = []
    for _ in range(1000):
        plt.clf()
        kinematics = dynamics(0.1)
        for body in bodies:
            x, y, z = body('x')
            plt.scatter(x, y)
            plt.xlim(-10, 10)
            plt.ylim(-10, 10)
        plt.pause(0.01)
        body = bodies[0]
        other_bodies = [x for x in bodies if not x == body]
        e = body.calculate_total_energies(other_bodies)
        energies.append(e)
    PE, KE, E, t = ([], [], [], [])
    for i, energy in enumerate(energies):
        t.append(i)
        KE.append(energy['KE'])
        PE.append(energy['PE'])
        E.append(energy['E'])
    KE = np.array(KE)
    PE = np.array(PE)
    plt.clf()
    plt.plot(t, KE)
    plt.plot(t, PE)
    plt.plot(t, E)
    plt.legend(['KE', 'PE', 'E'])
    plt.show()
