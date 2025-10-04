```python
import copy
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

def get_holes(base_comp: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    holes = set()
    for i, j in base_comp:
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < 30 and 0 <= nj < 30 and (ni, nj) not in holes:
                holes.add((ni, nj))
    hole_list = [(i, j) for i, j in holes if 0 <= i < 30 and 0 <= j < 30]
    hole_list.sort(key=lambda x: (x[0], x[1]))
    return hole_list

def get_anchor(comp: List[Tuple[int, int]]) -> Tuple[int, int]:
    min_r = min(r for r, c in comp)
    min_cs = [c for r, c in comp if r == min_r]
    min_c = min(min_cs)
    return min_r, min_c

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy.deepcopy(g)
    components = get_connected_components(out)
    if not components:
        return out
    base_idx = max(range(len(components)), key=lambda k: len(components[k][1]))
    base_color, base_comp = components[base_idx]
    base_min_r = min(r for r, c in base_comp)
    base_max_r = max(r for r, c in base_comp)
    holes = get_holes(base_comp)
    small_components = [comp for idx, comp in enumerate(components) if idx != base_idx]
    small_components.sort(key=lambda x: (min(r for r, c in x[1]), min(c for r, c in x[1])))
    below_components = []
    for color, comp in small_components:
        anchor_r, anchor_c = get_anchor(comp)
        placed = False
        for hole_r, hole_c in holes:
            good = True
            new_pos = []
            for r, c in comp:
                delta_r = r - anchor_r
                delta_c = c - anchor_c
                nr = hole_r + delta_r
                nc = hole_c + delta_c
                if not (0 <= nr < 30 and 0 <= nc < 30):
                    good = False
                    break
                new_pos.append((nr, nc))
                if base_min_r <= nr <= base_max_r:
                    if out[nr][nc] != 0:
                        good = False
                        break
                else:
                    if out[nr][nc] != 0:
                        good = False
                        break
            if good:
                for r, c in comp:
                    out[r][c] = 0
                for nr, nc in new_pos:
                    out[nr][nc] = color
                placed = True
                break
        if not placed:
            below_components.append((color, comp))
    # stacking below
    if below_components:
        # block cols from base
        base_min_c = min(c for r, c in base_comp)
        base_max_c = max(c for r, c in base_comp)
        block_min = base_min_c
        block_max = min(base_max_c, base_min_c + 6)  # arbitrary width
        # skyline
        skyline = [base_max_r] * 30
        for j in range(block_min, block_max + 1):
            for i in range(base_max_r + 1, 30):
                if out[i][j] > 0:
                    skyline[j] = max(skyline[j], i)
        # sort below by color
        below_components.sort(key=lambda x: x[0])
        for color, comp in below_components:
            min_r_comp = min(r for r, c in comp)
            min_c_comp = min(c for r, c in comp)
            rel_cells = [(r - min_r_comp, c - min_c_comp) for r, c in comp]
            max_rel_r = {}
            for rel_r, rel_c in rel_cells:
                if rel_c not in max_rel_r:
                    max_rel_r[rel_c] = rel_r
                else:
                    max_rel_r[rel_c] = max(max_rel_r[rel_c], rel_r)
            base_r = base_max_r + 1
            for rel_c in max_rel_r:
                col = block_min + rel_c
                if 0 <= col < 30:
                    temp = skyline[col] + 1 - max_rel_r[rel_c]
                    base_r = max(base_r, temp)
            shift_r = base_r - min_r_comp
            shift_c = block_min - min_c_comp
            for r, c in comp:
                out[r][c] = 0
            for rel_r, rel_c in rel_cells:
                nr = min_r_comp + shift_r + rel_r
                nc = min_c_comp + shift_c + rel_c
                if 0 <= nr < 30 and 0 <= nc < 30:
                    out[nr][nc] = color
            # update skyline
            for rel_r, rel_c in rel_cells:
                nr = min_r_comp + shift_r + rel_r
                nc = min_c_comp + shift_c + rel_c
                if 0 <= nr < 30 and 0 <= nc < 30:
                    skyline[nc] = max(skyline[nc], nr)
    return out
```