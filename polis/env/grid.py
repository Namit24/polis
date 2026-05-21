from dataclasses import dataclass
@dataclass
class Cell:
    x: int
    y: int
    occupied: bool = False
    resource: int = 0


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.cells = [
            [Cell(x, y) for y in range(height)]
            for x in range(width)
        ]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[x][y]