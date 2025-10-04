```python
from typing import List
from collections import deque

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def remove_small_components(g: List[List[int]], bg: int) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    grid = [row[:] for row in g]
    visited = [[False] * cols for _ in range(rows)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def component_size(start_r: int, start_c: int, color: int) -> List[tuple]:
        component = []
        queue = deque([(start_r, start_c)])
        visited[start_r][start_c] = True
        while queue:
            x, y = queue.popleft()
            component.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                    visited[nx][ny] = True
                    queue.append((nx, ny))
        return component

    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and grid[i][j] != bg:
                comp = component_size(i, j, grid[i][j])
                if len(comp) <= 4:
                    for x, y in comp:
                        grid[x][y] = bg
    return grid

def get_pattern(c: int, bg: int) -> List[int]:
    if c == 8:
        return [0, 2, 4, 6, 8, 10]
    elif c == 4:
        return [0, 6, 8, 10]
    elif c in (1, 2):
        if bg == 3:
            return [0, 6, 8, 10] if c == 1 else []
        else:
            return [0, 8, 10]
    else:
        return []

def complete_u_shapes(g: List[List[int]], bg: int) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    grid = [row[:] for row in g]
    start_r = 0
    while start_r < rows - 4:
        found = False
        for s in range(1, cols - 10):
            c = grid[start_r][s]
            if c == bg:
                continue
            # check isolated solid top
            top_solid = all(grid[start_r][s + k] == c for k in range(11))
            if not top_solid:
                continue
            if s > 0 and grid[start_r][s - 1] != bg:
                continue
            if s + 11 < cols and grid[start_r][s + 11] != bg:
                continue
            # count consecutive thin rows
            n = 0
            r = start_r + 1
            while r < rows:
                is_thin = (grid[r][s] == c and grid[r][s + 10] == c and
                           all(grid[r][s + k] == bg for k in range(1, 10)))
                if not is_thin:
                    break
                n += 1
                r += 1
            # check if next is isolated solid bottom
            if r >= rows:
                continue
            bottom_solid = all(grid[r][s + k] == c for k in range(11))
            if not bottom_solid:
                continue
            if (r > 0 and grid[r][s - 1] != bg if s > 0 else False) or \
               (r + 1 < rows and grid[r][s - 1] != bg if s > 0 else False):
                continue  # not isolated, skip
            if (s > 0 and grid[r][s - 1] != bg) or (s + 11 < cols and grid[r][s + 11] != bg):
                continue
            # found U with n thin rows, bottom at r
            found = True
            bottom_r = r
            middle_r = start_r + 2
            if n < 3:
                # complete: set current bottom to thin
                for k in range(1, 10):
                    grid[bottom_r][s + k] = bg
                # sides already c
                num_to_add = 3 - n
                for i in range(num_to_add):
                    inner_r = bottom_r + i
                    # ensure within bounds
                    if inner_r >= rows:
                        break
                    # set to thin
                    grid[inner_r][s] = c
                    grid[inner_r][s + 10] = c
                    for k in range(1, 10):
                        grid[inner_r][s + k] = bg
                    # set non-shape cols to bg
                    for j in range(cols):
                        if not (s <= j <= s + 10):
                            grid[inner_r][j] = bg
                # new bottom
                new_bottom_r = bottom_r + num_to_add
                if new_bottom_r < rows:
                    for k in range(11):
                        grid[new_bottom_r][s + k] = c
                    for j in range(cols):
                        if not (s <= j <= s + 10):
                            grid[new_bottom_r][j] = bg
                    middle_r = start_r + 2  # remains the same
                else:
                    # cannot extend, skip fill
                    start_r += 1
                    continue
            else:
                # n >= 3, assume 3, no extension
                pass
            # fill middle row
            pat = get_pattern(c, bg)
            for rel in pat:
                if s + rel < cols:
                    grid[middle_r][s + rel] = c
            # skip to after this shape
            start_r = max(start_r, new_bottom_r if 'new_bottom_r' in locals() else bottom_r) + 1
            break  # only one per start_r
        if not found:
            start_r += 1
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    cleaned = remove_small_components(g, bg)
    completed = complete_u_shapes(cleaned, bg)
    return completed
```