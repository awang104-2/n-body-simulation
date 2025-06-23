import dynamics
import matplotlib.pyplot as plt
import pygame


def define_bodies():
    bodies = [
        dynamics.define_body(mass=1, position=[0, 1, 0], velocity=[0, 1, 0]),
        dynamics.define_body(mass=1, position=[-1, -3, 0], velocity=[1, -1, 0]),
        dynamics.define_body(mass=1, position=[2, -1, 0])
    ]
    return bodies


def simulate():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED)
    clock = pygame.time.Clock()
    running, pressed = True, False
    x, y, radius = 100, 20, 3
    velocity = [7, 3]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
                radius = 0
                x, y = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                pressed = False
        screen.fill('white')
        pygame.draw.circle(screen, 0, (x, y), radius)
        pygame.display.flip()
        clock.tick(60)




def graph_simulation(bodies, n):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED)
    clock = pygame.time.Clock()
    running = True
    # pygame.display.toggle_fullscreen()
    pressed = False
    r = 3
    x, y = None, None
    color = 0
    circles = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
                x, y = pygame.mouse.get_pos()
                circles.append([x, y, r])
            elif event.type == pygame.MOUSEBUTTONUP:
                pressed = False
        if pressed:
            circles[-1][2] += 1
        screen.fill('white')
        for circle in circles:
            pygame.draw.circle(screen, (0, 0, 255), (circle[0], circle[1]), circle[2])
        pygame.display.flip()
        clock.tick(60)

    '''
    for t_step in range(n):
        plt.cla()  # Clear the graph
        for pos in dynamics.get_kinematic_quantity(bodies, 'x'):
            plt.plot(pos[0], pos[1], marker='.', linestyle='')
        plt.xlim(-20, 20)  # x-axis limits from -20 to 20
        plt.ylim(-20, 20)  # y-axis limits from -20 to 20
        bodies = dynamics.leapfrog(bodies=bodies, force=dynamics.gravity, dt=0.1, is_a0=t_step == 0)
        plt.pause(0.1)
    plt.show()
    '''


if __name__ == '__main__':
    nbody = define_bodies()
    simulate()
            




