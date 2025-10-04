```python
from typing import List, Optional, Tuple
from collections import Counter

def get_bar_colors(g: List[List[int]]) -> Tuple[int, int, int, int]:
    row = g[1]
    bar1 = next((c for c in row[1:5] if c != 0), 0)
    bar2 = next((c for c in row[7:11] if c != 0), 0)
    bar3 = next((c for c in row[13:17] if c != 0), 0)
    bar4 = next((c for c in row[19:23] if c != 0), 0)
    return bar1, bar2, bar3, bar4

def has_merge(bar2: int, bar3: int) -> bool:
    return bar2 == 6 or bar3 == 6

def get_initial_pair(g: List[List[int]]) -> Optional[Tuple[int, int]]:
    for row in g[6:25]:
        i = 0
        n = len(row)
        while i < n - 1:
            if row[i] == 8 and row[i + 1] == 8:
                return (i, i + 1)
            i += 1
    return None

def spread_row(row: List[int], protected: set) -> List[int]:
    new_row = row.copy()
    n = len(new_row)
    i = 0
    while i < n:
        if new_row[i] == 8:
            start = i
            while i < n and new_row[i] == 8:
                i += 1
            end = i - 1
            j = start - 1
            while j >= 0 and new_row[j] not in protected:
                new_row[j] = 8
                j -= 1
            j = end + 1
            while j < n and new_row[j] not in protected:
                new_row[j] = 8
                j += 1
            i = j
        else:
            i += 1
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    bars = get_bar_colors(g)
    bar1, bar2, bar3, bar4 = bars
    protected = {bar1, bar2, bar3, bar4, 5}
    if not has_merge(bar2, bar3):
        return [row.copy() for row in g[6:25]]
    pair = get_initial_pair(g)
    out = []
    for i in range(19):
        row = g[6 + i].copy()
        has8 = 8 in row
        if has8:
            row = spread_row(row, protected)
        elif pair is not None:
            c1, c2 = pair
            if c1 < len(row) and row[c1] not in protected:
                row[c1] = 8
            if c2 < len(row) and row[c2] not in protected:
                row[c2] = 8
        out.append(row)
    return out
```