```python
from typing import List, Set

def get_non_zero_colors(g: List[List[int]]) -> Set[int]:
    colors: Set[int] = set()
    for row in g:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def get_filler(colors: Set[int]) -> int:
    standard: Set[int] = {1, 2, 3, 4, 8}
    non_standard: List[int] = [c for c in colors if c not in standard]
    return non_standard[0] if non_standard else 0

def get_bar_order(colors: Set[int]) -> List[int]:
    order: List[int] = []
    if 8 in colors:
        order.append(8)
    if 1 in colors:
        order.append(1)
    if 4 in colors:
        if 2 in colors:
            order.append(2)
        order.append(4)
        if 3 in colors:
            order.append(3)
    else:
        if 3 in colors:
            order.append(3)
        if 2 in colors:
            order.append(2)
    return [c for c in order if c in colors]

def get_widths(num_rows: int) -> List[int]:
    if num_rows == 3:
        return [1, 2, 4]
    if num_rows == 4:
        return [1, 2, 3, 4]
    if num_rows == 5:
        return [1, 2, 3, 3, 4]
    return []

def build_row(color: int, width: int, filler: int) -> List[int]:
    effective_width: int = min(width, 4)
    return [color] * effective_width + [filler] * (4 - effective_width)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or all(all(cell == 0 for cell in row) for row in g):
        return []
    colors: Set[int] = get_non_zero_colors(g)
    if not colors:
        return []
    filler: int = get_filler(colors)
    order: List[int] = get_bar_order(colors)
    num_rows: int = len(order)
    if num_rows == 0:
        return []
    widths: List[int] = get_widths(num_rows)
    output: List[List[int]] = []
    for i in range(num_rows):
        row: List[int] = build_row(order[i], widths[i], filler)
        output.append(row)
    return output
```