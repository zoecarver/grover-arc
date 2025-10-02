```python
from typing import List

def flatten_and_extract_distinct(g: List[List[int]]) -> List[int]:
    flat = [cell for row in g for cell in row]
    return sorted({c for c in flat if c != 0})

def select_filler(distinct: List[int]) -> int:
    high = [c for c in distinct if c >= 5]
    return min(high) if high else 0

def extract_extras(distinct: List[int], filler: int) -> List[int]:
    extras = [c for c in distinct if c > 4 and c != filler]
    return sorted(extras, reverse=True)

def order_low_colors(distinct: List[int]) -> List[int]:
    low_set = {c for c in distinct if 1 <= c <= 4}
    if not low_set:
        return []
    max_low = max(low_set)
    order = []
    if 1 in low_set:
        order.append(1)
    if max_low <= 3:
        for c in range(max_low, 1, -1):
            if c in low_set:
                order.append(c)
    else:
        if 2 in low_set:
            order.append(2)
        for c in range(4, 2, -1):
            if c in low_set:
                order.append(c)
    return order

def compute_lengths(k: int) -> List[int]:
    if k == 0:
        return []
    lengths = []
    for pos in range(1, k + 1):
        if pos == 1:
            lengths.append(1)
        elif pos == 2:
            lengths.append(2)
        elif pos == k:
            lengths.append(4)
        else:
            lengths.append(3)
    return lengths

def build_single_bar(color: int, length: int, filler: int) -> List[int]:
    return [color] * length + [filler] * (4 - length)

def assemble_bars(bar_colors: List[int], lengths: List[int], filler: int) -> List[List[int]]:
    return [build_single_bar(c, l, filler) for c, l in zip(bar_colors, lengths)]

def program(g: List[List[int]]) -> List[List[int]]:
    distinct = flatten_and_extract_distinct(g)
    filler = select_filler(distinct)
    extras = extract_extras(distinct, filler)
    lows = order_low_colors(distinct)
    bar_colors = extras + lows
    lengths = compute_lengths(len(bar_colors))
    return assemble_bars(bar_colors, lengths, filler)
```