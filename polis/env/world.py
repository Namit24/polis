import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from polis.agents.base_agent import BaseAgent
from polis.utils.logger import get_logger

if TYPE_CHECKING:
    from polis.simulation.metrics import SimMetrics

log = get_logger(__name__)


@dataclass
class Food:
    x: int
    y: int


class World:
    def __init__(
        self,
        width: int = 50,
        height: int = 50,
        num_agents: int = 50,
        num_food: int = 150,
        food_respawn_per_tick: int = 2,
        food_cap: int = 300,
        reproduce_threshold: int = 70,
        reproduce_cost: int = 40,
        reproduce_child_energy: int = 50,
        agent_cap: int = 200,
    ):
        self.width = width
        self.height = height
        self.food_respawn_per_tick = food_respawn_per_tick
        self.food_cap = food_cap
        self.reproduce_threshold = reproduce_threshold
        self.reproduce_cost = reproduce_cost
        self.reproduce_child_energy = reproduce_child_energy
        self.agent_cap = agent_cap
        self._next_agent_id: int = 0

        self.agents: list[BaseAgent] = []
        self.foods: list[Food] = []
        self.tick: int = 0
        self.metrics: "SimMetrics | None" = None

        self._spawn_agents(num_agents)
        self._spawn_food(num_food)
        log.info(f"World initialised — size={width}x{height} agents={num_agents} food={num_food} respawn={food_respawn_per_tick}/tick cap={food_cap}")

    # ------------------------------------------------------------------
    # Init helpers
    # ------------------------------------------------------------------

    def _spawn_agents(self, n: int):
        for _ in range(n):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.agents.append(BaseAgent(agent_id=self._next_agent_id, x=x, y=y))
            self._next_agent_id += 1

    def _spawn_food(self, n: int):
        for _ in range(n):
            self.foods.append(self._random_food())

    def _random_food(self) -> Food:
        return Food(
            x=random.randint(0, self.width - 1),
            y=random.randint(0, self.height - 1),
        )

    # ------------------------------------------------------------------
    # Per-tick logic
    # ------------------------------------------------------------------

    def update(self):
        if self.metrics:
            self.metrics._prev_agent_count = len(self.agents)

        self._move_agents()
        self._consume_food()
        self._drain_energy()
        self._kill_dead_agents()
        self._reproduce()
        self._respawn_food()

        self.tick += 1

        if self.metrics:
            self.metrics.record(self.tick, self)

    def _move_agents(self):
        for agent in self.agents:
            dx, dy = agent.seek_action(self.foods)
            agent.x = max(0, min(self.width - 1, agent.x + dx))
            agent.y = max(0, min(self.height - 1, agent.y + dy))

    def _consume_food(self):
        food_positions = {(f.x, f.y): f for f in self.foods}
        eaten: list[Food] = []

        for agent in self.agents:
            food = food_positions.get((agent.x, agent.y))
            if food and food not in eaten:
                agent.energy = min(100, agent.energy + 30)
                eaten.append(food)

        for f in eaten:
            self.foods.remove(f)

        if self.metrics:
            self.metrics._food_eaten_this_tick = len(eaten)

    def _drain_energy(self):
        for agent in self.agents:
            agent.energy -= 1  # 1 energy per tick

    def _kill_dead_agents(self):
        self.agents = [a for a in self.agents if a.energy > 0]

    def _reproduce(self):
        if len(self.agents) >= self.agent_cap:
            return

        # build a set of occupied positions for quick lookup
        occupied = {(a.x, a.y) for a in self.agents}
        children: list[BaseAgent] = []

        for agent in self.agents:
            if agent.energy < self.reproduce_threshold:
                continue
            if len(self.agents) + len(children) >= self.agent_cap:
                break

            # find a free adjacent cell for the child
            offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            random.shuffle(offsets)
            child_pos = None
            for dx, dy in offsets:
                cx = max(0, min(self.width - 1, agent.x + dx))
                cy = max(0, min(self.height - 1, agent.y + dy))
                if (cx, cy) not in occupied:
                    child_pos = (cx, cy)
                    break

            if child_pos is None:
                continue  # surrounded, skip

            # pay the cost, spawn child
            agent.energy -= self.reproduce_cost
            child = BaseAgent(
                agent_id=self._next_agent_id,
                x=child_pos[0],
                y=child_pos[1],
            )
            child.energy = self.reproduce_child_energy
            self._next_agent_id += 1
            children.append(child)
            occupied.add(child_pos)

        if children:
            self.agents.extend(children)
            log.debug(f"tick={self.tick} | reproduction: +{len(children)} children")

    def _respawn_food(self):
        slots = self.food_cap - len(self.foods)
        for _ in range(min(self.food_respawn_per_tick, slots)):
            self.foods.append(self._random_food())