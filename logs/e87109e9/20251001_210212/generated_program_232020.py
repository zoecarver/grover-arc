```python
from collections import Counter
from typing import List

def get_background(g: List[List[int]]) -> int:
    flat = [g[r][c] for r in range(6, 25) for c in range(24) if g[r][c] != 0 and g[r][c] != 5]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_bar_colors(g: List[List[int]]) -> tuple:
    row = g[1]
    b1 = next((c for c in row[1:5] if c != 0), 0)
    b2 = next((c for c in row[7:11] if c != 0), 0)
    b3 = next((c for c in row[13:17] if c != 0), 0)
    b4 = next((c for c in row[19:23] if c != 0), 0)
    return b1, b2, b3, b4

def has_merge(b2: int, b3: int) -> bool:
    return b2 == 6 or b3 == 6

def spread_left(row: List[int], bg: int) -> List[int]:
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
            i = end + 1
        else:
            i += 1
    return new_row

def spread_both(row: List[int], bg: int) -> List[int]:
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

def get_pillar_cols(g: List[List[int]]) -> list:
    cols = set()
    for r in range(6, 25):
        for c in range(24):
            if g[r][c] == 8:
                cols.add(c)
    return list(cols)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    b1, b2, b3, b4 = get_bar_colors(g)
    merge = has_merge(b2, b3)
    sub = [row[:] for row in g[6:25]]
    pillar_cols = get_pillar_cols(g) if merge else []
    out = []
    for i in range(19):
        row = sub[i][:]
        has8 = 8 in row
        for j in range(24):
            if row[j] == 0 or row[j] == 5:
                row[j] = bg
        for c in pillar_cols:
            if 0 <= c < 24 and row[c] == bg:
                row[c] = 8
        if has8:
            if merge:
                row = spread_both(row, bg)
            else:
                row = spread_left(row, bg)
        out.append(row)
    return out
```