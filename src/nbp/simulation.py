"""
MIT License

Copyright (c) 2025 awang104
"""
from typing import Iterable
from nbp import dynamics
import matplotlib.pyplot as plt
import pygame
import multiprocessing


def draw(surface: pygame.Surface, positions, scale: float = 1):
    """
    Draws a list of Body instances as small circles representing point masses.
    :param surface: The pygame Surface the bodies are to be drawn on
    :param bodies: List of Body instances
    :param scale: Meters per pixel, by default 1 m/px
    """
    for x in positions:
        pygame.draw.circle(surface, (255, 0, 0), (x[0], x[1]), 5)


def simulate(system: dynamics.SystemLike, integrator=dynamics.leapfrog, scale: float = 1, *, x_storage=None, e_storage=None):
    """
    Simulates n-body interaction with PyGame.
    :param system:
    :param integrator:
    :param scale:
    """
    positions = multiprocessing.Queue()
    stop_flag = multiprocessing.Event()
    gui = multiprocessing.Process(target=_visuals, args=(positions, stop_flag, scale))
    computation = multiprocessing.Process(target=_simulation, args=(system, integrator, positions, stop_flag))
    computation.start()
    gui.run()


def _visuals(q, flag, scale):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('black')
        positions = q.get()
        draw(screen, positions, scale)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    flag.set()
    

def _simulation(system, integrator, q, flag):
    import time
    t, dt = 0, 0.001
    while not flag.is_set():
        for i in range(10):
            t, dt = integrator(system, t, dt)
            x = system.x.copy()
            q.put(x)
        time.sleep(0.01)
        

def energy_plot(t: Iterable[float], e: Iterable[float]):
    plt.figure()
    plt.title('Mechanical Energy vs. Time of N-Body Problem')
    for e_i in e:
        plt.plot(t, e_i)
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.show()



