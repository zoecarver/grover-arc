```python
from typing import List

def find_yellow_column(g: List[List[int]]) -> int:
    """Find the column index of the yellow element (4)."""
    for row in g:
        for j, cell in enumerate(row):
            if cell == 4:
                return j
    return 0  # Default if not found

def create_background_grid(h: int, w: int) -> List[List[int]]:
    """Create a grid filled with maroon (8)."""
    return [[8 for _ in range(w)] for _ in range(h)]

def fill_red_column(out: List[List[int]], x: int, h: int):
    """Fill the entire column x with red (2), based on yellow position influence."""
    for i in range(h):
        out[i][x] = 2

def remove_non_maroon_elements(out: List[List[int]], g: List[List[int]], h: int, w: int):
    """Remove all colored elements (1,3,4) by setting to maroon (8), absorbing into background."""
    for i in range(h):
        for j in range(w):
            if g[i][j] in (1, 3, 4):
                out[i][j] = 8

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    out = create_background_grid(h, w)
    x = find_yellow_column(g)
    remove_non_maroon_elements(out, g, h, w)
    fill_red_column(out, x, h)
    return out
```