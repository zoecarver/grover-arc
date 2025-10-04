```python
from collections import Counter
from typing import List

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_separator_columns(g: List[List[int]], b: int) -> List[int]:
    r = len(g)
    c = len(g[0])
    seps = []
    for j in range(c):
        col_val = g[0][j]
        if col_val != b and all(g[i][j] == col_val for i in range(r)):
            seps.append(j)
    return seps

def calculate_panel_size(c: int, m: int) -> int:
    k = m + 1
    return (c - m) // k

def extract_first_panel(g: List[List[int]], seps: List[int], s: int) -> List[List[int]]:
    r = len(g)
    start = 0
    end = seps[0] if seps else len(g[0])
    out = [row[start:end] for row in g]
    out = [row[:s] for row in out]
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    r = len(g)
    c = len(g[0])
    b = find_background(g)
    seps = find_separator_columns(g, b)
    m = len(seps)
    s = calculate_panel_size(c, m)
    return extract_first_panel(g, seps, s)
```