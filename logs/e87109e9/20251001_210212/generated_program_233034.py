```python
from typing import List
from collections import Counter

def get_bar_colors(g: List[List[int]]) -> tuple:
    row = g[1]
    bar1 = next((c for c in row[1:5] if c != 0), 0)
    bar2 = next((c for c in row[7:11] if c != 0), 0)
    bar3 = next((c for c in row[13:17] if c != 0), 0)
    bar4 = next((c for c in row[19:23] if c != 0), 0)
    return bar1, bar2, bar3, bar4

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g[6:25] for cell in row if cell != 0 and cell != 5]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def spread_row(row: List[int], protected: set, bg: int) -> List[int]:
    new_row = row[:]
    n = len(new_row)
    i = 0
    while i < n:
        if new_row[i] == 8:
            start = i
            while i < n and new_row[i] == 8:
                i += 1
            end = i - 1
            j = start - 1
            while j >= 0 and new_row[j] == bg:
                new_row[j] = 8
                j -= 1
            j = end + 1
            while j < n and new_row[j] == bg:
                new_row[j] = 8
                j += 1
            i = j
        else:
            i += 1
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g[6:25]]
    bar1, bar2, bar3, bar4 = get_bar_colors(g)
    protected = {bar1, bar2, bar3, bar4, 5}
    bg = get_background(g)
    for i in range(len(out)):
        if 8 in out[i]:
            out[i] = spread_row(out[i], protected, bg)
    return out
```