```python
from typing import List, Tuple

def get_connected_components(g: List[List[int]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = [[False] * 30 for _ in range(30)]
    components = []
    for i in range(30):
        for j in range(30):
            if g[i][j] > 0 and not visited[i][j]:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 30 and 0 <= ny < 30 and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    components = get_connected_components(g)
    if not components:
        return [[0 for _ in range(30)] for _ in range(30)]
    # Find base: max size, tie by max color
    base = max(components, key=lambda x: (len(x[1]), x[0]))
    out = [[0 for _ in range(30)] for _ in range(30)]
    base_color, base_pos = base
    for r, c in base_pos:
        out[r][c] = base_color
    smalls = [c for c in components if c != base]
    # Sort smalls by increasing color, then increasing min_r
    smalls.sort(key=lambda x: (x[0], min(rr for rr, cc in x[1])))
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    base_min_r = min(r for r, c in base_pos) if base_pos else 15
    base_max_r = max(r for r, c in base_pos) if base_pos else 15
    base_min_c = min(c for r, c in base_pos) if base_pos else 15
    base_max_c = max(c for r, c in base_pos) if base_pos else 15
    for color, pos in smalls:
        best_score = (-1, -1, 100, 100)
        best_dr = best_dc = None
        for dr in range(-30, 31):
            for dc in range(-30, 31):
                proposed = [(r + dr, c + dc) for r, c in pos]
                if any(not (0 <= nr < 30 and 0 <= nc < 30) for nr, nc in proposed):
                    continue
                if any(out[nr][nc] != 0 for nr, nc in proposed):
                    continue
                fill = sum(base_min_r <= nr <= base_max_r and base_min_c <= nc <= base_max_c for nr, nc in proposed)
                adj = 0
                for nr, nc in proposed:
                    for dx, dy in directions:
                        nnr = nr + dx
                        nnc = nc + dy
                        if 0 <= nnr < 30 and 0 <= nnc < 30 and out[nnr][nnc] > 0:
                            adj += 1
                min_r_prop = min(nr for nr, nc in proposed)
                min_c_prop = min(nc for nr, nc in proposed)
                score = (fill, adj, -min_r_prop, -min_c_prop)
                if score > best_score:
                    best_score = score
                    best_dr = dr
                    best_dc = dc
        if best_dr is not None:
            for r, c in pos:
                nr = r + best_dr
                nc = c + best_dc
                out[nr][nc] = color
    return out
```