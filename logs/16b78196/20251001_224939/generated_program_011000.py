```python
from typing import List, Tuple
import copy

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
    if not comp:
        return 0, 0
    min_r = min(r for r, c in comp)
    min_cs = [c for r, c in comp if r == min_r]
    min_c = min(min_cs)
    return min_r, min_c

def get_bbox(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0
    min_r = min(r for r, c in comp)
    max_r = max(r for r, c in comp)
    min_c = min(c for r, c in comp)
    max_c = max(c for r, c in comp)
    return min_r, max_r, min_c, max_c

def get_center(comp: List[Tuple[int, int]]) -> Tuple[float, float]:
    if not comp:
        return 0.0, 0.0
    n = len(comp)
    sum_r = sum(r for r, c in comp)
    sum_c = sum(c for r, c in comp)
    return sum_r / n, sum_c / n

def select_base(components: List[Tuple[int, List[Tuple[int, int]]]]) -> Tuple[int, List[Tuple[int, int]]]:
    if not components:
        return (0, [])
    base = max(components, key=lambda x: (len(x[1]), x[0]))
    return base

def get_smalls(components: List[Tuple[int, List[Tuple[int, int]]]], base: Tuple[int, List[Tuple[int, int]]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    return [c for c in components if c != base]

def sort_smalls(smalls: List[Tuple[int, List[Tuple[int, int]]]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    def sort_key(comp: Tuple[int, List[Tuple[int, int]]]):
        color, pos = comp
        size = len(pos)
        min_r = min((r for r, _ in pos), default=0)
        return (-size, color, min_r)
    smalls.sort(key=sort_key)
    return smalls

def place_base(out: List[List[int]], base: Tuple[int, List[Tuple[int, int]]]):
    color, pos_list = base
    for r, c in pos_list:
        out[r][c] = color

def find_best_placement(out: List[List[int]], comp: Tuple[int, List[Tuple[int, int]]], b_bbox: Tuple[int, int, int, int], b_center: Tuple[float, float]) -> List[Tuple[int, int]]:
    color, pos_list = comp
    anchor_r, anchor_c = get_anchor(pos_list)
    best_score = (-float('inf'), -float('inf'), float('inf'))
    best_proposed: List[Tuple[int, int]] = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    b_min_r, b_max_r, b_min_c, b_max_c = b_bbox
    b_avg_r, b_avg_c = b_center
    for tr in range(30):
        for tc in range(30):
            dr = tr - anchor_r
            dc = tc - anchor_c
            proposed = []
            valid = True
            sum_nr = 0.0
            sum_nc = 0.0
            for r, c in pos_list:
                nr = r + dr
                nc = c + dc
                if nr < 0 or nr > 29 or nc < 0 or nc > 29 or out[nr][nc] != 0:
                    valid = False
                    break
                proposed.append((nr, nc))
                sum_nr += nr
                sum_nc += nc
            if not valid or not proposed:
                continue
            n_prop = len(proposed)
            avg_nr = sum_nr / n_prop
            avg_nc = sum_nc / n_prop
            dist = (avg_nr - b_avg_r) ** 2 + (avg_nc - b_avg_c) ** 2
            fill = sum(1 for nr, nc in proposed if b_min_r <= nr <= b_max_r and b_min_c <= nc <= b_max_c)
            adj = 0
            for nr, nc in proposed:
                for dx, dy in directions:
                    nnr = nr + dx
                    nnc = nc + dy
                    if 0 <= nnr < 30 and 0 <= nnc < 30 and out[nnr][nnc] > 0:
                        adj += 1
            score = (fill, adj, -dist)
            if score > best_score:
                best_score = score
                best_proposed = proposed
    return best_proposed

def place_comp(out: List[List[int]], comp: Tuple[int, List[Tuple[int, int]]], proposed: List[Tuple[int, int]]):
    color, _ = comp
    for nr, nc in proposed:
        out[nr][nc] = color

def program(g: List[List[int]]) -> List[List[int]]:
    components = get_connected_components(g)
    if not components:
        return [[0] * 30 for _ in range(30)]
    base = select_base(components)
    smalls = get_smalls(components, base)
    smalls = sort_smalls(smalls)
    out = [[0] * 30 for _ in range(30)]
    place_base(out, base)
    b_bbox = get_bbox(base[1])
    b_center = get_center(base[1])
    for comp in smalls:
        proposed = find_best_placement(out, comp, b_bbox, b_center)
        if proposed:
            place_comp(out, comp, proposed)
    return out
```