```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = [list(row) for row in g]
    for ri in range(len(new_g)):
        row = new_g[ri]
        n = len(row)
        divider = -1
        for j in range(n - 1, -1, -1):
            if row[j] != 0:
                divider = j
                break
        if divider == -1:
            continue
        runs = []
        i = 0
        while i < divider:
            if row[i] == 0:
                i += 1
                continue
            c = row[i]
            start = i
            i += 1
            while i < divider and row[i] == c:
                i += 1
            L = i - start
            runs.append((c, L))
        start_fill = divider + 1
        if start_fill < n:
            for c, L in runs:
                rel = 0
                while True:
                    pos = start_fill + rel
                    if pos >= n:
                        break
                    row[pos] = c
                    rel += L
    return new_g
```