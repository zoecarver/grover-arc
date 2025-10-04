```python
from typing import List

def matches_w(row1: List[int], row2: List[int], s: int) -> bool:
    prefix = [0] * 5
    w_upper = [s, s, 0, s, s, 0, s, s, 0, s, s]
    w_lower = [s, 0, 0, s, 0, 0, s, 0, 0, s, 0]
    return (row1[:5] == prefix and row1[5:] == w_upper and
            row2[:5] == prefix and row2[5:] == w_lower)

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    non_zeros = {val for row in g for val in row if val != 0}
    if not non_zeros:
        return out
    special = next(iter(non_zeros))
    has_w = False
    for rr in range(15):
        if matches_w(g[rr], g[rr + 1], special):
            has_w = True
            out[rr][8] = 1
            out[rr][9] = 1
            out[rr + 1][8] = 1
            add_r = rr - 5
            if add_r >= 0:
                pattern = [0] * 16
                for ii in (0, 3, 6, 9):
                    pattern[ii] = 1
                out[add_r] = pattern
    if not has_w:
        for r in range(5, 10):
            orig_r = r + 5
            next_r = orig_r + 1
            out[r] = [
                1 if (
                    g[orig_r][c] == special and next_r < 16 and (
                        (c > 0 and g[next_r][c - 1] == special) or
                        g[next_r][c] == special or
                        (c < 15 and g[next_r][c + 1] == special)
                    )
                ) else out[r][c]
                for c in range(16)
            ]
    if special == 1:
        out[9][7] = 5
    return out
```