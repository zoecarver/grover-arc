```python
from typing import List, Tuple
from collections import defaultdict, deque
import copy

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
    dirs = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == 0 and dj == 0)]  # 8-connectivity
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

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    output = [[bg for _ in range(len(row))] for row in g]
    objects = extract_objects(g, bg)
    components = defaultdict(list)
    for obj in objects:
        if obj:
            c = obj[0][2]
            components[c].append(obj)
    templates = {
        1: (6, 9, [(0,1),(0,2),(0,3),(0,5),(0,6),(0,7),(1,0),(1,1),(1,7),(1,8),(2,1),(2,7),(3,1),(3,3),(3,4),(3,5),(3,7),(4,0),(4,1),(4,2),(4,3),(4,5),(4,6),(4,7),(5,2),(5,6)]),
        2: (5, 6, [(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,4),(1,5),(2,0),(2,1),(2,4),(2,5),(3,1),(3,2),(3,3),(3,4),(4,2),(4,3)]),
        3: (5, 6, [(0,1),(0,2),(0,3),(0,4),(1,4),(2,1),(2,2),(2,3),(2,4),(3,4),(4,1),(4,2),(4,3),(4,4)]),
        4: (6, 7, [(0,2),(0,3),(0,4),(1,1),(1,2),(1,3),(1,4),(1,5),(2,0),(2,1),(2,5),(2,6),(3,1),(3,2),(3,3),(3,4),(3,5),(4,1),(4,2),(4,3),(4,4),(4,5),(5,3)]),
        6: (3, 3, [(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(2,2)]),
        8: (4, 3, [(0,1),(1,0),(1,2),(2,0),(2,2),(3,1)])
    }
    for c in components:
        if c == bg or c not in templates: continue
        max_obj = max(components[c], key=len)
        if len(max_obj) < 3: continue
        rows = [p[0] for p in max_obj]
        cols = [p[1] for p in max_obj]
        min_r = min(rows)
        max_r = max(rows)
        min_c = min(cols)
        max_c = max(cols)
        ch = max_r - min_r + 1
        cw = max_c - min_c + 1
        base_h, base_w, base_pos = templates[c]
        base_grid = [[0] * base_w for _ in range(base_h)]
        for br, bc in base_pos:
            base_grid[br][bc] = 1
        scaled = [[0] * cw for _ in range(ch)]
        for i in range(ch):
            base_i = min(int(i * base_h / ch), base_h - 1)
            for j in range(cw):
                base_j = min(int(j * base_w / cw), base_w - 1)
                if base_grid[base_i][base_j] == 1:
                    scaled[i][j] = 1
        for i in range(ch):
            for j in range(cw):
                if scaled[i][j] == 1:
                    r = min_r + i
                    cc = min_c + j
                    if 0 <= r < len(g) and 0 <= cc < len(g[0]):
                        output[r][cc] = c
    return output
```