```python
from typing import List
import copy
from collections import deque

def is_high(c: int) -> bool:
    return c > 4

def get_color(component_id: int) -> int:
    palette = [4, 3, 1, 2]
    return palette[component_id % len(palette)]

def flood_fill(h: List[List[int]], visited: List[List[int]], g: List[List[int]], start_i: int, start_j: int, color: int, size: int) -> None:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start_i, start_j)])
    visited[start_i][start_j] = True
    h[start_i][start_j] = color
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and is_high(g[nx][ny]) and not visited[nx][ny]:
                visited[nx][ny] = True
                h[nx][ny] = color
                queue.append((nx, ny))

def program(g: List[List[int]]) -> List[List[int]]:
    size = len(g)
    h = copy.deepcopy(g)
    visited = [[False] * size for _ in range(size)]
    component_id = 0
    for i in range(size):
        for j in range(size):
            if is_high(g[i][j]) and not visited[i][j]:
                color = get_color(component_id)
                flood_fill(h, visited, g, i, j, color, size)
                component_id += 1
    return h
```