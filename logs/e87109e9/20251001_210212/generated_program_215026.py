```python
from typing import List, Optional, Tuple

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
        while i < n:
            if row[i] == 8:
                start = i
                count = 0
                while i < n and row[i] == 8:
                    i += 1
                    count += 1
                if count >= 2:
                    return (start, start + 1)
            else:
                i += 1
    return None

def has_eight(row: List[int]) -> bool:
    return 8 in row

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
    bar1, bar2, bar3, bar4 = get_bar_colors(g)
    protected = {bar1, bar2, bar3, bar4, 5}
    merge = has_merge(bar2, bar3)
    subgrid = [row[:] for row in g[6:25]]
    pair = get_initial_pair(g)
    original_has = [has_eight(g[6 + i]) for i in range(19)]
    for i in range(19):
        row = subgrid[i]
        if merge and pair is not None and not original_has[i]:
            start, end = pair
            if 0 <= start < len(row) and row[start] not in protected:
                row[start] = 8
            if 0 <= end < len(row) and row[end] not in protected:
                row[end] = 8
        if original_has[i]:
            subgrid[i] = spread_row(subgrid[i], protected)
    return subgrid
```