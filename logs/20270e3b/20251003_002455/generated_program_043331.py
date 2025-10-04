```python
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    blocks = get_vertical_blocks(g)
    processed_blocks = []
    max_width = 0
    for block in blocks:
        processed = process_block(block)
        if processed:
            processed_blocks.append(processed)
            max_width = max(max_width, len(processed[0]))
    result = []
    for p in processed_blocks:
        padded = pad_to_width(p, max_width)
        result.extend(padded)
    return result

def get_vertical_blocks(g: List[List[int]]) -> List[List[List[int]]]:
    blocks = []
    i = 0
    n = len(g)
    while i < n:
        if all(x == 1 for x in g[i]):
            i += 1
            continue
        start = i
        while i < n and not all(x == 1 for x in g[i]):
            i += 1
        block = [row[:] for row in g[start:i]]
        blocks.append(block)
    return blocks

def process_block(block: List[List[int]]) -> List[List[int]]:
    if not block:
        return []
    h = len(block)
    w_input = len(block[0]) if h > 0 else 0
    temp = [row[:] for row in block]
    # Find main component treating 4 and 7 as filled
    component = find_left_touching_treat7(temp)
    if not component:
        component = get_largest_treat7(temp)
    if not component:
        return []
    min_c_main = min(c for r, c in component)
    max_c_main = max(c for r, c in component)
    w = max_c_main - min_c_main + 1
    new_grid = [[1] * w for _ in range(h)]
    main_set = set((r, c) for r, c in component)
    for r, c in component:
        new_grid[r][c - min_c_main] = 4
    # Find other small components of original 4s only
    original_temp = [row[:] for row in block]
    all_comps = find_all_components(original_temp)
    for comp in all_comps:
        if len(comp) >= 10:
            continue
        if all((r, c) in main_set for r, c in comp):
            continue
        min_c_comp = min(c for r, c in comp)
        max_c_comp = max(c for r, c in comp)
        span = max_c_comp - min_c_comp + 1
        sum_r = sum(r for r, c in comp)
        avg_r = sum_r / len(comp)
        row = round(avg_r)
        if 0 <= row < h:
            gap = min_c_comp - max_c_main - 1
            if gap > 0:
                start_col_new = w - gap - span
                if start_col_new >= 0:
                    for k in range(span):
                        sc = start_col_new + k
                        if sc < w:
                            new_grid[row][sc] = 4
    # Fill single horizontal gaps conditionally (handles observation of crack vs hole)
    new_grid = fill_single_gaps_conditional(new_grid)
    # Extend bars (handles observation of protrusion extension from horizontal bars)
    new_grid = extend_bars(new_grid)
    # Collapse consecutive all-4 rows (handles vertical normalization and consolidation)
    new_grid = collapse_all4_rows(new_grid)
    return new_grid

def find_left_touching_treat7(grid: List[List[int]]) -> List[Tuple[int, int]]:
    h = len(grid)
    if h == 0:
        return []
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    component = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        if grid[i][0] in (4, 7) and not visited[i][0]:
            stack = [(i, 0)]
            visited[i][0] = True
            component.append((i, 0))
            while stack:
                x, y = stack.pop()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] in (4, 7) and not visited[nx][ny]:
                        visited[nx][ny] = True
                        stack.append((nx, ny))
                        component.append((nx, ny))
    return component

def get_largest_treat7(grid: List[List[int]]) -> List[Tuple[int, int]]:
    h = len(grid)
    if h == 0:
        return []
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    max_comp = []
    max_size = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if grid[i][j] in (4, 7) and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                comp.append((i, j))
                size = 1
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] in (4, 7) and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            comp.append((nx, ny))
                            size += 1
                if size > max_size:
                    max_size = size
                    max_comp = comp
    return max_comp

def find_all_components(grid: List[List[int]]) -> List[List[Tuple[int, int]]]:
    h = len(grid)
    if h == 0:
        return []
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if grid[i][j] == 4 and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                comp.append((i, j))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == 4 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            comp.append((nx, ny))
                components.append(comp)
    return components

def fill_single_gaps_conditional(grid: List[List[int]]) -> List[List[int]]:
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    changed = True
    while changed:
        changed = False
        for i in range(h):
            for j in range(1, w - 1):
                if grid[i][j] == 1 and grid[i][j - 1] == 4 and grid[i][j + 1] == 4:
                    both_vertical_4 = (i > 0 and grid[i - 1][j] == 4) and (i < h - 1 and grid[i + 1][j] == 4)
                    if not both_vertical_4:
                        grid[i][j] = 4
                        changed = True
    return grid

def extend_bars(grid: List[List[int]]) -> List[List[int]]:
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    new_grid = [row[:] for row in grid]
    for i in range(h - 2):
        j = 0
        while j < w:
            if new_grid[i][j] == 4:
                start = j
                while j < w and new_grid[i][j] == 4:
                    j += 1
                end = j - 1
                length = end - start + 1
                if length < w and length > 2:
                    # Extend left end if not touching left
                    if start > 0:
                        col = start
                        for k in range(1, 3):
                            if i + k < h and new_grid[i + k][col] == 1:
                                new_grid[i + k][col] = 4
                    # Extend right end-1 if touching right
                    if end == w - 1:
                        col = end - 1
                        for k in range(1, 3):
                            if i + k < h and new_grid[i + k][col] == 1:
                                new_grid[i + k][col] = 4
                    # Extend right end if not touching right
                    else:
                        col = end
                        for k in range(1, 3):
                            if i + k < h and new_grid[i + k][col] == 1:
                                new_grid[i + k][col] = 4
            else:
                j += 1
    return new_grid

def collapse_all4_rows(grid: List[List[int]]) -> List[List[int]]:
    if not grid:
        return []
    result = []
    i = 0
    h = len(grid)
    while i < h:
        current = grid[i][:]
        if all(x == 4 for x in current):
            result.append(current)
            i += 1
            while i < h and all(x == 4 for x in grid[i]):
                i += 1
        else:
            result.append(current)
            i += 1
    return result

def pad_to_width(grid: List[List[int]], target: int) -> List[List[int]]:
    if not grid:
        return []
    padded = []
    for row in grid:
        padded_row = row[:] + [1] * (target - len(row))
        padded.append(padded_row)
    return padded
```