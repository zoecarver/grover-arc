```python
from typing import List
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    grid = [row[:] for row in g]
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    if w == 0:
        return grid
    W = grid[0][0]
    F = grid[1][1]
    # Detect wall columns from floor row
    walls = sorted([j for j in range(w) if grid[1][j] == W])
    # Skip border and floor rows (assuming symmetric top/bottom)
    skip_rows = {0, 1, h-2, h-1}
    for r in range(h):
        if r in skip_rows:
            continue
        row = grid[r]
        for k in range(len(walls) - 1):
            left = walls[k]
            right = walls[k + 1]
            room_start = left + 1
            room_end = right - 1
            if room_start > room_end:
                continue
            # Find pattern segment skipping leading/trailing F
            ps = room_start
            while ps <= room_end and row[ps] == F:
                ps += 1
            pe = room_end
            while pe >= ps and row[pe] == F:
                pe -= 1
            if ps > pe:
                continue
            L = pe - ps + 1
            # Colors in pattern segment excluding W and F
            room_colors = set(row[j] for j in range(ps, pe + 1)) - {W, F}
            if len(room_colors) != 1:
                continue
            C = next(iter(room_colors))
            # Compute group sizes of C in pattern segment
            group_sizes = []
            i = ps
            while i <= pe:
                if row[i] == C:
                    sz = 0
                    while i <= pe and row[i] == C:
                        sz += 1
                        i += 1
                    group_sizes.append(sz)
                else:
                    i += 1
            if not group_sizes:
                continue
            cnt = Counter(group_sizes)
            max_freq = cnt.most_common(1)[0][1]
            K_list = [kv[0] for kv in cnt.items() if kv[1] == max_freq]
            # Find best pattern across possible K
            min_diff = float('inf')
            best_pattern = None
            first_val = row[ps]
            for K in K_list:
                p_ = K + 1
                for s in range(p_):
                    exp_first_pos = s % p_
                    exp_first = C if exp_first_pos < K else W
                    if exp_first != first_val:
                        continue
                    this_diff = 0
                    this_pattern = []
                    for ii in range(L):
                        pos = (ii + s) % p_
                        exp = C if pos < K else W
                        j = ps + ii
                        if exp != row[j]:
                            this_diff += 1
                        this_pattern.append(exp)
                    if this_diff < min_diff:
                        min_diff = this_diff
                        best_pattern = this_pattern
            # Apply if improvement (min_diff > 0 means changes needed)
            if best_pattern is not None and min_diff > 0:
                for ii in range(L):
                    j = ps + ii
                    row[j] = best_pattern[ii]
    return grid
```