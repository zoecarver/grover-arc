```python
from typing import List
from collections import deque, Counter
import copy

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def extract_components(g: List[List[int]], bg: int) -> List[List[tuple[int, int, int]]]:
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != bg and not visited[i][j]:
                c = g[i][j]
                comp = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    comp.append((x, y, c))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == c:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components.append(comp)
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    h, w = len(g), len(g[0])
    bg = find_background(g)
    out = copy.deepcopy(g)
    components = extract_components(out, bg)
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dirs8 = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if di != 0 or dj != 0]
    for comp in components:
        size = len(comp)
        if size < 3:
            c = comp[0][2]
            for i, j, _ in comp:
                out[i][j] = bg
            continue
        iset = {p[0] for p in comp}
        jset = {p[1] for p in comp}
        min_i, max_i = min(iset), max(iset)
        min_j, max_j = min(jset), max(jset)
        c = comp[0][2]
        # Fill gaps within bbox
        temp = copy.deepcopy(out)
        for i in range(min_i, max_i + 1):
            for j in range(min_j, max_j + 1):
                if out[i][j] == bg:
                    count = sum(1 for di, dj in dirs4 if 0 <= i + di < h and 0 <= j + dj < w and out[i + di][j + dj] == c)
                    if count >= 3:
                        temp[i][j] = c
        out = temp
        # Prune low-connectivity within bbox
        for _ in range(2):
            changed = False
            temp = copy.deepcopy(out)
            for i in range(min_i, max_i + 1):
                for j in range(min_j, max_j + 1):
                    if out[i][j] != c:
                        continue
                    count = sum(1 for di, dj in dirs8 if 0 <= i + di < h and 0 <= j + dj < w and out[i + di][j + dj] == c)
                    if count < 2:
                        temp[i][j] = bg
                        changed = True
            out = temp
            if not changed:
                break
    return out
```