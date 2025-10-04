```python
from typing import List, Dict
from math import gcd

def process_line(line: List[int], n: int, is_vertical: bool) -> List[int]:
    out = [0] * n
    for i in range(n):
        if line[i] != 0:
            out[i] = line[i]
    S = [i for i in range(n) if line[i] != 0]
    k = len(S)
    if k < 2:
        return out
    diffs = [S[i + 1] - S[i] for i in range(k - 1)]
    is_perfect_ap = all(d == diffs[0] for d in diffs)
    if is_perfect_ap:
        d = diffs[0]
        c = line[S[0]]
        pos = S[0]
        while pos < n:
            out[pos] = c
            pos += d
        if is_vertical:
            pos = S[0] - d
            while pos >= 0:
                out[pos] = c
                pos -= d
    else:
        if not is_vertical:
            g_val = diffs[0]
            for dd in diffs:
                g_val = gcd(g_val, dd)
            c = line[S[-1]]
            pos = S[0]
            while pos <= S[-1]:
                out[pos] = c
                pos += g_val
        else:
            pos_by_color: Dict[int, List[int]] = {}
            for i in range(n):
                colr = line[i]
                if colr != 0:
                    if colr not in pos_by_color:
                        pos_by_color[colr] = []
                    pos_by_color[colr].append(i)
            for colr, S_c in pos_by_color.items():
                if len(S_c) < 2:
                    continue
                S_c = sorted(S_c)
                diffs_c = [S_c[i + 1] - S_c[i] for i in range(len(S_c) - 1)]
                if all(d == diffs_c[0] for d in diffs_c):
                    d_c = diffs_c[0]
                    start_c = S_c[0]
                    pos = start_c
                    while pos < n:
                        if out[pos] == 0:
                            out[pos] = colr
                        pos += d_c
                    pos = start_c - d_c
                    while pos >= 0:
                        if out[pos] == 0:
                            out[pos] = colr
                        pos -= d_c
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    num_rows = len(g)
    num_cols = len(g[0]) if num_rows > 0 else 0
    if num_rows > num_cols:
        return [process_line(row, num_cols, False) for row in g]
    else:
        out_g = [[0] * num_cols for _ in range(num_rows)]
        for j in range(num_cols):
            col = [g[i][j] for i in range(num_rows)]
            processed = process_line(col, num_rows, True)
            for i in range(num_rows):
                out_g[i][j] = processed[i]
        return out_g
```