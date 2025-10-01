```python
from typing import List, Tuple
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def flood_fill_same(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    rows, cols = len(g), len(g[0])
    stack = deque([(sr, sc)])
    cells = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.popleft()
        if visited[x][y]:
            continue
        visited[x][y] = True
        if g[x][y] != color:
            continue
        cells.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                stack.append((nx, ny))
    return cells

def flood_fill_ge4(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]]) -> List[Tuple[int, int]]:
    rows, cols = len(g), len(g[0])
    stack = deque([(sr, sc)])
    cells = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.popleft()
        if visited[x][y]:
            continue
        visited[x][y] = True
        if g[x][y] < 4:
            continue
        cells.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] >= 4:
                stack.append((nx, ny))
    return cells

def count_holes(grid: List[List[int]], component_cells: List[Tuple[int, int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    is_barrier = [[False] * cols for _ in range(rows)]
    for r, c in component_cells:
        is_barrier[r][c] = True
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in (0, cols - 1):
            if not is_barrier[r][c] and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in range(cols):
        for r in (0, rows - 1):
            if not is_barrier[r][c] and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and not is_barrier[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
    hole_count = 0
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and not is_barrier[r][c] and grid[r][c] == 0:
                hole_count += 1
                qq = deque([(r, c)])
                visited[r][c] = True
                while qq:
                    x, y = qq.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and not is_barrier[nx][ny] and grid[nx][ny] == 0:
                            visited[nx][ny] = True
                            qq.append((nx, ny))
    return hole_count

def find_keys(g: List[List[int]]) -> List[dict]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    keys = []
    for r in range(rows):
        for c in range(cols):
            if 1 <= g[r][c] <= 4 and not visited[r][c]:
                color = g[r][c]
                cells = flood_fill_same(g, r, c, visited, color)
                if cells:
                    min_r = min(rr for rr, _ in cells)
                    max_r = max(rr for rr, _ in cells)
                    if max_r - min_r + 1 == 3:
                        h = count_holes(g, cells)
                        min_c = min(cc for _, cc in cells)
                        keys.append({'color': color, 'h': h, 'min_r': min_r, 'min_c': min_c})
    keys.sort(key=lambda d: (d['min_r'], d['min_c']))
    return keys

def program(g: List[List[int]]) -> List[List[int]]:
    keys = find_keys(g)
    rows, cols = len(g), len(g[0])
    out_grid = copy_grid(g)
    visited = [[False] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] >= 4 and not visited[r][c]:
                cells = flood_fill_ge4(g, r, c, visited)
                if cells:
                    min_r = min(rr for rr, _ in cells)
                    max_r = max(rr for rr, _ in cells)
                    height = max_r - min_r + 1
                    all_low = all(g[rr][cc] <= 4 for rr, cc in cells)
                    if not (height == 3 and all_low):
                        h = count_holes(g, cells)
                        if h < len(keys):
                            colr = keys[h]['color']
                            for rr, cc in cells:
                                out_grid[rr][cc] = colr
                        else:
                            for rr, cc in cells:
                                out_grid[rr][cc] = 0
    return out_grid
```