```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    h = [row[:] for row in g]
    pattern_set = set()
    for row in g:
        for val in row:
            if val != 8:
                pattern_set.add(val)
    if not pattern_set:
        return h
    p = list(pattern_set)[0]  # Assume single pattern color
    for i in range(n):
        for j in range(n):
            if h[i][j] != 8:
                continue
            do_set = False
            # Vertical from above 2: if above is 2 and (left is 2 or not right is p)
            if i > 0 and h[i - 1][j] == 2:
                right_p = j + 1 < n and g[i][j + 1] == p
                left_support = j > 0 and h[i][j - 1] == 2
                if left_support or not right_p:
                    do_set = True
            # Horizontal from left 2: if left is 2 and not right is p
            if j > 0 and h[i][j - 1] == 2:
                right_p = j + 1 < n and g[i][j + 1] == p
                if not right_p:
                    do_set = True
            # Vertical from above p: if above is p and right of above is 8 and not (left of above is 2 and the one above that is 2)
            if i > 0 and g[i - 1][j] == p:
                if j + 1 < n and g[i - 1][j + 1] == 8:
                    block = False
                    if j > 0 and h[i - 1][j - 1] == 2:
                        if i > 1 and h[i - 2][j - 1] == 2:
                            block = True
                    if not block:
                        do_set = True
            if do_set:
                h[i][j] = 2
    return h
```