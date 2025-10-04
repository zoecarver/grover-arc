```python
from typing import List, Tuple
from collections import deque

def find_components(g: List[List[int]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    n = 30
    visited = [[False] * n for _ in range(n)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != 0 and not visited[i][j]:
                color = g[i][j]
                component = []
                q = deque([(i, j)])
                visited[i][j] = True
                while q:
                    x, y = q.popleft()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                components.append((color, component))
    return components

def place_base(h: List[List[int]], base_color: int, base_comp: List[Tuple[int, int]]):
    n = 30
    for i in range(n):
        for j in range(n):
            h[i][j] = 0
    for r, c in base_comp:
        h[r][c] = base_color

def get_relative(comp: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not comp:
        return []
    min_r = min(r for r, c in comp)
    min_c = min(c for r, c in comp)
    return [(r - min_r, c - min_c) for r, c in comp]

def place_shape(h: List[List[int]], color: int, rel: List[Tuple[int, int]], start_r: int, start_c: int):
    n = 30
    for dr, dc in rel:
        r = start_r + dr
        c = start_c + dc
        if 0 <= r < n and 0 <= c < n:
            h[r][c] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = 30
    h = [[0] * n for _ in range(n)]
    components = find_components(g)
    if not components:
        return h
    # Find base: largest component
    base = max(components, key=lambda x: len(x[1]))
    base_color, base_comp = base
    place_base(h, base_color, base_comp)
    # Other components, sort by color
    others = [c for c in components if c[1] != base_comp]
    others.sort(key=lambda x: x[0])
    # Stack them above the base on the left
    base_min_r = min(r for r, c in base_comp) if base_comp else n
    current_r = max(0, base_min_r - sum(len(c[1]) for c in others) // 5)  # rough estimate
    for color, comp in others:
        rel = get_relative(comp)
        if rel:
            max_dr = max(dr for dr, dc in rel)
            height = max_dr + 1
            place_shape(h, color, rel, current_r, 0)
            current_r += height
    return h
```