import random

from polis.env.grid import Grid
from polis.agents.base_agent import BaseAgent
from polis.env.resources import Food


class World:
    def __init__(
        self,
        width=50,
        height=50,
        num_agents=20,
        food_count=40,
    ):
        self.grid = Grid(width, height)

        self.width = width
        self.height = height

        self.agents = []
        self.foods = []

        self.spawn_agents(num_agents)
        self.spawn_food(food_count)

    def spawn_agents(self, num_agents: int):
        for i in range(num_agents):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            self.agents.append(
                BaseAgent(i, x, y)
            )

    def spawn_food(self, food_count: int):
        for _ in range(food_count):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            self.foods.append(Food(x, y))

    def update(self):
        alive_agents = []

        for agent in self.agents:

            # energy drain
            agent.energy -= 1

            if agent.energy <= 0:
                continue

            dx, dy = agent.random_action()

            new_x = agent.x + dx
            new_y = agent.y + dy

            if self.grid.in_bounds(new_x, new_y):
                agent.move(dx, dy)

            # check food collision
            eaten_food = None

            for food in self.foods:
                if food.x == agent.x and food.y == agent.y:
                    agent.energy += food.energy
                    eaten_food = food
                    break

            if eaten_food:
                self.foods.remove(eaten_food)

                # respawn new food
                self.spawn_food(1)

            alive_agents.append(agent)

        self.agents = alive_agents