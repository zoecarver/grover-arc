```python
from typing import List, Tuple

def find_eight_bounds(g: List[List[int]]) -> Tuple[int, int, int, int]:
    # Finds the bounding box of all 8s in the grid, assuming a single solid block
    rows = len(g)
    if rows == 0:
        return 0, 0, 0, 0
    cols = len(g[0])
    min_row = rows
    max_row = -1
    min_col = cols
    max_col = -1
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 8:
                min_row = min(min_row, i)
                max_row = max(max_row, i)
                min_col = min(min_col, j)
                max_col = max(max_col, j)
    if max_row == -1:
        return 0, 0, 0, 0
    return min_row, max_row, min_col, max_col

def get_block_dimensions(min_row: int, max_row: int, min_col: int, max_col: int) -> Tuple[int, int]:
    # Computes the height and width of the 8 block bounding box
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return height, width

def extract_adjacent_subgrid(g: List[List[int]], min_row: int, height: int, min_col: int, width: int) -> List[List[int]]:
    # Extracts a subgrid of size height x width adjacent to the 8 block
    # If block starts at column 0, extract to the right; otherwise to the left
    if min_col == 0:
        start_col = min_col + width  # Right of block
    else:
        start_col = min_col - width  # Left of block
    start_col = max(0, start_col)
    end_col = start_col + width
    subgrid = []
    for row in g[min_row : min_row + height]:
        sub_row = row[start_col : end_col]
        # Pad if necessary (right side out of bounds)
        if len(sub_row) < width:
            sub_row += [9] * (width - len(sub_row))
        subgrid.append(sub_row)
    return subgrid

def program(g: List[List[int]]) -> List[List[int]]:
    min_row, max_row, min_col, max_col = find_eight_bounds(g)
    height, width = get_block_dimensions(min_row, max_row, min_col, max_col)
    return extract_adjacent_subgrid(g, min_row, height, min_col, width)
```