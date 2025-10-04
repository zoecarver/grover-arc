```python
from typing import List, Tuple

def replace_sevens(grid: List[List[int]]) -> List[List[int]]:
    # Rule: Replace all 7s with 4s, treating 7 as filled cells to be resolved.
    grid = [row[:] for row in grid]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 7:
                grid[i][j] = 4
    return grid

def get_vertical_blocks(grid: List[List[int]]) -> List[List[List[int]]]:
    # Observation: Separate the grid into vertical blocks divided by all-1 rows.
    blocks = []
    i = 0
    n = len(grid)
    while i < n:
        if all(x == 1 for x in grid[i]):
            i += 1
            continue
        start = i
        while i < n and not all(x == 1 for x in grid[i]):
            i += 1
        block = [row[:] for row in grid[start:i]]
        blocks.append(block)
    return blocks

def find_leftmost_component(grid: List[List[int]]) -> List[Tuple[int, int]]:
    # Rule: Extract the connected component of 4s attached to the left border (column 0).
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    comp = []
    for i in range(rows):
        if grid[i][0] == 4 and not visited[i][0]:
            stack = [(i, 0)]
            visited[i][0] = True
            comp.append((i, 0))
            while stack:
                x, y = stack.pop()
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 4 and not visited[nx][ny]:
                        visited[nx][ny] = True
                        stack.append((nx, ny))
                        comp.append((nx, ny))
    return comp

def get_largest_component(grid: List[List[int]]) -> List[Tuple[int, int]]:
    # Rule: If no left-connected component, extract the largest connected component of 4s.
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    max_comp = []
    max_size = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 4 and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                comp.append((i, j))
                size = 1
                while stack:
                    x, y = stack.pop()
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 4 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            comp.append((nx, ny))
                            size += 1
                if size > max_size:
                    max_size = size
                    max_comp = comp
    return max_comp

def crop_to_bounding(grid: List[List[int]], comp: List[Tuple[int, int]]) -> List[List[int]]:
    # Rule: Crop the grid to the minimal bounding box of the component positions.
    if not comp:
        return []
    min_r = min(r for r, c in comp)
    max_r = max(r for r, c in comp)
    min_c = min(c for r, c in comp)
    max_c = max(c for r, c in comp)
    return [[grid[r][c] for c in range(min_c, max_c + 1)] for r in range(min_r, max_r + 1)]

def fill_single_gaps_horizontal(grid: List[List[int]]) -> List[List[int]]:
    # Rule: Fill isolated single 1s sandwiched between 4s horizontally to close small cracks, only if grid is wide enough.
    grid = [row[:] for row in grid]
    rows = len(grid)
    if rows == 0:
        return grid
    c = len(grid[0])
    if c <= 3:
        return grid
    changed = True
    passes = 0
    max_passes = rows * c
    while changed and passes < max_passes:
        changed = False
        passes += 1
        for i in range(rows):
            for j in range(1, c - 1):
                if grid[i][j] == 1 and grid[i][j - 1] == 4 and grid[i][j + 1] == 4:
                    grid[i][j] = 4
                    changed = True
    return grid

def collapse_consecutive_all_four_rows(grid: List[List[int]]) -> List[List[int]]:
    # Rule: Collapse multiple consecutive all-4 rows into a single all-4 row to normalize vertical bars.
    result = []
    i = 0
    n = len(grid)
    while i < n:
        current_row = grid[i][:]
        if all(x == 4 for x in current_row):
            result.append(current_row)
            i += 1
            while i < n and all(x == 4 for x in grid[i]):
                i += 1
        else:
            result.append(current_row)
            i += 1
    return result

def pad_rows_to_width(rows: List[List[int]], target_width: int) -> List[List[int]]:
    # Observation: Pad shorter rows with 1s on the right to match the maximum width across blocks.
    padded = []
    for row in rows:
        padded_row = row[:] + [1] * (target_width - len(row))
        padded.append(padded_row)
    return padded

def program(g: List[List[int]]) -> List[List[int]]:
    grid = replace_sevens(g)
    blocks = get_vertical_blocks(grid)
    processed_blocks = []
    max_width = 0
    for block in blocks:
        comp = find_leftmost_component(block)
        if not comp:
            comp = get_largest_component(block)
        if not comp:
            continue
        sub = crop_to_bounding(block, comp)
        sub = fill_single_gaps_horizontal(sub)
        sub = collapse_consecutive_all_four_rows(sub)
        if sub:
            w = len(sub[0])
            max_width = max(max_width, w)
            processed_blocks.append(sub)
    if not processed_blocks:
        return []
    # Stack all processed blocks, padding to max_width
    output = []
    for sub in processed_blocks:
        padded_sub = pad_rows_to_width(sub, max_width)
        output.extend(padded_sub)
    return output
```