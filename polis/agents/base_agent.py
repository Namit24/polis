import random
import math


ACTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


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
        return random.choice(ACTIONS)

    def seek_action(self, foods: list, radius: int = 8) -> tuple[int, int]:
        """
        Look for the nearest food item within `radius` cells.
        If found, step one cell toward it. Otherwise random walk.
        """
        best = None
        best_dist = float("inf")

        for food in foods:
            dx = food.x - self.x
            dy = food.y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < best_dist and abs(dx) <= radius and abs(dy) <= radius:
                best_dist = dist
                best = food

        if best is None:
            return self.random_action()

        dx = best.x - self.x
        dy = best.y - self.y

        # step one cell in the dominant axis toward food
        if abs(dx) >= abs(dy):
            return (1 if dx > 0 else -1, 0)
        else:
            return (0, 1 if dy > 0 else -1)