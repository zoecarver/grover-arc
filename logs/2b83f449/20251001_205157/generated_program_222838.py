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

def process_top_even(input_row: List[int], below_six: Set[int], w: int) -> List[int]:
    new_row = [0 if input_row[j] == 0 else 8 for j in range(w)]
    for j in below_six:
        if 0 <= j < w and new_row[j] == 8:
            new_row[j] = 6
    return new_row

def apply_protrusion(new_row: List[int], above_six: Set[int], below_six: Set[int], w: int) -> None:
    min_u = min(above_six) if above_six else math.inf
    max_u = max(above_six) if above_six else -math.inf
    min_l = min(below_six) if below_six else math.inf
    max_l = max(below_six) if below_six else -math.inf
    # left protrusion
    if min_u < min_l:
        if new_row[0] == 8:
            new_row[0] = 3
        if min_u <= 4 and 1 < w and new_row[1] == 8:
            new_row[1] = 3
    # right protrusion
    if max_u > max_l:
        if new_row[w - 1] == 8:
            new_row[w - 1] = 3
        if (w - 1 - max_u) <= 4 and w - 2 >= 0 and new_row[w - 2] == 8:
            new_row[w - 2] = 3

def apply_closing_threes(new_row: List[int], w: int) -> None:
    j = 0
    while j < w:
        start = j
        while j < w and new_row[j] != 0:
            j += 1
        end = j - 1
        if end >= start and j < w and new_row[j] == 0:
            has6 = any(new_row[k] == 6 for k in range(start, end + 1))
            if has6 and new_row[end] == 8:
                new_row[end] = 3
        while j < w and new_row[j] == 0:
            j += 1

def apply_bottom_threes(new_row: List[int], w: int) -> None:
    j = 0
    while j < w:
        if new_row[j] == 0:
            j += 1
            continue
        start = j
        has6 = False
        while j < w and new_row[j] != 0:
            if new_row[j] == 6:
                has6 = True
            j += 1
        end = j - 1
        if has6:
            if new_row[start] == 8:
                new_row[start] = 3
            if end == w - 1 and new_row[end] == 8:
                new_row[end] = 3

def process_internal_even(input_row: List[int], above_six: Set[int], below_six: Set[int], w: int, is_bottom: bool) -> List[int]:
    new_row = [0 if input_row[j] == 0 else 8 for j in range(w)]
    all_six = above_six.union(below_six)
    for j in all_six:
        if 0 <= j < w and new_row[j] == 8:
            new_row[j] = 6
    if is_bottom:
        apply_bottom_threes(new_row, w)
    else:
        apply_protrusion(new_row, above_six, below_six, w)
        apply_closing_threes(new_row, w)
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    m = len(g)
    if m == 0:
        return []
    w = len(g[0])
    out = [row[:] for row in g]
    for i in range(1, m, 2):
        if i < m:
            process_content_row(out[i])
    for i in range(0, m, 2):
        if i >= m:
            break
        input_row = g[i]
        if i == 0:
            below_six = get_six_positions(out[1]) if m > 1 else set()
            out[i] = process_top_even(input_row, below_six, w)
        elif i == m - 1:
            above_six = get_six_positions(out[i - 1])
            below_six = set()
            out[i] = process_internal_even(input_row, above_six, below_six, w, True)
        else:
            above_six = get_six_positions(out[i - 1])
            below_six = get_six_positions(out[i + 1]) if i + 1 < m else set()
            out[i] = process_internal_even(input_row, above_six, below_six, w, False)
    return out
```