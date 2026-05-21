import pygame

from polis.env.world import World
from polis.rendering.pygame_renderer import Renderer


def main():
    world = World()

    renderer = Renderer(world)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.update()

        renderer.render()

    pygame.quit()


if __name__ == "__main__":
    main()