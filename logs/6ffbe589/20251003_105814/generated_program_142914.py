```python
from typing import List

def get_nonzero_cols_per_row(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    return [[j for j in range(n) if g[i][j] != 0] for i in range(n)]

def find_largest_square_block(g: List[List[int]]) -> tuple:
    n = len(g)
    nonzero_per_row = get_nonzero_cols_per_row(g)
    best_h = 0
    best_start = 0
    best_min_col = 0
    best_nz = 0
    for h in range(n, 0, -1):
        for s in range(n - h + 1):
            rows_nz = nonzero_per_row[s:s + h]
            if not any(rows_nz):
                continue
            min_c = min(min(r) for r in rows_nz if r)
            max_c = max(max(r) for r in rows_nz if r)
            w = max_c - min_c + 1
            nz = sum(len(r) for r in rows_nz)
            if w == h and nz > best_nz:
                best_h = h
                best_start = s
                best_min_col = min_c
                best_nz = nz
    return best_start, best_h, best_min_col

def extract_subgrid(g: List[List[int]], start: int, h: int, min_col: int) -> List[List[int]]:
    return [[g[i][j] for j in range(min_col, min_col + h)] for i in range(start, start + h)]

def program(g: List[List[int]]) -> List[List[int]]:
    start, h, min_col = find_largest_square_block(g)
    return extract_subgrid(g, start, h, min_col)
```