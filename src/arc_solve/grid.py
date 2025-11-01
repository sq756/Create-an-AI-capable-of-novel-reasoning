"""Utility helpers for working with ARC grids.

The competition encodes each grid as a nested list of integers between 0 and 9.
This module provides a lightweight ``Grid`` data structure that exposes a
consistent API for working with grids and a collection of common utility
functions that simplify spatial reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

Color = int
Matrix = List[List[Color]]


@dataclass(frozen=True)
class Grid:
    """Immutable wrapper around a matrix used throughout the solver.

    The wrapper guarantees rectangular shape and exposes convenience helpers
    for indexing, slicing and deriving statistics that are repeatedly used by
    the rule based solvers.
    """

    cells: Tuple[Tuple[Color, ...], ...]

    def __post_init__(self) -> None:
        if not self.cells:
            raise ValueError("Grid cannot be empty")
        width = len(self.cells[0])
        if width == 0:
            raise ValueError("Grid rows must not be empty")
        for row in self.cells:
            if len(row) != width:
                raise ValueError("Grid must be rectangular")
            for value in row:
                if not 0 <= value <= 9:
                    raise ValueError("Colors must be between 0 and 9 inclusive")

    @property
    def height(self) -> int:
        return len(self.cells)

    @property
    def width(self) -> int:
        return len(self.cells[0])

    @property
    def shape(self) -> Tuple[int, int]:
        return self.height, self.width

    def to_matrix(self) -> Matrix:
        return [list(row) for row in self.cells]

    def flatten(self) -> List[Color]:
        return [value for row in self.cells for value in row]

    def count(self, color: Color) -> int:
        return sum(value == color for value in self.flatten())

    def unique_colors(self) -> List[Color]:
        return sorted(set(self.flatten()))

    def rotate90(self) -> "Grid":
        rotated = list(zip(*self.cells[::-1]))
        return Grid(tuple(tuple(row) for row in rotated))

    def flip_horizontal(self) -> "Grid":
        flipped = [row[::-1] for row in self.cells]
        return Grid(tuple(tuple(row) for row in flipped))

    def flip_vertical(self) -> "Grid":
        flipped = self.cells[::-1]
        return Grid(tuple(tuple(row) for row in flipped))

    def transpose(self) -> "Grid":
        transposed = list(zip(*self.cells))
        return Grid(tuple(tuple(row) for row in transposed))

    def crop(self, top: int, left: int, height: int, width: int) -> "Grid":
        if top < 0 or left < 0 or height <= 0 or width <= 0:
            raise ValueError("Invalid crop dimensions")
        rows = self.cells[top : top + height]
        return Grid(tuple(tuple(row[left : left + width]) for row in rows))

    def pad(self, top: int, bottom: int, left: int, right: int, color: Color) -> "Grid":
        new_height = self.height + top + bottom
        new_width = self.width + left + right
        padded: List[List[Color]] = [
            [color for _ in range(new_width)] for _ in range(new_height)
        ]
        for r in range(self.height):
            for c in range(self.width):
                padded[top + r][left + c] = self.cells[r][c]
        return Grid(tuple(tuple(row) for row in padded))

    def __getitem__(self, index: int) -> Tuple[Color, ...]:
        return self.cells[index]

    def __iter__(self) -> Iterable[Tuple[Color, ...]]:
        return iter(self.cells)

    @classmethod
    def from_matrix(cls, matrix: Sequence[Sequence[Color]]) -> "Grid":
        return cls(tuple(tuple(row) for row in matrix))


def as_grid(matrix: Sequence[Sequence[Color]]) -> Grid:
    if isinstance(matrix, Grid):
        return matrix
    return Grid.from_matrix(matrix)


def same_shape(*grids: Grid) -> bool:
    return all(grid.shape == grids[0].shape for grid in grids)
