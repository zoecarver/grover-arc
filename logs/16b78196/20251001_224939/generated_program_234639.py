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

def get_anchor(comp: List[Tuple[int, int]]) -> Tuple[int, int]:
    min_r = min(r for r, c in comp)
    min_cs = [c for r, c in comp if r == min_r]
    min_c = min(min_cs)
    return min_r, min_c

def program(g: List[List[int]]) -> List[List[int]]:
    components = get_connected_components(g)
    if not components:
        return [row[:] for row in g]
    base = max(components, key=lambda x: len(x[1]))
    out = [[0] * 30 for _ in range(30)]
    base_color, base_pos = base
    for r, c in base_pos:
        out[r][c] = base_color
    small = [comp for comp in components if comp != base]
    small.sort(key=lambda x: (-len(x[1]), x[0]))
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for color, comp in small:
        ar, ac = get_anchor(comp)
        best_score = -1
        best_placed = None
        best_min_r = 31
        best_min_c = 31
        best_max_r = -1
        for tr in range(30):
            for tc in range(30):
                dr = tr - ar
                dc = tc - ac
                valid = True
                placed_pos = []
                min_nr = 30
                min_nc = 30
                max_nr = 0
                for r, c in comp:
                    nr = r + dr
                    nc = c + dc
                    if not (0 <= nr < 30 and 0 <= nc < 30) or out[nr][nc] != 0:
                        valid = False
                        break
                    placed_pos.append((nr, nc))
                    min_nr = min(min_nr, nr)
                    min_nc = min(min_nc, nc)
                    max_nr = max(max_nr, nr)
                if valid:
                    score = 0
                    for nr, nc in placed_pos:
                        for dx, dy in directions:
                            nnr = nr + dx
                            nnc = nc + dy
                            if 0 <= nnr < 30 and 0 <= nnc < 30 and out[nnr][nnc] > 0:
                                score += 1
                    update = False
                    if score > best_score:
                        update = True
                    elif score == best_score:
                        if min_nr < best_min_r:
                            update = True
                        elif min_nr == best_min_r:
                            if min_nc < best_min_c:
                                update = True
                            elif min_nc == best_min_c:
                                if max_nr < best_max_r:
                                    update = True
                    if update:
                        best_score = score
                        best_placed = placed_pos
                        best_min_r = min_nr
                        best_min_c = min_nc
                        best_max_r = max_nr
        if best_placed:
            for nr, nc in best_placed:
                out[nr][nc] = color
    return out
```