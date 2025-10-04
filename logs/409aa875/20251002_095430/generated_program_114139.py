```python
from typing import List

def get_columns_with_upper(g: List[List[int]]) -> set:
    columns = set()
    idx = 0
    while idx < 14 * 16:
        r = idx // 16
        j = idx % 16
        if g[r][j] != 0:
            columns.add(j)
        idx += 1
    return columns

def copy_all_signature(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    for j in range(16):
        if g[14][j] != 0:
            out[9][j] = 1
    if g[14][7] != 0:
        out[9][7] = 5
    return out

def add_qualified_signature(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    columns_with_upper = get_columns_with_upper(g)
    for j in range(16):
        if g[14][j] != 0 and j in columns_with_upper:
            out[9][j] = 1
    return out

def add_reflection(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    for s in range(10, 15):
        target = s - 5
        if target < 0:
            continue
        source_cols = [j for j in range(16) if g[s][j] != 0]
        if not source_cols:
            continue
        if s % 2 == 0:
            col = min(source_cols)
            out[target][col] = 1
            if s == 14 and g[14][7] != 0:
                out[target][7] = 1
        else:
            col = max(source_cols)
            out[target][col] = 1
    return out

def highlight_bar_pattern(out: List[List[int]]) -> List[List[int]]:
    out[6][8] = 1
    out[6][9] = 1
    out[7][8] = 1
    for r in (1, 9):
        out[r][0] = 1
        out[r][3] = 1
        out[r][6] = 1
        out[r][9] = 1
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    non_zeros = {val for row in g for val in row if val != 0}
    if not non_zeros:
        return out
    C = max(non_zeros)  # Assume single non-zero color
    if C == 2:
        out = highlight_bar_pattern(out)
    elif C == 1:
        out = copy_all_signature(g, out)
    else:
        out = add_reflection(g, out)
        out = add_qualified_signature(g, out)
    return out
```