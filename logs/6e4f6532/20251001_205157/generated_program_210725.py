```python
from typing import List

def is_uniform(row: List[int]) -> bool:
    if not row:
        return True
    c = row[0]
    return all(x == c for x in row)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    top = 0
    while top < n and is_uniform(g[top]):
        top += 1
    bottom = 0
    while bottom < n - top and is_uniform(g[n - 1 - bottom]):
        bottom += 1
    canvas_start = top
    canvas_end = n - bottom
    canvas = g[canvas_start:canvas_end]
    reversed_canvas = canvas[::-1]
    return g[:canvas_start] + reversed_canvas + g[canvas_end:]
```