"""
MIT License

Copyright (c) 2025 awang104
"""

import dynamics
import pygame
import matplotlib.pyplot as plt 
from typing import Iterable


def draw(surface: pygame.Surface, bodies: Iterable[dynamics.Body], scale: float = 1):
    """
    Draws a list of Body instances as small circles representing point masses.
    :param surface: The pygame Surface the bodies are to be drawn on
    :param bodies: List of Body instances
    :param scale: Meters per pixel, by default 1 m/px
    """
    max_mass = max(map(lambda b: b.m, bodies))
    for b in bodies:
        x, y, z = (b.x / scale).astype(int)
        pygame.draw.circle(surface, b.color, (x, y), 5)


def simulate(bodies: Iterable[dynamics.Body], bounded: bool = False):
    """
    :param bodies:
    :param bounded: 
    """
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


def energy_plot(t: Iterable[float], e: Iterable[float]):
    plt.figure()
    plt.title('Mechanical Energy vs. Time of N-Body Problem')
    for e_i in e:
        plt.plot(t, e_i)
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.show()
    
