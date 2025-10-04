```python
from collections import Counter
from typing import List, Tuple, Dict

def get_background(g: List[List[int]]) -> int:
    n = len(g)
    flat = [g[i][j] for i in range(n) for j in range(n)]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[Dict]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] != bg and not visited[i][j]:
                cells: List[Tuple[int, int]] = []
                has_e = False
                stack = [(i, j)]
                visited[i][j] = True
                min_r, max_r = i, i
                min_c, max_c = j, j
                while stack:
                    x, y = stack.pop()
                    cells.append((x, y))
                    if g[x][y] == 8:
                        has_e = True
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append({
                    'cells': cells,
                    'minr': min_r,
                    'maxr': max_r,
                    'minc': min_c,
                    'maxc': max_c,
                    'has8': has_e
                })
    return components

def place_left_components(g: List[List[int]], out: List[List[int]], bg: int, left_comps: List[Dict]) -> None:
    n = len(g)
    if not left_comps:
        return
    left_comps.sort(key=lambda d: (d['minr'], d['minc']))
    current_width = 0
    last_maxr = -1
    for comp in left_comps:
        minr = comp['minr']
        maxr = comp['maxr']
        minc = comp['minc']
        w = comp['maxc'] - minc + 1
        if minr > last_maxr + 1:
            place_col = 0
        else:
            place_col = current_width
        shift = place_col - minc
        for r, c in comp['cells']:
            new_c = c + shift
            if 0 <= new_c < n:
                out[r][new_c] = g[r][c]
        current_width = place_col + w
        last_maxr = max(last_maxr, maxr)

def place_right_components(g: List[List[int]], out: List[List[int]], bg: int, right_comps: List[Dict]) -> None:
    n = len(g)
    for comp in right_comps:
        minc = comp['minc']
        if minc <= 8:
            place_col = 12
        else:
            place_col = 17
        shift = place_col - minc
        for r, c in comp['cells']:
            new_c = c + shift
            if 0 <= new_c < n:
                out[r][new_c] = g[r][c]

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_background(g)
    all_comps = find_components(g, bg)
    left_comps = [c for c in all_comps if c['has8']]
    right_comps = [c for c in all_comps if not c['has8']]
    out = [[bg for _ in range(n)] for _ in range(n)]
    place_left_components(g, out, bg, left_comps)
    place_right_components(g, out, bg, right_comps)
    return out
```