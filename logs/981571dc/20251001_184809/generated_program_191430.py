```python
from typing import List

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
                elif out[j][i] == 0 and out[i][j] != 0:
                    out[j][i] = out[i][j]
                    changed = True
    return out

def fill_with_shift(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    off_shift = 22
    diag_shift = 21
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i, n):
                if out[i][j] == 0:
                    if i == j:
                        s = (i - diag_shift) % n
                        if out[s][s] != 0:
                            out[i][j] = out[s][s]
                            changed = True
                    else:
                        s_i = (i - off_shift) % n
                        s_j = (j - off_shift) % n
                        if out[s_i][s_j] != 0:
                            val = out[s_i][s_j]
                            out[i][j] = val
                            out[j][i] = val
                            changed = True
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    sym = enforce_symmetry(g)
    filled = fill_with_shift(sym)
    return filled
```