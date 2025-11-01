"""Dataset loading utilities for ARC style JSON files."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

from .grid import Grid, as_grid


@dataclass(frozen=True)
class Pair:
    input: Grid
    output: Grid


@dataclass(frozen=True)
class Task:
    task_id: str
    train: Sequence[Pair]
    test: Sequence[Grid]


def load_tasks(path: Path | str) -> Dict[str, Task]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    tasks: Dict[str, Task] = {}
    for task_id, content in data.items():
        train_pairs: List[Pair] = [
            Pair(input=as_grid(pair["input"]), output=as_grid(pair["output"]))
            for pair in content["train"]
        ]
        test_grids: List[Grid] = [as_grid(item["input"]) for item in content["test"]]
        tasks[task_id] = Task(task_id=task_id, train=train_pairs, test=test_grids)
    return tasks


def iter_tasks(paths: Sequence[Path | str]) -> Iterable[Task]:
    for path in paths:
        yield from load_tasks(path).values()
