```python
from typing import List, Set, Dict

def get_colors(g: List[List[int]]) -> Set[int]:
    colors: Set[int] = set()
    for row in g:
        for val in row:
            if val != 0:
                colors.add(val)
    return colors

def determine_background(colors: Set[int]) -> int:
    standard = {1, 2, 3, 4, 8}
    non_standard = colors - standard
    return next(iter(non_standard))

def compute_lengths(colors: Set[int]) -> Dict[int, int]:
    has8 = 8 in colors
    lengths: Dict[int, int] = {}
    if 1 in colors:
        lengths[1] = 2 if has8 else 1
    if 2 in colors:
        lengths[2] = 3 if has8 else 4
    if 8 in colors:
        lengths[8] = 1
    has3 = 3 in colors
    has4 = 4 in colors
    if has3 or has4:
        if has4:
            if has8:
                lengths[4] = 3 if has3 else 4
            else:
                lengths[4] = 2
        if has3:
            if has8:
                lengths[3] = 4
            else:
                lengths[3] = 3 if has4 else 2
    return lengths

def get_order(colors: Set[int], lengths: Dict[int, int]) -> List[int]:
    order: List[int] = []
    has8 = 8 in colors
    if 8 in lengths:
        order.append(8)
    if 1 in lengths:
        order.append(1)
    if 2 in lengths and has8:
        order.append(2)
    has3 = 3 in lengths
    has4 = 4 in lengths
    if has4:
        order.append(4)
    if has3:
        order.append(3)
    if 2 in lengths and not has8:
        order.append(2)
    return order

def program(g: List[List[int]]) -> List[List[int]]:
    colors = get_colors(g)
    bg = determine_background(colors)
    lengths = compute_lengths(colors)
    order = get_order(colors, lengths)
    output: List[List[int]] = []
    for col in order:
        length = lengths[col]
        row = [col] * length + [bg] * (4 - length)
        output.append(row)
    return output
```