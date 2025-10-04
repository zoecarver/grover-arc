```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return g
    m = len(g)
    n = len(g[0])
    out = [row[:] for row in g]

    # Fill left border
    for i in range(m):
        if out[i][0] == 8:
            out[i][0] = 7

    # Check for right border condition
    has_right_1 = any(g[i][n - 1] == 1 for i in range(m - 1))
    if has_right_1:
        for i in range(m):
            if out[i][n - 1] == 8:
                out[i][n - 1] = 7

    # Fill top left segment
    i = 0
    for j in range(n):
        if g[i][j] == 1:
            break
        out[i][j] = 7

    # Fill bottom left segment
    i = m - 1
    j_start = 0
    if out[i][0] == 6:
        j_start = 1
    for j in range(j_start, n):
        if g[i][j] == 1:
            break
        out[i][j] = 7

    # Fill top rightmost segment if applicable
    if has_right_1:
        last1 = -1
        for j in range(n):
            if g[0][j] == 1:
                last1 = j
        for j in range(last1 + 1, n):
            out[0][j] = 7

    # Fill bottom rightmost segment if applicable
    if has_right_1:
        last1 = -1
        for j in range(n):
            if g[m - 1][j] == 1:
                last1 = j
        for j in range(last1 + 1, n):
            out[m - 1][j] = 7

    # Compute min_full for full vertical 1 columns
    min_full = n + 1
    for j in range(n):
        is_full = all(g[i][j] == 1 for i in range(m))
        if is_full:
            min_full = min(min_full, j)

    # Dilation: set 8 to 7 if 8-adjacent to a 1, respecting full vertical rules
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(m):
        for j in range(n):
            if out[i][j] == 8:
                for di, dj in directions:
                    ni = i + di
                    nj = j + dj
                    if 0 <= ni < m and 0 <= nj < n and g[ni][nj] == 1:
                        q = nj
                        skip = False
                        if min_full <= n:
                            if q > min_full or (q == min_full and j >= q):
                                skip = True
                        if not skip:
                            out[i][j] = 7
                            break

    return out
```