```python
from typing import List

def extract_distinct_colors(grid: List[List[int]]) -> List[int]:
    flat = [cell for row in grid for cell in row]
    return sorted(set(c for c in flat if c != 0))

def select_filler(distinct: List[int]) -> int:
    highs = [c for c in distinct if c >= 5]
    return min(highs) if highs else 0

def get_extras(distinct: List[int], filler: int) -> List[int]:
    extras = [c for c in distinct if c > 4 and c != filler]
    return sorted(extras, reverse=True)

def order_lows(distinct: List[int]) -> List[int]:
    lows = {c for c in distinct if 1 <= c <= 4}
    if not lows:
        return []
    max_l = max(lows)
    order = []
    if 1 in lows:
        order.append(1)
    if max_l <= 3:
        for c in range(max_l, 1, -1):
            if c in lows:
                order.append(c)
    else:
        if 2 in lows:
            order.append(2)
        for c in range(4, 2, -1):
            if c in lows:
                order.append(c)
    return order

def get_lengths(k: int) -> List[int]:
    if k == 0:
        return []
    lengths = []
    for i in range(1, k + 1):
        if i == 1:
            lengths.append(1)
        elif i == 2:
            lengths.append(2)
        elif i == k:
            lengths.append(4)
        else:
            lengths.append(3)
    return lengths

def build_bar(color: int, length: int, filler: int) -> List[int]:
    return [color] * length + [filler] * (4 - length)

def program(g: List[List[int]]) -> List[List[int]]:
    distinct = extract_distinct_colors(g)
    filler = select_filler(distinct)
    extras = get_extras(distinct, filler)
    lows = order_lows(distinct)
    bars = extras + lows
    lengths = get_lengths(len(bars))
    return [build_bar(c, l, filler) for c, l in zip(bars, lengths)]
```