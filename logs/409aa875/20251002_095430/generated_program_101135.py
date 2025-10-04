```python
from typing import List
from math import inf

def compute_min_dists(positions: List[int]) -> List[int]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    n = len(sorted_pos)
    min_dists = [100] * n  # large number for inf
    for i in range(n):
        c = sorted_pos[i]
        d1 = inf
        d2 = inf
        if i > 0:
            d1 = c - sorted_pos[i - 1]
        if i < n - 1:
            d2 = sorted_pos[i + 1] - c
        min_dists[i] = min(d1, d2)
    return min_dists

def get_normal_rep(positions: List[int]) -> List[int]:
    if not positions:
        return []
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    candidates = []
    for i in range(len(sorted_pos)):
        if min_d_list[i] == max_d:
            candidates.append(sorted_pos[i])
    if candidates:
        return [min(candidates)]  # leftmost
    return []

def get_penultimate_reps(g: List[List[int]], r: int) -> List[int]:
    row = g[r]
    positions = [c for c in range(16) if row[c] != 7]
    if not positions:
        return []
    # check if has left
    if all(c > 7 for c in positions):
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
        n = len(sorted_pos)
        while i < n:
            start = i
            j = i + 1
            while j < n and sorted_pos[j] == sorted_pos[j - 1] + 1:
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
        for c in shifted:
            if 0 <= c < 16:
                g[u][c] = 9
                g[1][c] = 9
        # fill second if possible
        if len(components) >= 2:
            second = components[1]
            g[6][second] = 9
            if second + 1 < 16:
                g[6][second + 1] = 9
            g[7][second] = 9
        return []  # no additional for reps, already set

def replicate_lower(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    for r in range(10, 15):
        u = r - 5
        if u < 0 or u > 9:
            continue
        row = g[r]
        positions = [c for c in range(16) if row[c] != 7]
        if not positions:
            continue
        if all(c > 7 for c in positions):
            continue
        if r == 14:
            reps = get_penultimate_reps(new_g, r)  # note: modifies new_g for pair
        else:
            reps = get_normal_rep(positions)
        for c in reps:
            new_g[u][c] = 9
    return new_g

def handle_center_blue(g: List[List[int]], original_g: List[List[int]]) -> List[List[int]]:
    if g[9][7] == 9 and original_g[14][7] == 9:
        g[9][7] = 1
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = replicate_lower(g)
    new_g = handle_center_blue(new_g, g)
    return new_g
```