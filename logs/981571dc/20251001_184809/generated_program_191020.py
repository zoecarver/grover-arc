```python
from typing import List

def symmetry_fill(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    for i in range(n):
        for j in range(i + 1, n):
            val = out[i][j]
            val2 = out[j][i]
            if val == 0 and val2 != 0:
                out[i][j] = val2
            elif val2 == 0 and val != 0:
                out[j][i] = val
    return out

def fill_remaining(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    for i in range(n):
        for j in range(i, n):
            if out[i][j] == 0:
                if i == j:
                    s = i - 21
                    if 0 <= s < n:
                        out[i][j] = out[s][s]
                else:
                    s_i = i - 22
                    s_j = j - 22
                    if 0 <= s_i < n and 0 <= s_j < n:
                        val = out[s_i][s_j]
                        out[i][j] = val
                        out[j][i] = val
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = symmetry_fill(g)
    out = fill_remaining(out)
    return out
```