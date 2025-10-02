```python
from typing import List

def get_distinct_colors(grid: List[List[int]]) -> List[int]:
    flat = [cell for row in grid for cell in row]
    colors = set(c for c in flat if c != 0)
    return sorted(colors)

def get_filler(distinct: List[int]) -> int:
    candidates = [c for c in distinct if c >= 5]
    return min(candidates)

def get_extra_colors(distinct: List[int], filler: int) -> List[int]:
    extras = [c for c in distinct if c > 4 and c != filler]
    return sorted(extras, reverse=True)

def get_low_order(distinct: List[int]) -> List[int]:
    low_set = {c for c in distinct if 1 <= c <= 4}
    if not low_set:
        return []
    max_low = max(low_set)
    low_order = []
    if max_low <= 3:
        if 1 in low_set:
            low_order.append(1)
        for c in range(max_low, 1, -1):
            if c in low_set:
                low_order.append(c)
    else:
        if 1 in low_set:
            low_order.append(1)
        if 2 in low_set:
            low_order.append(2)
        for c in range(4, 2, -1):
            if c in low_set:
                low_order.append(c)
    return low_order

def get_bar_colors(distinct: List[int], filler: int) -> List[int]:
    extra = get_extra_colors(distinct, filler)
    low = get_low_order(distinct)
    return extra + low

def get_lengths(k: int) -> List[int]:
    lengths = []
    for r in range(1, k + 1):
        if r <= 2:
            lengths.append(r)
        elif r == k:
            lengths.append(4)
        else:
            lengths.append(3)
    return lengths

def program(g: List[List[int]]) -> List[List[int]]:
    distinct = get_distinct_colors(g)
    filler = get_filler(distinct)
    bar_colors = get_bar_colors(distinct, filler)
    k = len(bar_colors)
    lengths = get_lengths(k)
    grid = []
    for i in range(k):
        colr = bar_colors[i]
        ln = lengths[i]
        row = [colr] * ln + [filler] * (4 - ln)
        grid.append(row)
    return grid
```