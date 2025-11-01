"""Command line helpers for running the reasoning engine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from .dataset import load_tasks
from .pipeline import ReasoningEngine
from .solvers.base import SolverPipeline
from .solvers.rule_based import default_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ARC reasoning engine")
    parser.add_argument(
        "--challenges",
        type=Path,
        required=True,
        help="Path to a challenges JSON file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Where to store the generated submission",
    )
    return parser


def generate_submission(engine: ReasoningEngine, challenges: Path) -> Dict[str, Any]:
    tasks = load_tasks(challenges)
    submission: Dict[str, Any] = {}
    for task_id, task in tasks.items():
        predictions = engine.solve_task(task)
        attempts: List[Dict[str, List[List[int]]]] = []
        for prediction in predictions:
            if prediction is None:
                attempts.append({"attempt_1": [[0]], "attempt_2": [[0]]})
                continue
            matrix = prediction.to_matrix()
            attempts.append({"attempt_1": matrix, "attempt_2": matrix})
        submission[task_id] = attempts
    return submission


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    engine = ReasoningEngine(SolverPipeline(default_pipeline()))
    submission = generate_submission(engine, args.challenges)

    args.output.write_text(json.dumps(submission), encoding="utf-8")


if __name__ == "__main__":  # pragma: no cover
    main()
