from arc_solve.grid import Grid
from arc_solve.vision import detect_symmetry, find_components, render_component


def test_find_components_returns_all_pixels():
    grid = Grid.from_matrix(
        [
            [1, 1, 0],
            [1, 0, 2],
            [0, 2, 2],
        ]
    )
    components = find_components(grid)
    total_area = sum(component.area for component in components)
    assert total_area == grid.height * grid.width


def test_detect_symmetry():
    vertical = Grid.from_matrix([[1, 0, 1], [2, 0, 2]])
    assert detect_symmetry(vertical) == "vertical"
    horizontal = Grid.from_matrix([[1, 2], [1, 2]])
    assert detect_symmetry(horizontal) == "horizontal"


def test_render_component_centering():
    grid = Grid.from_matrix(
        [
            [0, 0, 3],
            [0, 3, 3],
        ]
    )
    component = find_components(grid)[1]
    rendered = render_component(component, target_shape=(4, 4))
    assert rendered.count(3) == component.area
