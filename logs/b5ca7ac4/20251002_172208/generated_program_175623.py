```python
from collections import Counter
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [c for row in g for c in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int]]]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != bg and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(comp)
    return components

def classify_shape(comp: List[Tuple[int, int]], g: List[List[int]]) -> str:
    colors = {g[r][c] for r, c in comp}
    return 'left' if 8 in colors else 'right'

def get_bounding(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    rs = [r for r, _ in comp]
    cs = [c for _, c in comp]
    return min(rs), max(rs), min(cs), max(cs)

def sort_shapes(components: List[List[Tuple[int, int]]], g: List[List[int]]) -> Tuple[List[Tuple], List[Tuple]]:
    left = []
    right = []
    for comp in components:
        typ = classify_shape(comp, g)
        minr, maxr, minc, maxc = get_bounding(comp)
        h = maxr - minr + 1
        w = maxc - minc + 1
        entry = (minr, comp, minc, h, w)
        if typ == 'left':
            left.append(entry)
        else:
            right.append(entry)
    left.sort(key=lambda x: x[0])
    right.sort(key=lambda x: x[0])
    return left, right

def place_shapes(out: List[List[int]], shapes: List[Tuple], start_col: int, g: List[List[int]]):
    current_r = 0
    n = len(out)
    for minr, comp, minc, h, w in shapes:
        for dr in range(h):
            r = current_r + dr
            if r >= n:
                break
            for dc in range(w):
                c = start_col + dc
                if c < n:
                    out[r][c] = g[minr + dr][minc + dc]
        current_r += h

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    components = find_components(g, bg)
    left, right = sort_shapes(components, g)
    out = [[bg] * 22 for _ in range(22)]
    place_shapes(out, left, 0, g)
    place_shapes(out, right, 17, g)
    return out
```