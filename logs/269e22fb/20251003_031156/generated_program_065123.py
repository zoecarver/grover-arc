```python
from typing import List

def get_unique_colors(g: List[List[int]]) -> set:
    colors = set()
    for row in g:
        for cell in row:
            colors.add(cell)
    return colors

def determine_bg_fg(g: List[List[int]]) -> tuple:
    colors = get_unique_colors(g)
    if len(colors) != 2:
        raise ValueError("Grid must have exactly two colors")
    flat = [cell for row in g for cell in row]
    a, b = list(colors)
    count_a = flat.count(a)
    count_b = flat.count(b)
    if count_a > count_b:
        return a, b
    else:
        return b, a

def pad_grid(g: List[List[int]], bg: int, size: int = 20) -> List[List[int]]:
    h = len(g)
    w = len(g[0])
    out = [[bg for _ in range(size)] for _ in range(size)]
    for i in range(min(h, size)):
        for j in range(min(w, size)):
            out[i][j] = g[i][j]
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    bg, fg = determine_bg_fg(g)
    return pad_grid(g, bg)
```