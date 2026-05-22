"""
Simulation metrics: collect per-tick stats and print a rich summary table.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table

from polis.utils.logger import get_logger

if TYPE_CHECKING:
    from polis.env.world import World

log = get_logger(__name__)
_console = Console()


@dataclass
class TickSnapshot:
    tick: int
    agent_count: int
    food_count: int
    avg_energy: float
    min_energy: float
    max_energy: float
    deaths_this_tick: int
    food_eaten_this_tick: int


@dataclass
class SimMetrics:
    snapshots: list[TickSnapshot] = field(default_factory=list)
    total_deaths: int = 0
    total_food_eaten: int = 0
    total_births: int = 0

    # internal bookkeeping (set by World before update())
    _prev_agent_count: int = 0
    _food_eaten_this_tick: int = 0

    def record(self, tick: int, world: "World"):
        agents = world.agents
        n = len(agents)

        if n == 0:
            avg_e = min_e = max_e = 0.0
        else:
            energies = [a.energy for a in agents]
            avg_e = sum(energies) / n
            min_e = min(energies)
            max_e = max(energies)

        deaths = max(0, self._prev_agent_count - n)
        births = max(0, n - self._prev_agent_count + deaths)  # net change + deaths
        self.total_deaths += deaths
        self.total_births += births
        self.total_food_eaten += self._food_eaten_this_tick

        snap = TickSnapshot(
            tick=tick,
            agent_count=n,
            food_count=len(world.foods),
            avg_energy=avg_e,
            min_energy=min_e,
            max_energy=max_e,
            deaths_this_tick=deaths,
            food_eaten_this_tick=self._food_eaten_this_tick,
        )
        self.snapshots.append(snap)

        # log every tick at DEBUG, summarise every 50 at INFO
        log.debug(
            f"tick={tick:>5} | agents={n:>4} | food={len(world.foods):>4} "
            f"| avg_e={avg_e:>6.1f} | births={births} | deaths={deaths} | eaten={self._food_eaten_this_tick}"
        )

        if tick % 50 == 0:
            log.info(
                f"[bold]Tick {tick}[/bold] — "
                f"agents=[cyan]{n}[/cyan]  "
                f"food=[yellow]{len(world.foods)}[/yellow]  "
                f"avg_energy=[green]{avg_e:.1f}[/green]  "
                f"births=[blue]{self.total_births}[/blue]  "
                f"total_deaths=[red]{self.total_deaths}[/red]"
            )

        # reset transient counters
        self._prev_agent_count = n
        self._food_eaten_this_tick = 0

    def print_summary(self, ticks_run: int):
        """Print a final summary table to the terminal."""
        if not self.snapshots:
            log.warning("No snapshots to summarise.")
            return

        last = self.snapshots[-1]
        peak = max(s.agent_count for s in self.snapshots)
        lowest = min(s.agent_count for s in self.snapshots)

        table = Table(title=f"Polis — Final Summary ({ticks_run} ticks)", show_lines=True)
        table.add_column("Metric", style="bold cyan")
        table.add_column("Value", style="white")

        table.add_row("Ticks run", str(ticks_run))
        table.add_row("Agents alive (final)", str(last.agent_count))
        table.add_row("Peak population", str(peak))
        table.add_row("Lowest population", str(lowest))
        table.add_row("Total births", str(self.total_births))
        table.add_row("Total deaths", str(self.total_deaths))
        table.add_row("Total food eaten", str(self.total_food_eaten))
        table.add_row("Food remaining", str(last.food_count))
        table.add_row("Avg energy (final)", f"{last.avg_energy:.1f}")

        _console.print(table)