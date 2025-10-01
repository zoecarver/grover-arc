```python
from typing import List
import copy

def program(g: List[List[int]]) -> List[List[int]]:
    n = 30
    h = copy.deepcopy(g)
    for i in range(n):
        for j in range(n):
            if h[i][j] == 0:
                h[i][j] = g[j][i]
    return h
```