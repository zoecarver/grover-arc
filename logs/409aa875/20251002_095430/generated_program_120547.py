```python
from typing import List
import math

def program(g: List[List[int]]) -> List[List[int]]:
    h = [row[:] for row in g]
    n = 16
    apply_fork_lift(g, h, n)
    apply_upper_vertical_highlight(g, h, n)
    apply_periodic_header(g, h, n)
    return h

def apply_fork_lift(g: List[List[int]], h: List[List[int]], n: int):
    """Apply the downward fork lift rule: detect forks in rows 1-14 and set 5 rows up to 9 (or 1 if central and original is 9)."""
    for r in range(1, n - 1):
        for c in range(1, n - 1):
            if g[r][c] != 7 and g[r + 1][c - 1] != 7 and g[r + 1][c + 1] != 7:
                target_r = r - 5
                if target_r >= 0:
                    original = g[r][c]
                    new_color = 1 if original == 9 and c == 7 else 9
                    h[target_r][c] = new_color

def apply_upper_vertical_highlight(g: List[List[int]], h: List[List[int]], n: int):
    """Apply the central vertical pair highlight in rows 6-7: find vertical pairs of same non-7 color, highlight the central one and its right neighbor if present."""
    cs = []
    for c in range(n):
        if g[6][c] != 7 and g[7][c] != 7 and g[6][c] == g[7][c]:
            cs.append(c)
    if cs:
        central = min(cs, key=lambda c: abs(c - 7.5))
        h[6][central] = 9
        h[7][central] = 9
        if central + 1 < n and g[6][central + 1] != 7:
            h[6][central + 1] = 9

def apply_periodic_header(g: List[List[int]], h: List[List[int]], n: int):
    """Apply the periodic header in rows 1 and 9 if there are exactly 4 vertical pairs in rows 6-7."""
    cs = []
    for c in range(n):
        if g[6][c] != 7 and g[7][c] != 7 and g[6][c] == g[7][c]:
            cs.append(c)
    if len(cs) == 4:
        for i in range(4):
            col = 3 * i
            h[1][col] = 9
            h[9][col] = 9
```