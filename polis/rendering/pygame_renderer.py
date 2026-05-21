import pygame


CELL_SIZE = 12

BACKGROUND = (15, 15, 20)
GRID_COLOR = (40, 40, 50)

FOOD_COLOR = (255, 180, 0)


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

    def draw_food(self):
        for food in self.world.foods:
            rect = pygame.Rect(
                food.x * CELL_SIZE,
                food.y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )

            pygame.draw.rect(
                self.screen,
                FOOD_COLOR,
                rect,
            )

    def draw_agents(self):
        for agent in self.world.agents:

            energy_ratio = max(
                0,
                min(agent.energy / 100, 1)
            )

            color = (
                0,
                int(255 * energy_ratio),
                180,
            )

            rect = pygame.Rect(
                agent.x * CELL_SIZE,
                agent.y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE,
            )

            pygame.draw.rect(
                self.screen,
                color,
                rect,
            )

    def render(self):
        self.screen.fill(BACKGROUND)

        self.draw_grid()
        self.draw_food()
        self.draw_agents()

        pygame.display.flip()

        self.clock.tick(10)