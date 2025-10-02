```python
from typing import List

def transpose_fill_zeroes(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    for i in range(n):
        for j in range(n):
            if out[i][j] == 0:
                out[i][j] = g[j][i]
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    return transpose_fill_zeroes(g)
```