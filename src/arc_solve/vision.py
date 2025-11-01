"""Image level utilities used by the rule based solvers."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple

from .grid import Color, Grid


@dataclass(frozen=True)
class Component:
    color: Color
    pixels: Tuple[Tuple[int, int], ...]
    bounding_box: Tuple[int, int, int, int]

    @property
    def area(self) -> int:
        return len(self.pixels)


_OFFSETS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _neighbors(r: int, c: int, height: int, width: int) -> Iterable[Tuple[int, int]]:
    for dr, dc in _OFFSETS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc


def find_components(grid: Grid) -> List[Component]:
    height, width = grid.shape
    visited = [[False] * width for _ in range(height)]
    components: List[Component] = []
    for r in range(height):
        for c in range(width):
            if visited[r][c]:
                continue
            color = grid[r][c]
            queue: deque[Tuple[int, int]] = deque([(r, c)])
            pixels: List[Tuple[int, int]] = []
            visited[r][c] = True
            while queue:
                cr, cc = queue.popleft()
                pixels.append((cr, cc))
                for nr, nc in _neighbors(cr, cc, height, width):
                    if not visited[nr][nc] and grid[nr][nc] == color:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
            rows = [p[0] for p in pixels]
            cols = [p[1] for p in pixels]
            bbox = (min(rows), min(cols), max(rows) + 1, max(cols) + 1)
            components.append(
                Component(color=color, pixels=tuple(pixels), bounding_box=bbox)
            )
    return components


def render_component(component: Component, target_shape: Tuple[int, int]) -> Grid:
    height, width = target_shape
    matrix = [[0 for _ in range(width)] for _ in range(height)]
    top, left, bottom, right = component.bounding_box
    comp_height = bottom - top
    comp_width = right - left

    if comp_height > height or comp_width > width:
        # component does not fit, fallback to origin aligned crop
        rows = min(comp_height, height)
        cols = min(comp_width, width)
    else:
        rows = comp_height
        cols = comp_width

    row_offset = max((height - rows) // 2, 0)
    col_offset = max((width - cols) // 2, 0)

    for r, c in component.pixels:
        normalized_r = r - top
        normalized_c = c - left
        target_r = row_offset + normalized_r
        target_c = col_offset + normalized_c
        if 0 <= target_r < height and 0 <= target_c < width:
            matrix[target_r][target_c] = component.color
    return Grid.from_matrix(matrix)


def detect_symmetry(grid: Grid) -> Optional[str]:
    if grid == grid.flip_horizontal():
        return "vertical"
    if grid == grid.flip_vertical():
        return "horizontal"
    if grid == grid.transpose():
        return "diagonal"
    if grid == grid.transpose().flip_horizontal():
        return "anti-diagonal"
    return None
