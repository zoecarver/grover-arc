```python
from typing import List, Tuple
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def flood_fill_same(g: List[List[int]], sr: int, sc: int, visited: List[List[bool]], color: int) -> List[Tuple[int, int]]:
    rows, cols = len(g), len(g[0])
    stack = deque([(sr, sc)])
    visited[sr][sc] = True
    cells = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        x, y = stack.popleft()
        if g[x][y] != color:
            continue
        cells.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                visited[nx][ny] = True
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

def find_all_low_components(g: List[List[int]]) -> List[dict]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if 1 <= g[r][c] <= 4 and not visited[r][c]:
                color = g[r][c]
                cells = flood_fill_same(g, r, c, visited, color)
                if cells:
                    min_r = min(rr for rr, _ in cells)
                    min_c = min(cc for _, cc in cells)
                    size = len(cells)
                    num_holes = count_holes(g, cells)
                    components.append({
                        'color': color,
                        'holes': num_holes,
                        'min_r': min_r,
                        'min_c': min_c,
                        'size': size
                    })
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    low_comps = find_all_low_components(g)
    low_comps.sort(key=lambda d: (d['size'], d['min_r'], d['min_c']))
    mapping = {}
    for comp in low_comps:
        h = comp['holes']
        if h not in mapping:
            mapping[h] = comp['color']
    rows, cols = len(g), len(g[0])
    high_visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] > 4 and not high_visited[r][c]:
                blob_cells = []
                stack = deque([(r, c)])
                high_visited[r][c] = True
                while stack:
                    x, y = stack.popleft()
                    blob_cells.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not high_visited[nx][ny] and g[nx][ny] > 4:
                            high_visited[nx][ny] = True
                            stack.append((nx, ny))
                if blob_cells:
                    h = count_holes(g, blob_cells)
                    new_col = mapping.get(h, 0)
                    for rx, cx in blob_cells:
                        out[rx][cx] = new_col
    return out
```