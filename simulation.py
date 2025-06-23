"""
MIT License

Copyright (c) 2025 awang104
"""

import dynamics
import pygame
import matplotlib.pyplot as plt


def draw(surface, bodies):
    max_mass = max(map(lambda b: b.m, bodies))
    for b in bodies:
        x, y, z = b.x.astype(int)
        pygame.draw.circle(surface, [255, 0, int(b.m / max_mass * 255)], (x, y), 5)


def simulate(bodies, bounded=False):
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
        screen.fill('black')
        draw(screen, bodies)
        pygame.display.flip()
        dynamics.leapfrog(bodies=bodies, dt=0.01)
        if bounded:
            dynamics.boundary(bodies, [0, 1280], [0, 720])
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
    

