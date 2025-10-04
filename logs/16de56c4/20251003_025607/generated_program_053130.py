```python
from collections import defaultdict
from typing import List

def process_line_inplace(l: List[int], n: int) -> None:
    """
    Processes a single line (row or column) by identifying exactly two positions of the same color,
    computing the distance d, and extending bidirectionally into zeros with the color c.
    On encountering a conflict (non-zero different color), overwrites the extended chain (including originals)
    with the conflicting color and stops extension in that direction.
    Handles pairs independently per color; ignores singles or groups larger than 2.
    Mutates l in place.
    """
    if n == 0:
        return
    pos_by_c = defaultdict(list)
    for i in range(n):
        if l[i] != 0:
            pos_by_c[l[i]].append(i)
    for c in list(pos_by_c.keys()):
        poss = pos_by_c[c]
        if len(poss) != 2:
            continue
        p1, p2 = sorted(poss)
        d = p2 - p1
        if d == 0:
            continue
        # Rightward extension (increasing indices)
        chain_right = {p1, p2}
        current = p2
        while True:
            nextp = current + d
            if nextp >= n:
                break
            if l[nextp] == 0 or l[nextp] == c:
                l[nextp] = c
                chain_right.add(nextp)
                current = nextp
            else:
                conflict_c = l[nextp]
                for pp in chain_right:
                    l[pp] = conflict_c
                break
        # Leftward extension (decreasing indices)
        chain_left = {p1, p2}
        current = p1
        while True:
            nextp = current - d
            if nextp < 0:
                break
            if l[nextp] == 0 or l[nextp] == c:
                l[nextp] = c
                chain_left.add(nextp)
                current = nextp
            else:
                conflict_c = l[nextp]
                for pp in chain_left:
                    l[pp] = conflict_c
                break

def apply_horizontal_transformations(grid: List[List[int]]) -> List[List[int]]:
    """
    Applies line processing to each row horizontally.
    Used when the grid is taller (more rows than columns).
    Returns a deep copy of the grid with transformations applied.
    """
    if not grid:
        return []
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    grid_copy = [row[:] for row in grid]
    for i in range(num_rows):
        process_line_inplace(grid_copy[i], num_cols)
    return grid_copy

def apply_vertical_transformations(grid: List[List[int]]) -> List[List[int]]:
    """
    Applies line processing to each column vertically.
    Extracts columns, processes, and reconstructs the grid.
    Used when the grid is wider (more columns than rows) or square.
    Returns a deep copy of the grid with transformations applied.
    """
    if not grid:
        return []
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0
    grid_copy = [row[:] for row in grid]
    for j in range(num_cols):
        col = [grid_copy[i][j] for i in range(num_rows)]
        process_line_inplace(col, num_rows)
        for i in range(num_rows):
            grid_copy[i][j] = col[i]
    return grid_copy

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main function to solve the puzzle.
    Determines processing direction based on grid aspect ratio:
    - Horizontal (rows) if more rows than columns.
    - Vertical (columns) otherwise.
    Composes the appropriate transformation functions.
    """
    if not g:
        return []
    num_rows = len(g)
    num_cols = len(g[0]) if num_rows > 0 else 0
    if num_rows > num_cols:
        return apply_horizontal_transformations(g)
    else:
        return apply_vertical_transformations(g)
```