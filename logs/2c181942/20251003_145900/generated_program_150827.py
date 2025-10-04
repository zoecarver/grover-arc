```python
from collections import deque
from typing import List

def has_color(g: List[List[int]], c: int) -> bool:
    for row in g:
        if c in row:
            return True
    return False

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if has_color(g, 6):
        rows = len(new_g)
        cols = len(new_g[0]) if rows > 0 else 0
        for i in range(rows):
            for j in range(cols):
                if new_g[i][j] == 4:
                    new_g[i][j] = 8
    return new_g

def remove_small_blue_if_dark_red(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if not has_color(g, 7):
        return new_g
    rows = len(new_g)
    cols = len(new_g[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if new_g[i][j] == 1 and not visited[i][j]:
                q = deque([(i, j)])
                visited[i][j] = True
                component_pos = [(i, j)]
                size = 1
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and new_g[nx][ny] == 1:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            component_pos.append((nx, ny))
                            size += 1
                if size <= 2:
                    for px, py in component_pos:
                        new_g[px][py] = 8
    return new_g

def compact_to_top(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    rows = len(new_g)
    cols = len(new_g[0]) if rows > 0 else 0
    for j in range(cols):
        col_values = [new_g[i][j] for i in range(rows) if new_g[i][j] != 8]
        for i in range(rows):
            new_g[i][j] = col_values[i] if i < len(col_values) else 8
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    g = remove_yellow_if_pink(g)
    g = remove_small_blue_if_dark_red(g)
    g = compact_to_top(g)
    return g
```