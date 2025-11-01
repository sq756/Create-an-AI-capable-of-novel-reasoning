from arc_solve.dataset import Pair, Task
from arc_solve.grid import Grid
from arc_solve.pipeline import ReasoningEngine
from arc_solve.solvers.base import SolverPipeline
from arc_solve.solvers.rule_based import default_pipeline


def test_reasoning_engine_identity():
    task = Task(
        task_id="example",
        train=[
            Pair(
                input=Grid.from_matrix([[1, 2], [3, 4]]),
                output=Grid.from_matrix([[1, 2], [3, 4]]),
            )
        ],
        test=[Grid.from_matrix([[5, 6], [7, 8]])],
    )
    engine = ReasoningEngine(SolverPipeline(default_pipeline()))
    predictions = engine.solve_task(task)
    assert predictions[0] == Grid.from_matrix([[5, 6], [7, 8]])
