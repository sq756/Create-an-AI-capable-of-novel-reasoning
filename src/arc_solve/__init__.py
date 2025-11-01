"""Rule-based reasoning toolkit for the ARC Prize competition."""

from .dataset import Task, load_tasks
from .grid import Grid
from .pipeline import ReasoningEngine
from .solvers.base import SolverPipeline
from .solvers.rule_based import default_pipeline

__all__ = [
    "Grid",
    "Task",
    "load_tasks",
    "ReasoningEngine",
    "SolverPipeline",
    "default_pipeline",
]
