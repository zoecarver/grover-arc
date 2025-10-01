```python
from typing import List
import copy
from collections import deque

def find_background(g: List[List[int]]) -> int:
    count = {}
    for row in g:
        for cell in row:
            count[cell] = count.get(cell, 0) + 1
    return max(count, key=count.get)

def extract_objects(g: List[List[int]], bg: int) -> List[List[Tuple[int, int, int]]]:
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    objects = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != bg and not visited[i][j]:
                color = g[i][j]
                component = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    component.append((x, y, color))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                objects.append(component)
    return objects

def remove_small_objects(g: List[List[int]], bg: int, min_size: int = 3) -> List[List[int]]:
    objects = extract_objects(g, bg)
    new_g = copy.deepcopy(g)
    for obj in objects:
        if len(obj) < min_size:
            for i, j, c in obj:
                new_g[i][j] = bg
    return new_g

def prune_protrusions(g: List[List[int]], bg: int, threshold: int = 2, max_iters: int = 2) -> List[List[int]]:
    h, w = len(g), len(g[0])
    new_g = copy.deepcopy(g)
    for _ in range(max_iters):
        changed = False
        temp_g = [row[:] for row in new_g]
        for i in range(h):
            for j in range(w):
                if new_g[i][j] == bg:
                    continue
                c = new_g[i][j]
                count = 0
                dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < h and 0 <= nj < w and new_g[ni][nj] == c:
                        count += 1
                if count < threshold:
                    temp_g[i][j] = bg
                    changed = True
        new_g = temp_g
        if not changed:
            break
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    g_clean = remove_small_objects(g, bg, min_size=3)
    g_clean = prune_protrusions(g_clean, bg, threshold=2, max_iters=2)
    return g_clean
```