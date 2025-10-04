```python
from collections import deque
import copy
from typing import List, Tuple

directions4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions8 = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]

def find_components(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    for i in range(h):
        for j in range(w):
            if g[i][j] == 1 and not visited[i][j]:
                comp = []
                q = deque([(i, j)])
                visited[i][j] = True
                comp.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions4:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 1 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            comp.append((nx, ny))
                components.append(comp)
    return components

def detect_holes(g: List[List[int]], component: List[Tuple[int, int]], components: List[List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    h, w = len(g), len(g[0])
    temp = copy.deepcopy(g)
    for other_comp in components:
        if other_comp is not component:
            for x, y in other_comp:
                temp[x][y] = 4
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for i in range(h):
        for j in [0, w - 1]:
            if temp[i][j] == 4 and not visited[i][j]:
                visited[i][j] = True
                q.append((i, j))
    for j in range(1, w - 1):
        for i in [0, h - 1]:
            if temp[i][j] == 4 and not visited[i][j]:
                visited[i][j] = True
                q.append((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in directions4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and temp[nx][ny] == 4 and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append((nx, ny))
    holes = []
    for i in range(h):
        for j in range(w):
            if temp[i][j] == 4 and not visited[i][j]:
                holes.append((i, j))
    return holes

def add_borders(output_grid: List[List[int]], shape_positions: List[Tuple[int, int]]) -> None:
    h, w = len(output_grid), len(output_grid[0])
    for x, y in shape_positions:
        for dx, dy in directions8:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and output_grid[nx][ny] == 4:
                output_grid[nx][ny] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    output = copy.deepcopy(g)
    components = find_components(g)
    all_shape_pos = []
    for comp in components:
        all_shape_pos.extend(comp)
        holes = detect_holes(g, comp, components)
        if holes:
            for x, y in comp:
                output[x][y] = 8
            for x, y in holes:
                output[x][y] = 6
    add_borders(output, all_shape_pos)
    return output
```