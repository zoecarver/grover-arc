```python
from typing import List

def flatten_grid(grid: List[List[int]]) -> List[int]:
    return [cell for row in grid for cell in row]

def extract_distinct_colors(flat: List[int]) -> List[int]:
    return sorted({c for c in flat if c != 0})

def select_filler(distinct: List[int]) -> int:
    high_colors = [c for c in distinct if c >= 5]
    return min(high_colors) if high_colors else 0

def extract_extras(distinct: List[int], filler: int) -> List[int]:
    extras = [c for c in distinct if c > 4 and c != filler]
    return sorted(extras, reverse=True)

def order_low_colors(distinct: List[int]) -> List[int]:
    low_set = {c for c in distinct if 1 <= c <= 4}
    if not low_set:
        return []
    max_low = max(low_set)
    low_order = []
    if 1 in low_set:
        low_order.append(1)
    if max_low <= 3:
        for c in range(max_low, 1, -1):
            if c in low_set:
                low_order.append(c)
    else:
        if 2 in low_set:
            low_order.append(2)
        for c in range(4, 2, -1):
            if c in low_set:
                low_order.append(c)
    return low_order

def compute_bar_lengths(num_bars: int) -> List[int]:
    if num_bars == 0:
        return []
    lengths = []
    for pos in range(1, num_bars + 1):
        if pos == 1:
            lengths.append(1)
        elif pos == 2:
            lengths.append(2)
        elif pos == num_bars:
            lengths.append(4)
        else:
            lengths.append(3)
    return lengths

def build_bar(color: int, length: int, filler: int) -> List[int]:
    return [color] * length + [filler] * (4 - length)

def assemble_output(bars: List[int], lengths: List[int], filler: int) -> List[List[int]]:
    return [build_bar(c, l, filler) for c, l in zip(bars, lengths)]

def program(g: List[List[int]]) -> List[List[int]]:
    flat = flatten_grid(g)
    distinct = extract_distinct_colors(flat)
    filler = select_filler(distinct)
    extras = extract_extras(distinct, filler)
    lows = order_low_colors(distinct)
    bars = extras + lows
    lengths = compute_bar_lengths(len(bars))
    return assemble_output(bars, lengths, filler)
```