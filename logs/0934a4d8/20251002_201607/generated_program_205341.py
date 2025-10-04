```python
from typing import List, Tuple

def find_eight_bounds(g: List[List[int]]) -> Tuple[int, int, int, int]:
    rows = len(g)
    if rows == 0:
        return 0, 0, 0, 0
    cols = len(g[0])
    eight_positions = [(i, j) for i in range(rows) for j in range(cols) if g[i][j] == 8]
    if not eight_positions:
        return 0, 0, 0, 0
    min_row = min(pos[0] for pos in eight_positions)
    max_row = max(pos[0] for pos in eight_positions)
    min_col = min(pos[1] for pos in eight_positions)
    max_col = max(pos[1] for pos in eight_positions)
    return min_row, max_row, min_col, max_col

def compute_dimensions(min_row: int, max_row: int, min_col: int, max_col: int) -> Tuple[int, int]:
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return height, width

def extract_top_left_subgrid(g: List[List[int]], height: int, width: int) -> List[List[int]]:
    return [row[:width] for row in g[:height]]

def program(g: List[List[int]]) -> List[List[int]]:
    min_row, max_row, min_col, max_col = find_eight_bounds(g)
    height, width = compute_dimensions(min_row, max_row, min_col, max_col)
    return extract_top_left_subgrid(g, height, width)
```