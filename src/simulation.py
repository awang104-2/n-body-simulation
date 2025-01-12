from dynamics import Body, Dynamics
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
<<<<<<< Updated upstream
    b1 = Body(mass=1, position=np.array([1000, 0, 0]), velocity=np.array([0, 5, 0]))
    b2 = Body(mass=1, position=np.array([1000, 0, 0]), velocity=np.array([0, 0, 5]))
    b3 = Body(mass=25000, position=np.zeros(3), velocity=np.zeros(3))
    dynamics = Dynamics([b1, b2, b3])
    kinematics = dynamics(10000, 0.5)
    x1, y1, z1 = kinematics[0]['x'].T
    x2, y2, z2 = kinematics[1]['x'].T
    x3, y3, z3 = kinematics[2]['x'].T
    plt.plot(x1, y1, color='blue')
    plt.plot(x2, y2, color='red')
    plt.plot(x3, y3, color='black')
=======
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
    plt.plot(t, KE + PE)
    plt.plot(t, E)
    plt.legend(['KE', 'PE', 'E'])
>>>>>>> Stashed changes
    plt.show()
