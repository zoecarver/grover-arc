```python
from typing import List, Tuple, Optional
from collections import deque

def get_bg_color(g: List[List[int]]) -> int:
    return g[0][0]

def get_neighbors(y: int, x: int, h: int, w: int) -> List[Tuple[int, int]]:
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dy, dx in dirs:
        ny, nx = y + dy, x + dx
        if 0 <= ny < h and 0 <= nx < w:
            neighbors.append((ny, nx))
    return neighbors

def fill_small_components(g: List[List[int]]) -> None:
    h = len(g)
    w = len(g[0])
    bg = get_bg_color(g)
    visited = [[False] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != bg and not visited[i][j]:
                component = []
                queue = deque([(i, j)])
                visited[i][j] = True
                color = g[i][j]
                while queue:
                    cy, cx = queue.popleft()
                    component.append((cy, cx))
                    for ny, nx in get_neighbors(cy, cx, h, w):
                        if g[ny][nx] == color and not visited[ny][nx]:
                            visited[ny][nx] = True
                            queue.append((ny, nx))
                if len(component) <= 10:
                    for py, px in component:
                        g[py][px] = bg

def is_frame(g: List[List[int]], positions: List[Tuple[int, int]], bg: int) -> Optional[Tuple[int, int, int, int, int]]:
    if not positions:
        return None
    C = g[positions[0][0]][positions[0][1]]
    min_y = min(p[0] for p in positions)
    max_y = max(p[0] for p in positions)
    min_x = min(p[1] for p in positions)
    max_x = max(p[1] for p in positions)
    # Check top row full
    if any(g[min_y][j] != C for j in range(min_x, max_x + 1)):
        return None
    # Check bottom row full
    if any(g[max_y][j] != C for j in range(min_x, max_x + 1)):
        return None
    # Check inner rows: only sides C, others bg
    for y in range(min_y + 1, max_y):
        if g[y][min_x] != C or g[y][max_x] != C:
            return None
        for j in range(min_x + 1, max_x):
            if g[y][j] != bg:
                return None
    return (min_x, max_x, min_y, max_y, C)

def punch_frame(g: List[List[int]], min_x: int, max_x: int, min_y: int, max_y: int, C: int) -> None:
    inner_start_y = min_y + 1
    middle_y = inner_start_y + 1
    inner_start_x = min_x + 1
    inner_end_x = max_x - 1
    # Rightmost 2 odd relative positions: rel 5 and 7
    for rel in [5, 7]:
        x = inner_start_x + rel
        if x <= inner_end_x:
            g[middle_y][x] = C

def program(g: List[List[int]]) -> List[List[int]]:
    g = [row[:] for row in g]
    fill_small_components(g)
    h = len(g)
    w = len(g[0])
    bg = get_bg_color(g)
    visited = [[False] * w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != bg and not visited[i][j]:
                component = []
                queue = deque([(i, j)])
                visited[i][j] = True
                color = g[i][j]
                while queue:
                    cy, cx = queue.popleft()
                    component.append((cy, cx))
                    for ny, nx in get_neighbors(cy, cx, h, w):
                        if g[ny][nx] == color and not visited[ny][nx]:
                            visited[ny][nx] = True
                            queue.append((ny, nx))
                if len(component) > 10:
                    frame_info = is_frame(g, component, bg)
                    if frame_info:
                        min_x, max_x, min_y, max_y, C = frame_info
                        punch_frame(g, min_x, max_x, min_y, max_y, C)
    return g
```