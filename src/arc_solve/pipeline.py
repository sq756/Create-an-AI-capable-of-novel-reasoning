"""High level orchestration utilities."""

from __future__ import annotations

from typing import Dict, Iterable, List, Sequence

from .dataset import Task
from .grid import Grid
from .solvers.base import SolverPipeline


class ReasoningEngine:
    """Coordinates running solvers on tasks."""

    def __init__(self, pipeline: SolverPipeline):
        self.pipeline = pipeline

    def solve_task(self, task: Task) -> List[Grid | None]:
        train_inputs = [pair.input for pair in task.train]
        train_outputs = [pair.output for pair in task.train]
        predictions: List[Grid | None] = []
        for test in task.test:
            result = self.pipeline.run(train_inputs, train_outputs, test)
            predictions.append(result.successful_output())
        return predictions

    def solve_tasks(self, tasks: Iterable[Task]) -> Dict[str, List[Grid | None]]:
        return {task.task_id: self.solve_task(task) for task in tasks}
