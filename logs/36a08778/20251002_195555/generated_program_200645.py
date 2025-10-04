```python
from typing import List

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_num_rows(g: List[List[int]]) -> int:
    return len(g)

def get_num_cols(g: List[List[int]]) -> int:
    return len(g[0]) if g else 0

def apply_pour_to_row(prev_row: List[int], curr_input_row: List[int]) -> List[int]:
    m = len(curr_input_row)
    result = curr_input_row[:]
    for j in range(m):
        if prev_row[j] == 6 and curr_input_row[j] == 7:
            result[j] = 6
    return result

def get_2_groups(row: List[int]) -> List[tuple[int, int]]:
    groups = []
    m = len(row)
    i = 0
    while i < m:
        if row[i] == 2:
            l = i
            while i < m and row[i] == 2:
                i += 1
            r = i - 1
            groups.append((l, r))
        else:
            i += 1
    return groups

def apply_cap_spread(curr_row: List[int], next_row: List[int], orig_row: List[int]) -> List[int]:
    m = len(curr_row)
    result = curr_row[:]
    groups = get_2_groups(next_row)
    for l, r in groups:
        triggered = False
        j = l
        while j <= r:
            if curr_row[j] == 6:
                triggered = True
                break
            j += 1
        if triggered:
            start_c = max(0, l - 1)
            end_c = min(m - 1, r + 1)
            c = start_c
            while c <= end_c:
                if orig_row[c] == 7:
                    result[c] = 6
                c += 1
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    output = copy_grid(g)
    n = get_num_rows(g)
    m = get_num_cols(g)
    for k in range(n):
        if k > 0:
            output[k] = apply_pour_to_row(output[k - 1], g[k])
        if k + 1 < n:
            output[k] = apply_cap_spread(output[k], g[k + 1], g[k])
    return output
```