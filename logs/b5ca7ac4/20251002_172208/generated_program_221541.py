```python
from typing import List

def rotate90_clockwise(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    return [[g[n - 1 - j][i] for j in range(n)] for i in range(n)]

def program(g: List[List[int]]) -> List[List[int]]:
    return rotate90_clockwise(g)
```