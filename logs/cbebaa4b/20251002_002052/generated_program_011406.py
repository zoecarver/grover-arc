```python
from typing import List, Tuple, Dict
import math

def flood(start_i: int, start_j: int, c: int, g: List[List[int]], visited: List[List[bool]], n: int) -> List[Tuple[int, int, int]]:
    stack = [(start_i, start_j)]
    visited[start_i][start_j] = True
    component = []
    while stack:
        i, j = stack.pop()
        if g[i][j] != c:
            continue
        component.append((i, j, c))
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and not visited[ni][nj] and g[ni][nj] == c:
                visited[ni][nj] = True
                stack.append((ni, nj))
    return component

def process_component(main_comp: List[Tuple[int, int, int]], g: List[List[int]], n: int) -> Dict:
    if not main_comp:
        return {}
    min_r_main = min(r for r, _, _ in main_comp)
    max_r_main = max(r for r, _, _ in main_comp)
    min_c_main = min(c for _, c, _ in main_comp)
    # Upper 2's count
    upper_set = set()
    for r, c, _ in main_comp:
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + di, c + dj
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 2 and nr < min_r_main:
                upper_set.add((nr, nc))
    upper_count = len(upper_set)
    # Attached lower 2's
    start_2s = set()
    for r, c, _ in main_comp:
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + di, c + dj
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 2 and nr >= min_r_main:
                start_2s.add((nr, nc))
    visited_2 = [[False] * n for _ in range(n)]
    attached = []
    stack = list(start_2s)
    for i, j in start_2s:
        visited_2[i][j] = True
    while stack:
        i, j = stack.pop()
        if g[i][j] != 2 or visited_2[i][j]:
            continue
        visited_2[i][j] = True
        attached.append((i, j, 2))
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == 2 and not visited_2[ni][nj]:
                visited_2[ni][nj] = True
                stack.append((ni, nj))
    # Max r for bottom touch
    max_r = max_r_main
    if attached:
        max_r = max(max_r, max(r for r, _, _ in attached))
    is_bottom_touch = max_r >= n - 2
    centroid = sum(r for r, _, _ in main_comp) / len(main_comp)
    is_top_touch = upper_count > 0
    # Extra for top touch
    extra_abs = []
    if is_top_touch:
        bottom_rel = max_r_main - min_r_main
        bottom_abs_cols = set(c for r, c, _ in main_comp if r - min_r_main == bottom_rel)
        num = min(upper_count, len(bottom_abs_cols))
        sorted_cols = sorted(bottom_abs_cols)
        extra_r = min_r_main + bottom_rel + 1
        for ii in range(num):
            extra_c = sorted_cols[ii]
            extra_abs.append((extra_r, extra_c, 2))
    # All abs cells
    all_cells_abs = [(r, c, v) for r, c, v in main_comp] + [(r, c, 2) for r, c, _ in attached] + extra_abs
    if all_cells_abs:
        min_r_all = min(r for r, _, _ in all_cells_abs)
        min_c_all = min(c for _, c, _ in all_cells_abs)
    else:
        min_r_all = min_r_main
        min_c_all = min_c_main
    rel_comp = [(r - min_r_all, c - min_c_all, v) for r, c, v in all_cells_abs]
    return {
        'rel_comp': rel_comp,
        'min_r_main': min_r_main,
        'centroid': centroid,
        'is_top_touch': is_top_touch,
        'is_bottom_touch': is_bottom_touch
    }

def place(rel_comp: List[Tuple[int, int, int]], dy: int, left: int, out: List[List[int]], n: int):
    for rel_r, rel_c, val in rel_comp:
        nr = dy + rel_r
        nc = left + rel_c
        if 0 <= nr < n and 0 <= nc < n:
            out[nr][nc] = val

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] > 0 and g[i][j] != 2 and not visited[i][j]:
                main_comp = flood(i, j, g[i][j], g, visited, n)
                data = process_component(main_comp, g, n)
                if data['rel_comp']:  # only if has cells
                    components.append(data)
    bottom_touch = [d for d in components if d['is_bottom_touch']]
    top_touch = [d for d in components if d['is_top_touch']]
    remaining_base = [d for d in components if d not in bottom_touch and d not in top_touch]
    remaining_base.sort(key=lambda d: d['centroid'])
    if top_touch:
        order = bottom_touch[:1] + top_touch[:1] + remaining_base  # take first if multiple
    else:
        top_most = None
        if remaining_base:
            top_most_cand = min(remaining_base, key=lambda d: d['min_r_main'])
            top_most = top_most_cand
            remaining_base = [d for d in remaining_base if d != top_most]
        order = ([top_most] if top_most else []) + bottom_touch[:1] + remaining_base
    out = [[0] * n for _ in range(n)]
    baseline = 4
    max_shift = 10
    current_max_r = -1
    for idx, data in enumerate(order):
        rel_comp = data['rel_comp']
        if not rel_comp:
            continue
        h = max(r for r, _, _ in rel_comp) + 1
        w = max(c for _, c, _ in rel_comp) + 1
        center_left = (n - w) // 2
        use_small_shift = data['is_top_touch']
        shift = 2 if use_small_shift else max_shift
        if idx == 0:
            dy = baseline
            dx = 0
            left = center_left + dx
            place(rel_comp, dy, left, out, n)
            current_max_r = max(current_max_r, dy + h - 1)
            continue
        # tight placement
        best_dy = math.inf
        best_dx = 0
        best_abs = math.inf
        for cand_dy in range(0, n - h + 1):
            fitting_ddx = []
            for ddx in range(-shift, shift + 1):
                fits = True
                for rel_r, rel_c, val in rel_comp:
                    nr = cand_dy + rel_r
                    nc = center_left + rel_c + ddx
                    if nr >= n or nc < 0 or nc >= n or out[nr][nc] != 0:
                        fits = False
                        break
                if fits:
                    fitting_ddx.append(ddx)
            if fitting_ddx:
                # choose largest ddx among fitting
                selected_dx = max(fitting_ddx)
                abs_d = abs(selected_dx)
                if cand_dy < best_dy or (cand_dy == best_dy and abs_d < best_abs):
                    best_dy = cand_dy
                    best_dx = selected_dx
                    best_abs = abs_d
        if math.isinf(best_dy):
            # fallback
            dy = max(current_max_r + 1, baseline)
            dx = 0
            left = center_left + dx
        else:
            dy = best_dy
            dx = best_dx
            left = center_left + dx
        place(rel_comp, dy, left, out, n)
        current_max_r = max(current_max_r, dy + h - 1)
    return out
```