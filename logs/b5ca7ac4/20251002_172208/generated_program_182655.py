```python
from collections import Counter, deque
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
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

def get_bounding(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0
    rs = [r for r, _ in comp]
    cs = [c for _, c in comp]
    return min(rs), max(rs), min(cs), max(cs)

def has_eight(g: List[List[int]], comp: List[Tuple[int, int]]) -> bool:
    colors = {g[r][c] for r, c in comp}
    return 8 in colors

def program(g: List[List[int]]) -> List[List[int]]:
    n = 22
    bg = get_background(g)
    components = find_components(g, bg)
    left_comps = [comp for comp in components if has_eight(g, comp)]
    right_comps = [comp for comp in components if not has_eight(g, comp)]
    left_comps.sort(key=lambda comp: get_bounding(comp)[0])
    right_comps.sort(key=lambda comp: get_bounding(comp)[0])
    out = [[bg] * n for _ in range(n)]
    # Place left components with incremental stacking
    current_pos = 0
    current_maxr = -100
    for comp in left_comps:
        minr, maxr, minc, maxc = get_bounding(comp)
        if minr > current_maxr + 1:
            current_pos = 0
        offset = current_pos - minc
        for r, c in comp:
            new_c = c + offset
            if 0 <= new_c < n:
                out[r][new_c] = g[r][c]
        w = maxc - minc + 1
        current_pos += w
        current_maxr = max(current_maxr, maxr)
    # Place right components independently
    for comp in right_comps:
        minr, maxr, minc, maxc = get_bounding(comp)
        w = maxc - minc + 1
        if minc >= 9:
            offset = 21 - maxc
        else:
            offset = 12 - minc
        for r, c in comp:
            new_c = c + offset
            if 0 <= new_c < n:
                out[r][new_c] = g[r][c]
    return out
```