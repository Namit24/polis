import random
class BaseAgent:
    def __init__(self, agent_id: int, x: int, y: int):
        self.agent_id = agent_id

        self.x = x
        self.y = y

        self.health = 100
        self.energy = 100

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def random_action(self):
        return random.choice([
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ])