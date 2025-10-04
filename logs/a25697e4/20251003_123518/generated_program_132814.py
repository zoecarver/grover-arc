```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def apply_column_gravity(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    background = get_background(g)
    new_g = [[background for _ in range(w)] for _ in range(h)]
    for c in range(w):
        col_cells = [g[r][c] for r in range(h)]
        non_background = [cell for cell in col_cells if cell != background]
        stack_top = h - len(non_background)
        for i in range(len(non_background)):
            r = stack_top + i
            new_g[r][c] = non_background[i]
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    return apply_column_gravity(g)
```