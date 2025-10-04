```python
from typing import List, Set
from math import inf

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
    w = len(row)
    return {j for j in range(w) if row[j] == 6}

def process_top_even(input_row: List[int], below_six: Set[int]) -> List[int]:
    w = len(input_row)
    new_row = [0 if input_row[j] == 0 else 8 for j in range(w)]
    for j in below_six:
        if new_row[j] == 8:
            new_row[j] = 6
    return new_row

def process_internal_even(input_row: List[int], above_six: Set[int], below_six: Set[int], w: int, is_bottom: bool) -> List[int]:
    new_row = [0 if input_row[j] == 0 else 8 for j in range(w)]
    all_six = above_six.union(below_six)
    for j in all_six:
        if new_row[j] == 8:
            new_row[j] = 6
    a_min = min(above_six) if above_six else float('inf')
    b_min = min(below_six) if below_six else float('inf')
    a_max = max(above_six) if above_six else float('-inf')
    b_max = max(below_six) if below_six else float('-inf')
    zeros_list = [j for j in range(w) if new_row[j] == 0]
    prev = -1
    for curr_z in zeros_list + [w]:
        start = prev + 1
        end = curr_z
        seg_has6 = any(new_row[k] == 6 for k in range(start, end))
        if seg_has6:
            do_left = True
            if start == 0:
                do_left = a_min <= b_min
            if do_left and new_row[start] == 8:
                new_row[start] = 3
            if end < w and not is_bottom and new_row[end - 1] == 8:
                new_row[end - 1] = 3
        prev = curr_z
    # last right special
    last_start = zeros_list[-1] + 1 if zeros_list else 0
    has6_last = any(new_row[k] == 6 for k in range(last_start, w))
    if not is_bottom:
        do_right_last = a_max >= b_max
    else:
        do_right_last = has6_last
    if do_right_last and new_row[w - 1] == 8:
        new_row[w - 1] = 3
    # extras
    if new_row[0] == 3 and a_min <= 4 and 1 < w and new_row[1] == 8:
        new_row[1] = 3
    if new_row[w - 1] == 3 and (w - 1 - a_max) <= 4 and w - 2 >= 0 and new_row[w - 2] == 8:
        new_row[w - 2] = 3
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    m = len(g)
    w = len(g[0])
    out = [row[:] for row in g]
    # Process odd rows
    for i in range(1, m, 2):
        process_content_row(out[i])
    # Process even rows
    for i in range(0, m, 2):
        input_row = g[i]
        if i == 0 and m > 1:
            below_six = get_six_positions(out[1])
            out[i] = process_top_even(input_row, below_six)
        elif i == m - 1 and m > 1:
            above_six = get_six_positions(out[m - 2])
            out[i] = process_internal_even(input_row, above_six, set(), w, True)
        elif m > 2:
            above_six = get_six_positions(out[i - 1])
            below_six = get_six_positions(out[i + 1])
            out[i] = process_internal_even(input_row, above_six, below_six, w, False)
    return out
```