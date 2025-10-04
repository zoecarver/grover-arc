```python
from typing import List
from collections import Counter, deque

def fill_holes(g: List[List[int]]) -> List[List[int]]:
    """Fill all 1's with the nearest non-1 color using multi-source BFS."""
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    grid = [row[:] for row in g]
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for i in range(h):
        for j in range(w):
            if grid[i][j] != 1:
                q.append((i, j, grid[i][j]))
                visited[i][j] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y, color = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and grid[nx][ny] == 1:
                grid[nx][ny] = color
                visited[nx][ny] = True
                q.append((nx, ny, color))
    return grid

def compute_mode(lst: List[int]) -> int:
    """Compute mode ignoring 0."""
    count = Counter(x for x in lst if x != 0)
    if not count:
        return 0
    return max(count, key=count.get)

def find_vertical_stripes(g: List[List[int]]) -> List[tuple]:
    """Group consecutive columns with the same mode (ignoring 0)."""
    if not g or not g[0]:
        return []
    n_rows = len(g)
    n_cols = len(g[0])
    stripes = []
    i = 0
    while i < n_cols:
        col = [g[r][i] for r in range(n_rows)]
        mode = compute_mode(col)
        start = i
        i += 1
        while i < n_cols:
            next_col = [g[r][i] for r in range(n_rows)]
            next_mode = compute_mode(next_col)
            if next_mode != mode:
                break
            i += 1
        width = i - start
        stripes.append((start, width, mode))
    return stripes

def subdivide_stripe_vertically(g: List[List[int]], start_col: int, end_col: int) -> List[tuple]:
    """Group consecutive rows within the stripe columns with the same row segment mode (ignoring 0)."""
    n_rows = len(g)
    subblocks = []
    i = 0
    while i < n_rows:
        row_segment = [g[i][j] for j in range(start_col, end_col)]
        mode = compute_mode(row_segment)
        start_row = i
        i += 1
        while i < n_rows:
            next_segment = [g[i][j] for j in range(start_col, end_col)]
            next_mode = compute_mode(next_segment)
            if next_mode != mode:
                break
            i += 1
        height = i - start_row
        subblocks.append((start_row, height, mode))
    return subblocks

def build_blocky_grid(g: List[List[int]], stripes: List[tuple]) -> List[List[int]]:
    """Build the processed grid by filling sub-rectangles based on stripes and subblocks."""
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    out = [[0] * w for _ in range(h)]
    for start_col, width, _ in stripes:
        end_col = start_col + width
        subblocks = subdivide_stripe_vertically(g, start_col, end_col)
        for start_row, height, mode in subblocks:
            for r in range(start_row, start_row + height):
                for c in range(start_col, end_col):
                    out[r][c] = mode
    return out

def transpose(g: List[List[int]]) -> List[List[int]]:
    """Transpose the grid."""
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    filled = fill_holes(g)
    stripes = find_vertical_stripes(filled)
    processed = build_blocky_grid(filled, stripes)
    return transpose(processed)
```