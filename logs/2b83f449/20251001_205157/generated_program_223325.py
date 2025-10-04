```python
from typing import List, Set
import math

def process_content_row(row: List[int]) -> None:
    j = 0
    w = len(row)
    while j < w - 2:
        if row[j] == 7 and row[j + 1] == 7 and row[j + 2] == 7:
            row[j] = 8
            row[j + 1] = 6
            row[j + 2] = 8
            j += 3
        else:
            j += 1

def get_six_positions(row: List[int]) -> Set[int]:
    return {j for j in range(len(row)) if row[j] == 6}

def apply_protrusion(row: List[int], above_six: Set[int], below_six: Set[int], w: int) -> None:
    if not above_six:
        return
    min_u = min(above_six)
    max_u = max(above_six)
    min_l = min(below_six) if below_six else math.inf
    max_l = max(below_six) if below_six else -math.inf
    # left protrusion
    if min_u < min_l:
        if row[0] == 8:
            row[0] = 3
        if min_u <= 4 and w > 1 and row[1] == 8:
            row[1] = 3
    # right protrusion
    if max_u > max_l:
        if row[w - 1] == 8:
            row[w - 1] = 3
        dist = w - 1 - max_u
        if dist <= 4 and w > 1 and row[w - 2] == 8:
            row[w - 2] = 3

def apply_internal_closures(row: List[int], w: int) -> None:
    j = 0
    while j < w:
        if row[j] == 0:
            j += 1
            continue
        s = j
        has_6 = False
        while j < w and row[j] != 0:
            if row[j] == 6:
                has_6 = True
            j += 1
        e = j - 1
        if has_6:
            # opening 3 if adjacent to 0 on left
            if s > 0 and row[s - 1] == 0 and row[s] == 8:
                row[s] = 3
            # closing 3 if adjacent to 0 on right
            if j < w and row[j] == 0 and row[e] == 8:
                row[e] = 3

def apply_bottom_closures(row: List[int], w: int) -> None:
    j = 0
    while j < w:
        if row[j] == 0:
            j += 1
            continue
        s = j
        has_6 = False
        while j < w and row[j] != 0:
            if row[j] == 6:
                has_6 = True
            j += 1
        e = j - 1
        if has_6:
            # opening 3 at start
            if row[s] == 8:
                row[s] = 3
            # closing 3 only if at right edge
            if e == w - 1 and row[e] == 8:
                row[e] = 3

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    m = len(g)
    w = len(g[0])
    out = [row[:] for row in g]
    # Process odd rows for 7-7-7 replacement
    for i in range(1, m, 2):
        if i < m:
            process_content_row(out[i])
    # Process even rows
    for i in range(0, m, 2):
        if i >= m:
            continue
        input_row = g[i]
        base = [0 if input_row[j] == 0 else 8 for j in range(w)]
        above_six: Set[int] = set()
        below_six: Set[int] = set()
        if i > 0:
            above_six = get_six_positions(out[i - 1])
        if i + 1 < m:
            below_six = get_six_positions(out[i + 1])
        all_six = above_six | below_six
        for j in all_six:
            if 0 <= j < w and base[j] == 8:
                base[j] = 6
        is_top = (i == 0)
        is_bottom = (i == m - 1)
        is_internal = not is_top and not is_bottom
        if is_internal:
            apply_protrusion(base, above_six, below_six, w)
            apply_internal_closures(base, w)
        elif is_bottom:
            apply_bottom_closures(base, w)
        out[i] = base
    return out
```