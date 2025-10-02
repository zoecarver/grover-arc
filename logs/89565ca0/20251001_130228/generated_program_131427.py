```python
from typing import List

def flatten_and_deduplicate(g: List[List[int]]) -> List[int]:
    flat = [cell for row in g for cell in row]
    return sorted({c for c in flat if c != 0})

def select_filler(distinct: List[int]) -> int:
    candidates = [c for c in distinct if c >= 5]
    return min(candidates) if candidates else 0

def extract_highs(distinct: List[int], filler: int) -> List[int]:
    highs = [c for c in distinct if c > 4 and c != filler]
    return sorted(highs, reverse=True)

def order_lows_max_le_3(low_set: set) -> List[int]:
    order = []
    if 1 in low_set:
        order.append(1)
    max_l = max(low_set)
    for c in range(max_l, 1, -1):
        if c in low_set:
            order.append(c)
    return order

def order_lows_max_gt_3(low_set: set) -> List[int]:
    order = []
    if 1 in low_set:
        order.append(1)
    if 2 in low_set:
        order.append(2)
    for c in range(4, 2, -1):
        if c in low_set:
            order.append(c)
    return order

def get_low_order(distinct: List[int]) -> List[int]:
    low_set = {c for c in distinct if 1 <= c <= 4}
    if not low_set:
        return []
    max_low = max(low_set)
    if max_low <= 3:
        return order_lows_max_le_3(low_set)
    return order_lows_max_gt_3(low_set)

def combine_bar_colors(highs: List[int], lows: List[int]) -> List[int]:
    return highs + lows

def compute_lengths(k: int) -> List[int]:
    if k == 0:
        return []
    lengths = []
    for r in range(1, k + 1):
        if r == 1:
            lengths.append(1)
        elif r == 2:
            lengths.append(2)
        elif r == k:
            lengths.append(4)
        else:
            lengths.append(3)
    return lengths

def build_single_bar(color: int, length: int, filler: int) -> List[int]:
    return [color] * length + [filler] * (4 - length)

def assemble_output(bars: List[int], lengths: List[int], filler: int) -> List[List[int]]:
    return [build_single_bar(c, l, filler) for c, l in zip(bars, lengths)]

def program(g: List[List[int]]) -> List[List[int]]:
    distinct = flatten_and_deduplicate(g)
    filler = select_filler(distinct)
    highs = extract_highs(distinct, filler)
    lows = get_low_order(distinct)
    bars = combine_bar_colors(highs, lows)
    lengths = compute_lengths(len(bars))
    return assemble_output(bars, lengths, filler)
```