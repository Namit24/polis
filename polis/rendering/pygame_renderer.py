import pygame


CELL_SIZE = 12

BACKGROUND = (15, 15, 20)
GRID_COLOR = (40, 40, 50)
AGENT_COLOR = (0, 255, 180)


class Renderer:
    def __init__(self, world):
        pygame.init()

        self.world = world

        self.width = world.width * CELL_SIZE
        self.height = world.height * CELL_SIZE

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Polis")

        self.clock = pygame.time.Clock()

    def draw_grid(self):
        for x in range(self.world.width):
            for y in range(self.world.height):
                rect = pygame.Rect(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                )

                pygame.draw.rect(
                    self.screen,
                    GRID_COLOR,
                    rect,
                    1,
                )

    def draw_agents(self):
        for agent in self.world.agents:
            rect = pygame.Rect(
                agent.x * CELL_SIZE,
                agent.y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )

            pygame.draw.rect(
                self.screen,
                AGENT_COLOR,
                rect,
            )

    def render(self):
        self.screen.fill(BACKGROUND)

        self.draw_grid()
        self.draw_agents()

        pygame.display.flip()

        self.clock.tick(10)