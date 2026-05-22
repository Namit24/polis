import pygame

from polis.env.world import World
from polis.rendering.pygame_renderer import Renderer
from polis.simulation.metrics import SimMetrics
from polis.utils.logger import get_logger

log = get_logger(__name__)


def main():
    log.info("Starting Polis simulation")

    world = World(
        width=50,
        height=50,
        num_agents=50,
        num_food=150,
        food_respawn_per_tick=2,
        food_cap=300,
    )

    metrics = SimMetrics()
    metrics._prev_agent_count = len(world.agents)
    world.metrics = metrics

    renderer = Renderer(world)

    tick = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not world.agents:
            log.warning("All agents dead — stopping simulation")
            running = False
            break

        world.update()
        tick += 1

        renderer.render()

    log.info(f"Simulation ended after {tick} ticks")
    metrics.print_summary(tick)

    pygame.quit()


if __name__ == "__main__":
    main()