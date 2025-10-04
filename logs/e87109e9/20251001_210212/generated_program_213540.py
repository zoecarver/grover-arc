```python
from collections import Counter
from typing import List

def get_bar_colors(g: List[List[int]]) -> tuple:
    row = g[1]
    bar1 = next((c for c in row[1:5] if c != 0), 0)
    bar2 = next((c for c in row[7:11] if c != 0), 0)
    bar3 = next((c for c in row[13:17] if c != 0), 0)
    bar4 = next((c for c in row[19:23] if c != 0), 0)
    return bar1, bar2, bar3, bar4

def has_merge(bar2: int, bar3: int) -> bool:
    return bar2 == 6 or bar3 == 6

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def spread_row(row: List[int], background: int) -> List[int]:
    new_row = row.copy()
    i = 0
    n = len(new_row)
    while i < n:
        if new_row[i] == 8:
            start = i
            while i < n and new_row[i] == 8:
                i += 1
            end = i - 1
            j = start - 1
            while j >= 0 and new_row[j] == background:
                new_row[j] = 8
                j -= 1
            j = end + 1
            while j < n and new_row[j] == background:
                new_row[j] = 8
                j += 1
            i = j
        else:
            i += 1
    return new_row

def get_initial_pair(g: List[List[int]]) -> tuple:
    for row in g[6:25]:
        i = 0
        n = len(row)
        while i < n:
            if row[i] == 8:
                start = i
                while i < n and row[i] == 8:
                    i += 1
                end = i - 1
                if end - start + 1 >= 2:
                    return (start, start + 1)
                i = end + 1
            else:
                i += 1
    return None

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row.copy() for row in g[6:25]]
    background = get_background(g)
    bar1, bar2, bar3, bar4 = get_bar_colors(g)
    if has_merge(bar2, bar3):
        pair = get_initial_pair(g)
        if pair:
            p1, p2 = pair
            for row in out:
                if p1 < len(row) and row[p1] == background:
                    row[p1] = 8
                if p2 < len(row) and row[p2] == background:
                    row[p2] = 8
    for i in range(len(out)):
        if 8 in g[6 + i]:
            out[i] = spread_row(out[i], background)
    return out
```