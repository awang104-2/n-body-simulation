"""
MIT License

Copyright (c) 2025 awang104
"""

import dynamics
import pygame
import matplotlib.pyplot as plt


def draw(surface, bodies):
    for body in bodies:
        x, y, z = body.x.astype(int)
        pygame.draw.circle(surface, (0, 0, 255), (x, y), 5)


def simulate(bodies):
    t = [0]
    e = [[b.total_mechanical_energy(bodies)] for b in bodies]
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('white')
        draw(screen, bodies)
        pygame.display.flip()
        dynamics.leapfrog(bodies=bodies, dt=0.01)
        for i, b in enumerate(bodies):
            e[i].append(b.total_mechanical_energy(bodies))
        t.append(t[-1] + 0.01)
        clock.tick(60)
    pygame.quit()
    return t, e


def energy_plot(t, e):
    plt.figure()
    plt.title('Mechanical Energy vs. Time of N-Body Problem')
    for e_i in e:
        plt.plot(t, e_i)
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.show()
    

if __name__ == '__main__':
    bodies = []
    bodies.append(dynamics.Body(mass=1, position=(340, 360, 0), velocity=(0, 258, 0)))
    bodies.append(dynamics.Body(mass=2e7, position=(640, 360, 0), velocity=(0, 0, 0)))
    time, energy = simulate(bodies)
    energy_plot(time, energy)
