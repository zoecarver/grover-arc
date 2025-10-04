```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        bg = 0
    else:
        n = len(g)
        m = len(g[0])
        bg = g[0][0]  # default to first element as background
    result = [[bg for _ in range(20)] for _ in range(20)]
    if g and g[0]:
        n = len(g)
        m = len(g[0])
        for i in range(min(n, 20)):
            for j in range(min(m, 20)):
                result[i][j] = g[i][j]
    return result
```