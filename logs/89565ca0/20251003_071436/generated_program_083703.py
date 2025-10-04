```python
from typing import List

def find_filler(grid: List[List[int]]) -> int:
    for row in grid:
        colors = {c for c in row if c != 0}
        if colors:
            return max(colors)
    return 0

def get_distinct_nonzero(grid: List[List[int]]) -> set[int]:
    colors = set()
    for row in grid:
        colors.update(c for c in row if c != 0)
    return colors

def compute_stats(grid: List[List[int]], colors: set[int]) -> dict[int, tuple[int, float]]:
    h = len(grid)
    stats = {}
    for c in colors:
        total = 0
        sum_r = 0
        for i, row in enumerate(grid):
            cnt = row.count(c)
            total += cnt
            sum_r += i * cnt
        if total > 0:
            avg_r = sum_r / total
            stats[c] = (total, avg_r)
    return stats

def program(g: List[List[int]]) -> List[List[int]]:
    distinct = get_distinct_nonzero(g)
    f = find_filler(g)
    M = distinct - {f}
    if not M:
        return []
    stats = compute_stats(g, M)
    min_tot = min(stats[c][0] for c in M)
    s_cands = [c for c in M if stats[c][0] == min_tot]
    s = max(s_cands)
    remain = M - {s}
    if not remain:
        return [[s, f, f, f]]
    max_av = max(stats[c][1] for c in remain)
    b_cands = [c for c in remain if stats[c][1] == max_av]
    b = max(b_cands)
    mid_set = remain - {b}
    mid = sorted(mid_set)
    order = [s] + mid + [b]
    n = len(order)
    m = n - 2
    mid_widths = [2] + [3] * max(0, m - 1) if m > 0 else []
    widths = [1] + mid_widths + [4]
    out = []
    for i in range(n):
        col = order[i]
        w = widths[i]
        r = [col] * w + [f] * (4 - w)
        out.append(r)
    return out
```