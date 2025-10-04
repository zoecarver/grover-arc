```python
from typing import List

LARGE = 1000

def compute_min_dists(positions: List[int]) -> List[int]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    n = len(sorted_pos)
    min_dists = []
    for i in range(n):
        c = sorted_pos[i]
        d1 = LARGE if i == 0 else c - sorted_pos[i - 1]
        d2 = LARGE if i == n - 1 else sorted_pos[i + 1] - c
        min_dists.append(min(d1, d2))
    return min_dists

def get_normal_rep(positions: List[int]) -> List[int]:
    if not positions or all(c > 7 for c in positions):
        return []
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    candidates = [sorted_pos[i] for i in range(len(sorted_pos)) if min_d_list[i] == max_d]
    if candidates:
        return [min(candidates)]
    return []

def get_penultimate_reps(g: List[List[int]], r: int) -> List[int]:
    row = g[r]
    positions = [c for c in range(16) if row[c] != 7]
    if not positions or all(c > 7 for c in positions):
        return []
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    if max_d != 1:
        # gap rule
        reps = []
        current = None
        for c in sorted_pos:
            if current is None or (c - current) >= 6:
                reps.append(c)
                current = c
        return reps
    else:
        # pair mode
        components = []
        i = 0
        n_len = len(sorted_pos)
        while i < n_len:
            start = i
            j = i + 1
            while j < n_len and sorted_pos[j] == sorted_pos[j - 1] + 1:
                j += 1
            comp_size = j - start
            if comp_size == 2:
                left = sorted_pos[start]
                components.append(left)
            i = j
        if not components:
            return []
        shift = components[0]
        shifted = [c - shift for c in components]
        u = 9
        for c_shift in shifted:
            if 0 <= c_shift < 16:
                g[u][c_shift] = 9
                g[1][c_shift] = 9
        # fill second if possible
        if len(components) >= 2:
            second = components[1]
            g[6][second] = 9
            if second + 1 < 16:
                g[6][second + 1] = 9
            g[7][second] = 9
        return []

def handle_center_blue(g: List[List[int]], original_g: List[List[int]]) -> List[List[int]]:
    if g[9][7] == 9 and original_g[14][7] == 9:
        g[9][7] = 1
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    n = 16
    for r in range(10, 15):
        u = r - 5
        if r == 14:
            reps = get_penultimate_reps(out, r)
        else:
            positions = [c for c in range(n) if g[r][c] != 7]
            reps = get_normal_rep(positions)
        for rep in reps:
            out[u][rep] = 9
    out = handle_center_blue(out, g)
    return out
```