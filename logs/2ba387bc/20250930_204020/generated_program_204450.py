```python
from typing import List

def extract_subgrid(g: List[List[int]], r: int, c: int) -> List[List[int]]:
    return [[g[r + i][c + j] for j in range(4)] for i in range(4)]

def is_valid_frame(sub: List[List[int]]) -> bool:
    c = None
    for row in sub:
        for val in row:
            if val != 0:
                if c is None:
                    c = val
                elif c != val:
                    return False
    if c is None or c == 0:
        return False
    if sub[1][1] != 0 or sub[1][2] != 0 or sub[2][1] != 0 or sub[2][2] != 0:
        return False
    if any(sub[0][j] != c for j in range(4)):
        return False
    if any(sub[3][j] != c for j in range(4)):
        return False
    if sub[1][0] != c or sub[1][3] != c or sub[2][0] != c or sub[2][3] != c:
        return False
    return True

def is_valid_solid(sub: List[List[int]]) -> bool:
    if not sub or sub[0][0] == 0:
        return False
    c = sub[0][0]
    for row in sub:
        if any(x != c for x in row):
            return False
    return True

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    frames = []
    solids = []
    for r in range(h - 3):
        for c in range(w - 3):
            sub = extract_subgrid(g, r, c)
            if is_valid_solid(sub):
                solids.append((r, c, sub))
            elif is_valid_frame(sub):
                frames.append((r, c, sub))
    frames.sort(key=lambda x: (x[0], x[1]))
    solids.sort(key=lambda x: (x[0], x[1]))
    num_blocks = max(len(frames), len(solids))
    out = []
    empty = [[0] * 4 for _ in range(4)]
    for b in range(num_blocks):
        left = frames[b][2] if b < len(frames) else empty
        right = solids[b][2] if b < len(solids) else empty
        for i in range(4):
            out.append(left[i] + right[i])
    return out
```