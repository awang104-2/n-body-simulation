import dynamics
import matplotlib.pyplot as plt


def define_bodies():
    bodies = [
        dynamics.define_body(mass=1, position=[0, 1, 0], velocity=[0, 1, 0]),
        dynamics.define_body(mass=1, position=[-1, -3, 0], velocity=[1, -1, 0]),
        dynamics.define_body(mass=1, position=[2, -1, 0])
    ]
    return bodies


def graph_simulation(bodies, n):
    # Graphing the simulation
    for t_step in range(n):
        plt.cla()  # Clear the graph
        for pos in dynamics.get_kinematic_quantity(bodies, 'x'):
            plt.plot(pos[0], pos[1], marker='.', linestyle='')
        plt.xlim(-20, 20)  # x-axis limits from -20 to 20
        plt.ylim(-20, 20)  # y-axis limits from -20 to 20
        bodies = dynamics.leapfrog(bodies=bodies, force=dynamics.gravity, dt=0.1, is_a0=t_step == 0)
        plt.pause(0.1)
    plt.show()


if __name__ == '__main__':
    nbody = define_bodies()
    graph_simulation(nbody, 500)
