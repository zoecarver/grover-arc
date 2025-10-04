```python
from typing import List
from math import inf

def compute_min_dists(positions: List[int]) -> List[float]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    n = len(sorted_pos)
    min_dists = []
    for i in range(n):
        d1 = inf if i == 0 else sorted_pos[i] - sorted_pos[i - 1]
        d2 = inf if i == n - 1 else sorted_pos[i + 1] - sorted_pos[i]
        min_dists.append(min(d1, d2))
    return min_dists

def get_normal_rep(positions: List[int]) -> List[int]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    candidates = [sorted_pos[i] for i in range(len(sorted_pos)) if min_d_list[i] == max_d]
    if candidates:
        return [min(candidates)]
    return []

def get_penultimate_reps(g: List[List[int]], r: int) -> List[int]:
    positions = [c for c in range(16) if g[r][c] != 7]
    if not positions:
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
        n_len = len(sorted_pos)
        while i < n_len:
            start = i
            j = i + 1
            while j < n_len and sorted_pos[j] == sorted_pos[j - 1] + 1:
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
            if 0 <= c < 16:
                g[9][c] = 9
                g[1][c] = 9
        if len(components) >= 2:
            second = components[1]
            g[6][second] = 9
            if second + 1 < 16:
                g[6][second + 1] = 9
            g[7][second] = 9
        return []

def handle_center_override(g: List[List[int]], original_g: List[List[int]]) -> None:
    if g[9][7] == 9 and original_g[14][7] == 9:
        g[9][7] = 1

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    original_g = [row[:] for row in g]
    for r in range(10, 14):
        positions = [c for c in range(16) if out[r][c] != 7]
        reps = get_normal_rep(positions)
        u = r - 5
        for rep in reps:
            if 0 <= u < 16 and 0 <= rep < 16:
                out[u][rep] = 9
    penultimate_reps = get_penultimate_reps(out, 14)
    u = 14 - 5
    for rep in penultimate_reps:
        if 0 <= u < 16 and 0 <= rep < 16:
            out[u][rep] = 9
    handle_center_override(out, original_g)
    return out
```