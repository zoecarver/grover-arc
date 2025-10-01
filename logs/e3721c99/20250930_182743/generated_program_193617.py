```python
from typing import List, Tuple
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def find_legends(g: List[List[int]]) -> List[dict]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if 1 <= g[r][c] <= 4 and not visited[r][c]:
                color = g[r][c]
                cells: List[Tuple[int, int]] = []
                stack = deque([(r, c)])
                visited[r][c] = True
                cells.append((r, c))
                min_r, max_r, min_c, max_c = r, r, c, c
                while stack:
                    x, y = stack.popleft()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            cells.append((nx, ny))
                            min_r = min(min_r, nx)
                            max_r = max(max_r, nx)
                            min_c = min(min_c, ny)
                            max_c = max(max_c, ny)
                height = max_r - min_r + 1
                if height == 3:
                    components.append({
                        'color': color,
                        'min_r': min_r,
                        'min_c': min_c,
                        'cells': cells
                    })
    components.sort(key=lambda comp: (comp['min_r'], comp['min_c']))
    return components

def find_blobs(g: List[List[int]]) -> List[dict]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] > 4 and not visited[r][c]:
                cells: List[Tuple[int, int]] = []
                stack = deque([(r, c)])
                visited[r][c] = True
                cells.append((r, c))
                while stack:
                    x, y = stack.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] > 4:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            cells.append((nx, ny))
                blobs.append({'cells': cells})
    return blobs

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
        if r in (0, rows - 1):
            for c in range(cols):
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

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    legends = find_legends(g)
    for blob_dict in find_blobs(g):
        cells = blob_dict['cells']
        h = count_holes(g, cells)
        if h < len(legends):
            col = legends[h]['color']
            for r, c in cells:
                out[r][c] = col
        else:
            for r, c in cells:
                out[r][c] = 0
    return out
```