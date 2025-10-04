```python
from typing import List
from math import inf
from copy import deepcopy

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_positions(g: List[List[int]], r: int) -> List[int]:
    n = 16
    return [c for c in range(n) if g[r][c] != 7]

def compute_min_dists(positions: List[int]) -> List[float]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    m = len(sorted_pos)
    LARGE = 1000.0
    min_dists = []
    for i in range(m):
        d1 = LARGE if i == 0 else sorted_pos[i] - sorted_pos[i - 1]
        d2 = LARGE if i == m - 1 else sorted_pos[i + 1] - sorted_pos[i]
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

def get_penultimate_reps(out: List[List[int]], r: int) -> List[int]:
    positions = get_positions(out, r)
    if not positions or all(c > 7 for c in positions):
        return []
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    n = 16
    if max_d != 1:
        # Gap rule: greedy group starts
        reps = []
        current = None
        for c in sorted_pos:
            if current is None or (c - current) >= 6:
                reps.append(c)
                current = c
        return reps
    else:
        # Pair mode: exact size 2 consecutive components
        components = []
        i = 0
        m = len(sorted_pos)
        while i < m:
            start = i
            j = i + 1
            while j < m and sorted_pos[j] == sorted_pos[j - 1] + 1:
                j += 1
            comp_size = j - start
            if comp_size == 2:
                components.append(sorted_pos[start])
            i = j
        if not components:
            return []
        shift = components[0]
        shifted = [c - shift for c in components]
        # Place shifted in rows 9 and 1
        for c in shifted:
            if 0 <= c < n:
                out[9][c] = 9
                out[1][c] = 9
        # Extra highlight for second pair if exists
        if len(components) >= 2:
            second = components[1]
            out[6][second] = 9
            if second + 1 < n:
                out[6][second + 1] = 9
            out[7][second] = 9
        return []  # Already placed, no additional reps

def apply_replications(out: List[List[int]]):
    n = 16
    for r in range(10, 15):  # 10 to 14
        positions = get_positions(out, r)
        if not positions:
            continue
        if r < 14:
            # Normal rep for rows 10-13
            reps = get_normal_rep(positions)
            if reps:
                u = r - 5
                out[u][reps[0]] = 9
        else:
            # Penultimate for row 14
            reps = get_penultimate_reps(out, r)
            if reps:
                u = 9
                for rep in reps:
                    out[u][rep] = 9

def handle_center_blue(out: List[List[int]], original: List[List[int]]):
    if out[9][7] == 9 and original[14][7] == 9:
        out[9][7] = 1

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy_grid(g)
    original = copy_grid(g)
    apply_replications(out)
    handle_center_blue(out, original)
    return out
```