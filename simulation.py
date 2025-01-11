from dynamics import Body, Dynamics
import matplotlib.pyplot as plt


if __name__ == '__main__':
    b1 = Body(mass=1, position=np.array([1000, 0, 0]), velocity=np.array([0, 5, 0]))
    b3 = Body(mass=1, position=np.array([1000, 0, 0]), velocity=np.array([0, 0, 5]))
    b2 = Body(mass=25000, position=np.zeros(3), velocity=np.zeros(3))
    dynamics = Dynamics([b1, b2, b3])
    kinematics = dynamics(10000, 0.5)
    x1, y1, z1 = kinematics[0]['x'].T
    x2, y2, z2 = kinematics[1]['x'].T
    x3, y3, z3 = kinematics[2]['x'].T
    plt.plot(x1, y1, color='red')
    plt.plot(x2, y2, color='blue')
    plt.plot(x3, y3, color='green')
    plt.show()
