```python
from typing import List, Tuple

def has_full_spine(g: List[List[int]]) -> Tuple[bool, int]:
    n = len(g)
    if n == 0:
        return False, -1
    for col in range(n):
        if all(g[row][col] == 1 for row in range(n)):
            return True, col
    return False, -1

def has_right_1(g: List[List[int]]) -> bool:
    n = len(g)
    if n == 0:
        return False
    m = len(g[0])
    return any(g[i][m - 1] == 1 for i in range(n - 1))

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def apply_left_border(out: List[List[int]], n: int) -> None:
    for i in range(n):
        if out[i][0] == 8:
            out[i][0] = 7

def apply_right_border(out: List[List[int]], n: int, do_right: bool) -> None:
    if not do_right:
        return
    for i in range(n):
        if out[i][n - 1] == 8:
            out[i][n - 1] = 7

def apply_top_fill(out: List[List[int]], top_row_for_1s: List[int], n: int, do_right: bool) -> None:
    minj = next((j for j in range(n) if top_row_for_1s[j] == 1), n)
    for j in range(minj):
        if out[0][j] == 8:
            out[0][j] = 7
    if do_right:
        maxj_list = [j for j in range(n) if top_row_for_1s[j] == 1]
        if maxj_list:
            maxj = max(maxj_list)
            for j in range(maxj + 1, n):
                if out[0][j] == 8:
                    out[0][j] = 7

def apply_bottom_fill(out: List[List[int]], bottom_row_for_1s: List[int], g: List[List[int]], n: int, do_right: bool) -> None:
    row = g[n - 1]
    start = 1 if row[0] == 6 else 0
    minj = next((j for j in range(start, n) if bottom_row_for_1s[j] == 1), n)
    for j in range(start, minj):
        if out[n - 1][j] == 8:
            out[n - 1][j] = 7
    if do_right:
        maxj_list = [j for j in range(n) if bottom_row_for_1s[j] == 1]
        if maxj_list:
            maxj = max(maxj_list)
            for j in range(maxj + 1, n):
                if out[n - 1][j] == 8:
                    out[n - 1][j] = 7

def adjust_non_spine_positions(out: List[List[int]], g: List[List[int]], k: int, n: int) -> None:
    for i in range(n):
        for j in range(n):
            if g[i][j] == 1 and j != k:
                out[i][j] = 7 if j < k else 8

def apply_spine_frame(out: List[List[int]], k: int, n: int) -> None:
    if k == 0:
        return
    for i in range(n):
        if out[i][k - 1] == 8:
            out[i][k - 1] = 7

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n = len(g)
    has_spine, k = has_full_spine(g)
    out = copy_grid(g)
    do_right = has_right_1(g)
    if has_spine:
        adjust_non_spine_positions(out, g, k, n)
    top_row_for_1s = out[0] if has_spine else g[0]
    bottom_row_for_1s = out[n - 1] if has_spine else g[n - 1]
    apply_left_border(out, n)
    apply_right_border(out, n, do_right)
    apply_top_fill(out, top_row_for_1s, n, do_right)
    apply_bottom_fill(out, bottom_row_for_1s, g, n, do_right)
    if has_spine:
        apply_spine_frame(out, k, n)
    return out
```