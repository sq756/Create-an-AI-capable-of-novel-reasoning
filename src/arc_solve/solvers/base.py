"""Common interfaces shared by all solvers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from ..grid import Grid


class Solver(Protocol):
    """Protocol for a solver that predicts outputs for given inputs."""

    name: str

    def solve(self, train_inputs: Iterable[Grid], train_outputs: Iterable[Grid], test: Grid) -> Grid | None:
        ...


@dataclass(frozen=True)
class Attempt:
    solver: str
    output: Grid | None


@dataclass
class SolverResult:
    attempts: list[Attempt]

    def successful_output(self) -> Grid | None:
        for attempt in self.attempts:
            if attempt.output is not None:
                return attempt.output
        return None

    def append(self, attempt: Attempt) -> None:
        self.attempts.append(attempt)


class SolverPipeline:
    """Executes solvers sequentially until one succeeds."""

    def __init__(self, solvers: Iterable[Solver]):
        self.solvers = list(solvers)

    def run(self, train_inputs: Iterable[Grid], train_outputs: Iterable[Grid], test: Grid) -> SolverResult:
        result = SolverResult(attempts=[])
        cached_inputs = tuple(train_inputs)
        cached_outputs = tuple(train_outputs)
        for solver in self.solvers:
            prediction = solver.solve(cached_inputs, cached_outputs, test)
            result.append(Attempt(solver=solver.name, output=prediction))
            if prediction is not None:
                break
        return result
