```python
from typing import List, Tuple
from collections import deque

def find_special_color(g: List[List[int]]) -> int:
    s = None
    for row in g:
        for val in row:
            if val != 7:
                if s is None:
                    s = val
                break
        if s is not None:
            break
    return s

def get_component(g: List[List[int]], s: int, start: Tuple[int, int], visited: set) -> List[Tuple[int, int]]:
    component = []
    queue = deque([start])
    visited.add(start)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while queue:
        r, c = queue.popleft()
        component.append((r, c))
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 16 and 0 <= nc < 16 and (nr, nc) not in visited and g[nr][nc] == s:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return component

def get_all_components(g: List[List[int]], s: int) -> List[List[Tuple[int, int]]]:
    if s is None:
        return []
    positions = [(i, j) for i in range(16) for j in range(16) if g[i][j] == s]
    visited = set()
    components = []
    for p in positions:
        if p not in visited:
            comp = get_component(g, s, p, visited)
            components.append(comp)
    return components

def compute_projection(comp: List[Tuple[int, int]]) -> Tuple[int, int]:
    min_r = min(r for r, _ in comp)
    row_out = min_r - 5
    if row_out < 0:
        return None
    top = [c for r, c in comp if r == min_r]
    top_cols = sorted(list(set(top)))
    if len(top_cols) == 1:
        col_out = top_cols[0]
    elif max(top_cols) - min(top_cols) + 1 == len(top_cols):
        col_out = min(top_cols) - 5
    else:
        col_out = round(sum(top_cols) / len(top_cols))
    if col_out < 0 or col_out >= 16:
        return None
    return row_out, col_out

def apply_highlights(out_g: List[List[int]], g: List[List[int]], components: List[List[Tuple[int, int]]], pos_to_comp: dict, s: int, proj_comp: List[Tuple[int, int]]):
    proj = compute_projection(proj_comp)
    if proj is None:
        return
    target_r, target_c = proj
    if g[target_r][target_c] == 7:
        color = 1 if s == 9 and target_c == 7 else 9
        out_g[target_r][target_c] = color
    elif g[target_r][target_c] == s and (target_r, target_c) in pos_to_comp:
        idx = pos_to_comp[(target_r, target_c)]
        for pr, pc in components[idx]:
            out_g[pr][pc] = 9

def program(g: List[List[int]]) -> List[List[int]]:
    s = find_special_color(g)
    components = get_all_components(g, s)
    pos_to_comp = {}
    for idx, comp in enumerate(components):
        for p in comp:
            pos_to_comp[p] = idx
    out_g = [row[:] for row in g]
    for comp in components:
        min_r = min(r for r, _ in comp)
        if min_r < 5:
            continue
        apply_highlights(out_g, g, components, pos_to_comp, s, comp)
    return out_g
```