```python
from typing import List

def preprocess(g: List[List[int]], c: int) -> List[List[int]]:
    n = 12
    new_g = [row[:] for row in g]
    for j in range(n):
        i = 0
        while i < n:
            if new_g[i][j] == c and i > 0:
                start = i
                while i < n and new_g[i][j] == c:
                    i += 1
                length = i - start
                if length == 1 and new_g[start - 1][j] != 0:
                    new_g[start][j] = new_g[start - 1][j]
                else:
                    for k in range(start, i):
                        new_g[k][j] = 0
            else:
                i += 1
    return new_g

def one_pass_gravity(g: List[List[int]]) -> List[List[int]]:
    n = 12
    new_g = [row[:] for row in g]
    for j in range(n):
        for i in range(n - 1, -1, -1):
            if new_g[i][j] != 0 and i + 1 < n and new_g[i + 1][j] == 0:
                new_g[i][j], new_g[i + 1][j] = new_g[i + 1][j], new_g[i][j]
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    n = 12
    c = g[0][0]
    temp = preprocess(g, c)
    for _ in range(n):
        temp = one_pass_gravity(temp)
    return temp
```