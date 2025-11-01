"""Collection of light-weight heuristic solvers.

The objective is not to achieve state-of-the-art performance but to
provide a transparent baseline that demonstrates how the reasoning
pipeline is structured. Each solver encodes a single intuition and
returns ``None`` when the intuition does not apply.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable, List, Sequence

from ..grid import Grid, same_shape
from .base import Solver


@dataclass
class IdentitySolver:
    name: str = "identity"

    def solve(
        self,
        train_inputs: Iterable[Grid],
        train_outputs: Iterable[Grid],
        test: Grid,
    ) -> Grid | None:
        if not all(same_shape(inp, out) for inp, out in zip(train_inputs, train_outputs)):
            return None
        return test


@dataclass
class ConstantColorSolver:
    """Predicts a single color fill when demonstrations share that property."""

    name: str = "constant-color"

    def solve(
        self,
        train_inputs: Iterable[Grid],
        train_outputs: Iterable[Grid],
        test: Grid,
    ) -> Grid | None:
        outputs = list(train_outputs)
        if not outputs:
            return None
        if not all(len(set(out.flatten())) == 1 for out in outputs):
            return None
        fill_color = outputs[0].flatten()[0]
        return Grid.from_matrix([[fill_color for _ in range(test.width)] for _ in range(test.height)])


@dataclass
class MajorityColorSolver:
    """Fills the test grid with the most common color observed in outputs."""

    name: str = "majority-color"

    def solve(
        self,
        train_inputs: Iterable[Grid],
        train_outputs: Iterable[Grid],
        test: Grid,
    ) -> Grid | None:
        counter: Counter[int] = Counter()
        for output in train_outputs:
            counter.update(output.flatten())
        if not counter:
            return None
        color, frequency = counter.most_common(1)[0]
        if frequency == 0:
            return None
        return Grid.from_matrix([[color for _ in range(test.width)] for _ in range(test.height)])


@dataclass
class CopyLargestObjectSolver:
    """Replicates the largest connected component from training outputs."""

    name: str = "copy-largest-object"

    def solve(
        self,
        train_inputs: Iterable[Grid],
        train_outputs: Iterable[Grid],
        test: Grid,
    ) -> Grid | None:
        from ..vision import find_components, render_component

        components = []
        for output in train_outputs:
            components.extend(find_components(output))
        if not components:
            return None
        component = max(components, key=lambda comp: comp.area)
        return render_component(component, target_shape=test.shape)


@dataclass
class SymmetrySolver:
    """Copies the symmetric axis detected in demonstration outputs."""

    name: str = "symmetry"

    def solve(
        self,
        train_inputs: Iterable[Grid],
        train_outputs: Iterable[Grid],
        test: Grid,
    ) -> Grid | None:
        from ..vision import detect_symmetry

        axes = [detect_symmetry(output) for output in train_outputs]
        axes = [axis for axis in axes if axis is not None]
        if not axes:
            return None
        if len(set(axes)) != 1:
            return None
        axis = axes[0]
        # mirror the test grid around the detected axis
        if axis == "horizontal":
            return test.flip_vertical()
        if axis == "vertical":
            return test.flip_horizontal()
        if axis == "diagonal":
            return test.transpose()
        if axis == "anti-diagonal":
            return test.transpose().flip_horizontal()
        return None


def default_pipeline() -> List[Solver]:
    return [
        IdentitySolver(),
        ConstantColorSolver(),
        MajorityColorSolver(),
        SymmetrySolver(),
        CopyLargestObjectSolver(),
    ]
