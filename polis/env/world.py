import random
from polis.env.grid import Grid
from polis.agents.base_agent import BaseAgent


class World:
    def __init__(self, width=50, height=50, num_agents=20):
        self.grid = Grid(width, height)

        self.width = width
        self.height = height

        self.agents = []

        self.spawn_agents(num_agents)

    def spawn_agents(self, num_agents: int):
        for i in range(num_agents):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            agent = BaseAgent(i, x, y)

            self.agents.append(agent)

    def update(self):
        for agent in self.agents:
            dx, dy = agent.random_action()

            new_x = agent.x + dx
            new_y = agent.y + dy

            if self.grid.in_bounds(new_x, new_y):
                agent.move(dx, dy)