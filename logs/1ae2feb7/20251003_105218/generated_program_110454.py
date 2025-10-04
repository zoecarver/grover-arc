```python
from typing import List

def find_spine_column(g: List[List[int]]) -> int:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    max_count = 0
    spine_col = -1
    for s in range(cols):
        non_zeros = [g[r][s] for r in range(rows) if g[r][s] != 0]
        if non_zeros:
            c = non_zeros[0]
            if all(x == c for x in non_zeros):
                count = len(non_zeros)
                if count > max_count:
                    max_count = count
                    spine_col = s
    return spine_col

def find_run_length(g_row: List[int], start: int, c: int) -> int:
    n = 1
    i = start - 1
    while i >= 0 and g_row[i] == c:
        n += 1
        i -= 1
    return n

def project_run(g_row: List[int], spine_col: int, c: int, n: int) -> None:
    for pos in range(spine_col + 1, len(g_row), n):
        if g_row[pos] == 0:
            g_row[pos] = c

def program(g: List[List[int]]) -> List[List[int]]:
    output = [row[:] for row in g]
    rows = len(output)
    if rows == 0:
        return output
    cols = len(output[0])
    spine_col = find_spine_column(output)
    for r in range(rows):
        row = output[r]
        i = spine_col - 1
        while i >= 0:
            while i >= 0 and row[i] == 0:
                i -= 1
            if i < 0:
                break
            c = row[i]
            n = find_run_length(row, i, c)
            project_run(row, spine_col, c, n)
            i -= n
    return output
```