```python
from typing import List, Tuple

def find_eight_bounds(g: List[List[int]]) -> Tuple[int, int, int, int]:
    """Finds the bounding box of all 8's in the grid."""
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

def get_dimensions(min_row: int, max_row: int, min_col: int, max_col: int) -> Tuple[int, int]:
    """Computes height and width from bounds."""
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return height, width

def extract_adjacent(g: List[List[int]], min_row: int, height: int, min_col: int, width: int, max_col: int) -> List[List[int]]:
    """Extracts the adjacent subgrid to the left if possible, else to the right, with padding if necessary."""
    if min_col >= width:
        start_col = min_col - width
        subgrid = [row[start_col:start_col + width] for row in g[min_row:min_row + height]]
    else:
        start_col = max_col + 1
        subgrid = [row[start_col:start_col + width] for row in g[min_row:min_row + height]]
        # Pad with 9's if out of bounds
        for row in subgrid:
            if len(row) < width:
                row.extend([9] * (width - len(row)))
    return subgrid

def make_symmetric(subgrid: List[List[int]]) -> List[List[int]]:
    """Makes each row of the subgrid horizontally symmetric by copying left to right."""
    height = len(subgrid)
    if height == 0:
        return subgrid
    width = len(subgrid[0])
    for i in range(height):
        for j in range(width // 2):
            subgrid[i][width - 1 - j] = subgrid[i][j]
    return subgrid

def program(g: List[List[int]]) -> List[List[int]]:
    """Main function to process the grid and generate the output."""
    min_row, max_row, min_col, max_col = find_eight_bounds(g)
    height, width = get_dimensions(min_row, max_row, min_col, max_col)
    subgrid = extract_adjacent(g, min_row, height, min_col, width, max_col)
    subgrid = make_symmetric(subgrid)
    return subgrid
```