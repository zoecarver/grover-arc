```python
from typing import List, Set

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
    if not positions or all(c > 7 for c in positions):
        return []
    sorted_pos = sorted(positions)
    min_d_list = compute_min_dists(sorted_pos)
    max_d = max(min_d_list)
    candidates = [sorted_pos[i] for i in range(len(sorted_pos)) if min_d_list[i] == max_d]
    if candidates:
        return [min(candidates)]
    return []

def find_matching_upper_row(grid: List[List[int]]) -> int:
    bottom0: Set[int] = {x for x in range(16) if grid[14][x] != 7}
    bottom1: Set[int] = {x for x in range(16) if grid[15][x] != 7}
    for u in range(15):
        upper0: Set[int] = {x for x in range(16) if grid[u][x] != 7}
        upper1: Set[int] = {x for x in range(16) if grid[u + 1][x] != 7}
        if upper0 == bottom0 and upper1 == bottom1:
            return u
    return -1

def get_projected_cols_from_bottom(g: List[List[int]]) -> List[int]:
    pos = [x for x in range(16) if g[15][x] != 7]
    if not pos:
        return []
    color = g[15][pos[0]]
    sorted_pos = sorted(pos)
    if len(sorted_pos) < 2:
        return sorted_pos
    diffs = [sorted_pos[i + 1] - sorted_pos[i] for i in range(len(sorted_pos) - 1)]
    if all(d == diffs[0] for d in diffs):
        d = diffs[0]
        return [i * d for i in range(len(sorted_pos))]
    groups = []
    curr = [sorted_pos[0]]
    for i in range(1, len(sorted_pos)):
        if sorted_pos[i] - curr[-1] == 2:
            curr.append(sorted_pos[i])
        else:
            groups.append(curr)
            curr = [sorted_pos[i]]
    groups.append(curr)
    projected = []
    for grp in groups:
        l = len(grp)
        if l == 1:
            projected.append(grp[0])
        else:
            projected.append((grp[0] + grp[-1]) // 2)
    return projected

def get_pair_starts(g: List[List[int]], r: int) -> List[int]:
    row = g[r]
    pos = [c for c in range(16) if row[c] != 7]
    sorted_pos = sorted(set(pos))
    components = []
    i = 0
    while i < len(sorted_pos):
        start_i = i
        j = i + 1
        while j < len(sorted_pos) and sorted_pos[j] == sorted_pos[j - 1] + 1:
            j += 1
        size = j - start_i
        if size == 2:
            components.append(sorted_pos[start_i])
        i = j
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    n = 16
    out = [row[:] for row in g]
    u = find_matching_upper_row(g)
    projected = get_projected_cols_from_bottom(g)
    color = 7
    pos = [x for x in range(n) if g[15][x] != 7]
    if pos:
        color = g[15][pos[0]]
    mid_p = None
    if projected and len(projected) > 1 and len(projected) % 2 == 1 and color == 9:
        proj_sorted = sorted(projected)
        mid_p = proj_sorted[len(projected) // 2]
    # Place in row 9
    for p in projected:
        if 0 <= p < n:
            val = 1 if mid_p is not None and p == mid_p else 9
            out[9][p] = val
    if u != -1:
        # Place in u-5 all 9
        for p in projected:
            if 0 <= p < n:
                out[u - 5][p] = 9
        # Fill second component
        starts = get_pair_starts(g, 14)
        if len(starts) >= 2:
            second = starts[1]
            out[u][second] = 9
            if second + 1 < n:
                out[u][second + 1] = 9
            out[u + 1][second] = 9
    else:
        # Inner reps for r=10 to 13
        for r in range(10, 14):
            positions = [c for c in range(n) if g[r][c] != 7]
            if positions and not all(c > 7 for c in positions):
                reps = get_normal_rep(positions)
                for p in reps:
                    if 0 <= p < n:
                        out[r - 5][p] = 9
    # Center override
    if out[9][7] == 9 and g[14][7] == 9:
        out[9][7] = 1
    return out
```