```python
from typing import List

def split_long_runs(g: List[List[int]]) -> List[List[int]]:
    h = [row[:] for row in g]
    for r in range(len(h)):
        c = 0
        n = len(h[r])
        while c < n:
            start = c
            color = h[r][c]
            while c < n and h[r][c] == color:
                c += 1
            l = c - start
            if l >= 3:
                left = start - 1
                right = c
                if left >= 0 and right < n and h[r][left] == h[r][right] and h[r][left] != color:
                    mid = start + l // 2
                    h[r][mid] = h[r][left]
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    return split_long_runs(g)
```