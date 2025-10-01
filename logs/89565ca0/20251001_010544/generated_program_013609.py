```python
from typing import List, Set

def extract_colors(g: List[List[int]]) -> Set[int]:
    return {c for row in g for c in row if c != 0}

def get_background(colors: Set[int]) -> int:
    standard = {1, 2, 3, 4, 8}
    return next(iter(colors - standard))

def has_eight(colors: Set[int]) -> bool:
    return 8 in colors

def compute_length(color: int, colors: Set[int]) -> int:
    has8 = has_eight(colors)
    if color == 8:
        return 1
    if color == 1:
        return 2 if has8 else 1
    if color == 2:
        return 3 if has8 else 4
    if color == 3:
        if has8:
            return 4
        return 3 if 4 in colors else 2
    if color == 4:
        if has8:
            return 3 if 3 in colors else 4
        return 2
    return 0

def get_order(colors: Set[int]) -> List[int]:
    order: List[int] = []
    if 8 in colors:
        order.append(8)
    if 1 in colors:
        order.append(1)
    if 2 in colors and has_eight(colors):
        order.append(2)
    if 4 in colors or 3 in colors:
        if 4 in colors:
            order.append(4)
        if 3 in colors:
            order.append(3)
    if 2 in colors and not has_eight(colors):
        order.append(2)
    return order

def build_row(color: int, length: int, background: int) -> List[int]:
    return [color] * length + [background] * (4 - length)

def program(g: List[List[int]]) -> List[List[int]]:
    colors = extract_colors(g)
    background = get_background(colors)
    order = get_order(colors)
    rows: List[List[int]] = []
    for color in order:
        length = compute_length(color, colors)
        if length > 0:
            rows.append(build_row(color, length, background))
    return rows
```