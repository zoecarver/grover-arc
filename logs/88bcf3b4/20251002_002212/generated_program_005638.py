```python
from typing import List
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def fall_down_column(col: List[int], background: int, n: int) -> List[int]:
    non_bg = [x for x in col if x != background]
    new_col = [background] * n
    for idx in range(len(non_bg)):
        new_col[n - 1 - idx] = non_bg[-1 - idx]
    return new_col

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return g
    bg = find_background(g)
    new_g = [row[:] for row in g]
    for j in range(n):
        col = [new_g[i][j] for i in range(n)]
        new_col = fall_down_column(col, bg, n)
        for i in range(n):
            new_g[i][j] = new_col[i]
    return new_g
```