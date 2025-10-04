```python
from typing import List

def compute_min_dists(positions: List[int]) -> List[int]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    m = len(sorted_pos)
    LARGE = 1000
    min_dists = []
    for i in range(m):
        d1 = LARGE if i == 0 else sorted_pos[i] - sorted_pos[i - 1]
        d2 = LARGE if i == m - 1 else sorted_pos[i + 1] - sorted_pos[i]
        min_dists.append(min(d1, d2))
    return min_dists

def get_normal_rep(positions: List[int]) -> List[int]:
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    candidates = [sorted_pos[i] for i in range(len(sorted_pos)) if min_d_list[i] == max_d]
    return [min(candidates)] if candidates else []

def get_penultimate_reps(out: List[List[int]], g: List[List[int]], r: int) -> List[int]:
    n = 16
    row = g[r]
    positions = [c for c in range(n) if row[c] != 7]
    if not positions or all(c > 7 for c in positions):
        return []
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    if max_d != 1:
        reps = []
        current = None
        for c in sorted_pos:
            if current is None or (c - current) >= 6:
                reps.append(c)
                current = c
        return reps
    else:
        components = []
        i = 0
        while i < len(sorted_pos):
            start = i
            j = i + 1
            while j < len(sorted_pos) and sorted_pos[j] == sorted_pos[j - 1] + 1:
                j += 1
            comp_size = j - start
            if comp_size == 2:
                components.append(sorted_pos[start])
            i = j
        if not components:
            return []
        shift = components[0]
        shifted = [c - shift for c in components]
        for c in shifted:
            if 0 <= c < n:
                out[9][c] = 9
                out[1][c] = 9
        if len(components) >= 2:
            second = components[1]
            out[6][second] = 9
            if second + 1 < n:
                out[6][second + 1] = 9
            out[7][second] = 9
        return []

def handle_center_blue(out: List[List[int]], g: List[List[int]]) -> None:
    if out[9][7] == 9 and g[14][7] == 9:
        out[9][7] = 1

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    n = 16
    for r in range(10, 14):
        positions = [c for c in range(n) if g[r][c] != 7]
        if positions and not all(c > 7 for c in positions):
            reps = get_normal_rep(positions)
            u = r - 5
            for rep in reps:
                out[u][rep] = 9
    r = 14
    positions = [c for c in range(n) if g[r][c] != 7]
    if positions and not all(c > 7 for c in positions):
        reps = get_penultimate_reps(out, g, r)
        if reps:
            u = 9
            for rep in reps:
                out[u][rep] = 9
    handle_center_blue(out, g)
    return out
```