```python
from typing import List, Tuple
import sys

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
        return [[0] * 30 for _ in range(30)]
    max_size = max(len(c[1]) for c in components)
    candidates = [c for c in components if len(c[1]) == max_size]
    base = min(candidates, key=lambda c: c[0])
    smalls = [c for c in components if c != base]
    smalls.sort(key=lambda x: (-min(r for r, c in x[1]), min(c for r, c in x[1])))
    out = [[0] * 30 for _ in range(30)]
    for r, c in base[1]:
        out[r][c] = base[0]
    base_min_r = min(r for r, c in base[1]) if base[1] else 0
    base_max_r = max(r for r, c in base[1]) if base[1] else 0
    base_min_c = min(c for r, c in base[1]) if base[1] else 0
    base_max_c = max(c for r, c in base[1]) if base[1] else 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for small in smalls:
        color, pos = small
        best_dr = best_dc = None
        best_score = (-sys.maxsize, 0, 0, 0)
        for dr in range(-29, 30):
            for dc in range(-29, 30):
                placed_pos = []
                valid = True
                for r, c in pos:
                    nr = r + dr
                    nc = c + dc
                    if not (0 <= nr < 30 and 0 <= nc < 30) or out[nr][nc] != 0:
                        valid = False
                        break
                    placed_pos.append((nr, nc))
                if not valid:
                    continue
                fill_count = sum(1 for nr, nc in placed_pos if base_min_r <= nr <= base_max_r and base_min_c <= nc <= base_max_c)
                adj_count = 0
                has_adj = False
                for nr, nc in placed_pos:
                    for dx, dy in directions:
                        nnr = nr + dx
                        nnc = nc + dy
                        if 0 <= nnr < 30 and 0 <= nnc < 30 and out[nnr][nnc] > 0:
                            adj_count += 1
                            has_adj = True
                if not has_adj:
                    continue
                min_nr = min(nr for nr, nc in placed_pos)
                min_nc = min(nc for nr, nc in placed_pos)
                score = (fill_count, adj_count, -min_nr, -min_nc)
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