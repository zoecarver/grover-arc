```python
from typing import List, Tuple
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def count_blues(g: List[List[int]]) -> int:
    count = 0
    for row in g:
        count += sum(1 for cell in row if cell == 1)
    return count

def find_blue_component(g: List[List[int]]) -> List[Tuple[int, int]]:
    visited = [[False for _ in range(10)] for _ in range(10)]
    component = []
    queue = deque()
    found = False
    for r in range(10):
        for c in range(10):
            if g[r][c] == 1 and not visited[r][c]:
                queue.append((r, c))
                visited[r][c] = True
                found = True
                component.append((r, c))
                break
        if found:
            break
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        cr, cc = queue.popleft()
        for dr, dc in directions:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and not visited[nr][nc] and (g[nr][nc] == 0 or g[nr][nc] == 1):
                visited[nr][nc] = True
                queue.append((nr, nc))
                component.append((nr, nc))
    return component

def program(g: List[List[int]]) -> List[List[int]]:
    n = count_blues(g)
    component = find_blue_component(g)
    if len(component) < n:
        # If less positions than blues, fill all
        pass
    component.sort(key=lambda x: (-x[0], -x[1]))
    h = copy_grid(g)
    # Set all blues to 0
    for r in range(10):
        for c in range(10):
            if h[r][c] == 1:
                h[r][c] = 0
    # Fill the first n positions in sorted component
    for i in range(min(n, len(component))):
        r, c = component[i]
        h[r][c] = 1
    return h
```