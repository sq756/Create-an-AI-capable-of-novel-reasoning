from arc_solve.grid import Grid


def test_rotate_flip_transpose():
    grid = Grid.from_matrix([[1, 2], [3, 4]])
    assert grid.rotate90().to_matrix() == [[3, 1], [4, 2]]
    assert grid.flip_horizontal().to_matrix() == [[2, 1], [4, 3]]
    assert grid.flip_vertical().to_matrix() == [[3, 4], [1, 2]]
    assert grid.transpose().to_matrix() == [[1, 3], [2, 4]]


def test_pad_crop():
    grid = Grid.from_matrix([[1]])
    padded = grid.pad(top=1, bottom=1, left=1, right=1, color=0)
    assert padded.shape == (3, 3)
    cropped = padded.crop(1, 1, 1, 1)
    assert cropped.to_matrix() == [[1]]
