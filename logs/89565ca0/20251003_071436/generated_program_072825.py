```python
from typing import List, Dict, Set

def get_fill_color(g: List[List[int]]) -> int:
    for row in g:
        non_zero = [c for c in row if c != 0]
        if non_zero:
            return max(non_zero)
    return 0

def compute_min_rows(g: List[List[int]]) -> Dict[int, int]:
    min_rows: Dict[int, int] = {}
    for r, row in enumerate(g):
        seen = set(row)
        for c in seen:
            if c != 0 and (c not in min_rows or r < min_rows[c]):
                min_rows[c] = r
    return min_rows

def program(g: List[List[int]]) -> List[List[int]]:
    fill = get_fill_color(g)
    all_nonzero: Set[int] = set()
    for row in g:
        for c in row:
            if c > 0:
                all_nonzero.add(c)
    foreground = all_nonzero - {fill}
    min_rows = compute_min_rows(g)
    order: List[int] = []
    if 8 in foreground:
        order.append(8)
        low_colors = [1, 2]
    else:
        low_colors = [1]
    for lc in low_colors:
        if lc in foreground:
            order.append(lc)
    remaining = [c for c in foreground if c not in order]
    remaining.sort(key=lambda c: min_rows.get(c, float('inf')))
    order.extend(remaining)
    num_rows = len(order)
    output: List[List[int]] = []
    for i, col in enumerate(order):
        if i == num_rows - 1:
            num_rep = 4
        else:
            num_rep = min(i + 1, 3)
        row_out = [col] * num_rep + [fill] * (4 - num_rep)
        output.append(row_out)
    return output
```