```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    new_g = [[8] * w for _ in range(h)]
    c = -1
    for idx in range(h * w):
        r = idx // w
        s = idx % w
        if g[r][s] == 4:
            c = s
            break
    if c != -1:
        for r in range(h):
            new_g[r][c] = 2
    return new_g
```