from dataclasses import dataclass


@dataclass
class Food:
    x: int
    y: int
    energy: int = 25