```python
from typing import List

def has_full_spine(g: List[List[int]]) -> tuple[bool, int]:
    n = len(g)
    for k in range(n):
        if all(g[i][k] == 1 for i in range(n)):
            return True, k
    return False, -1

def clean_other_1s(g: List[List[int]], k: int):
    n = len(g)
    for i in range(n):
        for j in range(n):
            if j != k and g[i][j] == 1:
                g[i][j] = 8

def draw_frame(g: List[List[int]], k: int, n: int):
    # Set left border upper rows to 7 if 8
    for i in range(n - 1):
        if g[i][0] == 8:
            g[i][0] = 7
    # Set column k-1 all rows to 7 if 8
    for i in range(n):
        if g[i][k - 1] == 8:
            g[i][k - 1] = 7
    # Top row full fill 0 to k-1 to 7 if 8
    for j in range(k):
        if g[0][j] == 8:
            g[0][j] = 7
    # Bottom row full fill 1 to k-1 to 7 if 8
    for j in range(1, k):
        if g[n - 1][j] == 8:
            g[n - 1][j] = 7

def fill_non_spine_basic(g: List[List[int]], n: int):
    # Basic handling for non-spine: borders and bottom fill
    # Left border upper
    for i in range(n - 1):
        if g[i][0] == 8:
            g[i][0] = 7
    # Right border all
    for i in range(n):
        if g[i][n - 1] == 8:
            g[i][n - 1] = 7
    # Bottom row all 8 to 7
    i = n - 1
    for j in range(n):
        if g[i][j] == 8:
            g[i][j] = 7

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    has_spine, k = has_full_spine(out)
    if has_spine:
        clean_other_1s(out, k)
        draw_frame(out, k, n)
    else:
        fill_non_spine_basic(out, n)
    return out
```