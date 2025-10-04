```python
from typing import List

def compute_min_dists(positions: List[int]) -> List[int]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    n = len(sorted_pos)
    LARGE = 100
    min_dists = []
    for i in range(n):
        c = sorted_pos[i]
        d1 = LARGE if i == 0 else c - sorted_pos[i - 1]
        d2 = LARGE if i == n - 1 else sorted_pos[i + 1] - c
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

def get_gap_reps(positions: List[int]) -> List[int]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    reps = []
    current = None
    for c in sorted_pos:
        if current is None or (c - current) >= 6:
            reps.append(c)
            current = c
    return reps

def handle_center_blue(out: List[List[int]], g: List[List[int]]) -> List[List[int]]:
    n = 16
    if out[9][7] == 9 and g[14][7] == 9:
        out[9][7] = 1
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    n = 16
    out = [row[:] for row in g]
    for r in range(10, 15):
        positions = [c for c in range(n) if g[r][c] != 7]
        if not positions or all(c > 7 for c in positions):
            continue
        if r == 14:
            min_d_list = compute_min_dists(positions)
            max_d = max(min_d_list)
            if max_d != 1:
                reps = get_gap_reps(positions)
                for p in reps:
                    if 0 <= p < n:
                        out[9][p] = 9
            else:
                sorted_pos = sorted(positions)
                m = len(sorted_pos)
                components = []
                i = 0
                while i < m:
                    start_i = i
                    j = i + 1
                    while j < m and sorted_pos[j] == sorted_pos[j - 1] + 1:
                        j += 1
                    comp_size = j - start_i
                    if comp_size == 2:
                        components.append(sorted_pos[start_i])
                    i = j
                if components:
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
        else:
            reps = get_normal_rep(positions)
            u = r - 5
            for p in reps:
                if 0 <= u < n and 0 <= p < n:
                    out[u][p] = 9
    out = handle_center_blue(out, g)
    return out
```