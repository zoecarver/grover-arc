```python
from typing import List, Optional, Tuple, Set

def get_type_and_color(trigger_value: int) -> Tuple[Optional[str], int]:
    """Maps trigger values to shape type and output color."""
    mapping = {
        2: ('rectangle', 4),
        3: ('diamond', 1),
        5: ('z', 6),
        7: ('anti_diamond', 7),
        8: ('anti_diamond', 7)
    }
    return mapping.get(trigger_value, (None, 0))

def get_pattern_positions(shape_type: str) -> Set[Tuple[int, int]]:
    """Returns the set of relative positions for the given shape type."""
    patterns = {
        'rectangle': {
            (0, 0), (0, 1), (0, 2), (0, 3),
            (3, 0), (3, 1), (3, 2), (3, 3),
            (1, 0), (1, 3), (2, 0), (2, 3)
        },
        'diamond': {
            (0, 1), (0, 2),
            (3, 1), (3, 2),
            (1, 0), (1, 3),
            (2, 0), (2, 3)
        },
        'z': {
            (0, 0), (0, 1),
            (1, 0), (1, 1),
            (2, 2), (2, 3),
            (3, 2), (3, 3)
        },
        'anti_diamond': {
            (0, 0), (0, 3),
            (3, 0), (3, 3),
            (1, 1), (1, 2),
            (2, 1), (2, 2)
        }
    }
    return patterns.get(shape_type, set())

def is_valid_block(grid: List[List[int]], start_row: int, start_col: int, pattern: Set[Tuple[int, int]]) -> bool:
    """Validates that the 4x4 block has no non-zero values outside the pattern positions (except at (0,0))."""
    for di in range(4):
        for dj in range(4):
            row, col = start_row + di, start_col + dj
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != 0:
                rel_pos = (di, dj)
                if rel_pos != (0, 0) and rel_pos not in pattern:
                    return False
    return True

def fill_shape_in_output(output: List[List[int]], start_row: int, start_col: int, pattern: Set[Tuple[int, int]], color: int) -> None:
    """Fills the pattern positions in the output grid with the given color."""
    for di, dj in pattern:
        row, col = start_row + di, start_col + dj
        if 0 <= row < len(output) and 0 <= col < len(output[0]):
            output[row][col] = color

def process_position(grid: List[List[int]], output: List[List[int]], i: int, j: int, n: int) -> None:
    """Processes a single potential starting position for shape detection and filling."""
    trigger = grid[i][j]
    shape_type, color = get_type_and_color(trigger)
    if shape_type is None:
        return
    pattern = get_pattern_positions(shape_type)
    if not is_valid_block(grid, i, j, pattern):
        return
    fill_shape_in_output(output, i, j, pattern, color)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: Initializes output to zeros and processes all possible 4x4 starting positions."""
    n = len(g)
    output = [[0] * n for _ in range(n)]
    for i in range(n - 3):
        for j in range(n - 3):
            process_position(g, output, i, j, n)
    return output
```