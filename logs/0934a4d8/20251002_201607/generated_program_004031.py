```python
import typing as tp

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    n = 30
    rows_with8 = [i for i in range(n) if 8 in g[i]]
    min_r = min(rows_with8)
    max_r = max(rows_with8)
    h = max_r - min_r + 1
    # find s, w from min_r row
    row = g[min_r]
    s = -1
    w = 0
    current_run = 0
    for j in range(n):
        if row[j] == 8:
            current_run += 1
            if s == -1:
                s = j - current_run + 1
        else:
            current_run = 0
    w = current_run
    # cols
    if s == 0:
        start_col = w
        end_col = w + w
    elif s + w == n:
        start_col = s - w
        end_col = s
    else:
        start_col = s - w
        end_col = s
    cols = list(range(start_col, end_col))
    # rows
    block_rows = list(range(min_r, min_r + h))
    # small
    small = [[g[r][c] for c in cols] for r in block_rows]
    return small
```