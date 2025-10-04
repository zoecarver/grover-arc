```python
from typing import List

def get_non_zero_colors(grid: List[List[int]]) -> set[int]:
    colors = set()
    for row in grid:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def get_order_and_accent(non_zero: set[int]) -> tuple[List[int], int]:
    main_set = {1, 2, 3, 4, 8}
    possible_mains = main_set & non_zero
    extras = non_zero - main_set
    accent = list(extras)[0] if extras else 0
    order: List[int] = []
    if 8 in possible_mains:
        order.append(8)
    order.append(1)
    has_four = 4 in possible_mains
    has_three = 3 in possible_mains
    if has_four:
        order.append(2)
        order.append(4)
        if has_three:
            order.append(3)
    else:
        if has_three:
            order.append(3)
        order.append(2)
    return order, accent

def get_widths(num_rows: int) -> List[int]:
    if num_rows == 3:
        return [1, 2, 4]
    elif num_rows == 4:
        return [1, 2, 3, 4]
    elif num_rows == 5:
        return [1, 2, 3, 3, 4]
    else:
        return [1] * num_rows  # fallback, not expected

def program(g: List[List[int]]) -> List[List[int]]:
    non_zero = get_non_zero_colors(g)
    order, accent = get_order_and_accent(non_zero)
    r = len(order)
    widths = get_widths(r)
    output: List[List[int]] = []
    for i in range(r):
        col = order[i]
        w = widths[i]
        row = [col] * w + [accent] * (4 - w)
        output.append(row)
    return output
```