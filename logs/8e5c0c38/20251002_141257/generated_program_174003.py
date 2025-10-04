```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    n = len(g)
    m = len(g[0])
    flat = [cell for row in g for cell in row]
    bg = max(set(flat), key=flat.count)
    bases = [
        [[0,0,0], [0,1,0], [0,0,0]],
        [[0,0,0], [0,1,0], [0,1,1]],
        [[0,0,0], [0,1,1], [0,0,1]],
        [[1,1,0], [0,1,1], [0,0,0]],
        [[0,0,0], [0,1,1], [0,1,1]],
        [[0,1,1], [0,1,1], [0,0,0]],
        [[1,1,1], [1,1,0], [0,0,0]],
        [[0,0,1], [0,1,1], [0,1,1]],
    ]
    def rotate90(p: List[List[int]]) -> List[List[int]]:
        return [list(row) for row in zip(*p[::-1])]
    bad_patterns = set()
    for base in bases:
        current = [row[:] for row in base]
        for _ in range(4):
            flat_pat = tuple(item for sublist in current for item in sublist)
            bad_patterns.add(flat_pat)
            current = rotate90(current)
    new_g = [row[:] for row in g]
    for r in range(1, n-1):
        for c in range(1, m-1):
            color = g[r][c]
            if color == bg:
                continue
            bin_pat = [[1 if g[r + i - 1][c + j - 1] == color else 0 for j in range(3)] for i in range(3)]
            flat_pat = tuple(item for sublist in bin_pat for item in sublist)
            if flat_pat in bad_patterns:
                new_g[r][c] = bg
    return new_g
```