```python
from typing import List

def mirror_rows(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    for k in range(2, 16):
        m = 31 - k
        if m < n:
            out[m] = out[k][:]
    return out

def enforce_symmetry(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                if out[i][j] == 0 and out[j][i] != 0:
                    out[i][j] = out[j][i]
                    changed = True
                if out[j][i] == 0 and out[i][j] != 0:
                    out[j][i] = out[i][j]
                    changed = True
    return out

def fill_remaining(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    diag_shift = 21
    off_shift = 22
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i, n):
                if out[i][j] == 0:
                    if i == j:
                        s = (i - diag_shift) % n
                        if out[s][s] != 0:
                            val = out[s][s]
                            out[i][j] = val
                            changed = True
                    else:
                        s_i = (i - off_shift) % n
                        s_j = (j - off_shift) % n
                        if out[s_i][s_j] != 0:
                            val = out[s_i][s_j]
                            out[i][j] = val
                            if out[j][i] == 0:
                                out[j][i] = val
                            changed = True
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = mirror_rows(g)
    out = enforce_symmetry(out)
    out = mirror_rows(out)
    out = enforce_symmetry(out)
    out = fill_remaining(out)
    return out
```