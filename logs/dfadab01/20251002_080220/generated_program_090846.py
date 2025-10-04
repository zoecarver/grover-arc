```python
from typing import List, Tuple
from typing import Set

def get_yellow_filled() -> Set[Tuple[int, int]]:
    filled = set()
    for i in range(4):
        for j in range(4):
            if not (1 <= i <= 2 and 1 <= j <= 2):
                filled.add((i, j))
    return filled

def get_blue_filled() -> Set[Tuple[int, int]]:
    return {(0,1), (0,2), (1,0), (1,3), (2,0), (2,3), (3,1), (3,2)}

def get_pink_filled() -> Set[Tuple[int, int]]:
    return {(0,0), (0,1), (1,0), (1,1), (2,2), (2,3), (3,2), (3,3)}

def get_darkred_filled() -> Set[Tuple[int, int]]:
    return {(0,0), (0,3), (1,1), (1,2), (2,1), (2,2), (3,0), (3,3)}

def can_place_shape(g: List[List[int]], r: int, c: int, out_col: int, filled_rel: Set[Tuple[int, int]]) -> bool:
    n = len(g)
    # Check filled positions
    for di, dj in filled_rel:
        nr = r + di
        nc = c + dj
        if nr == r and nc == c:
            continue  # seed always allowed
        val = g[nr][nc]
        if val != 0 and val != out_col:
            return False
    # Check hole positions
    for i in range(4):
        for j in range(4):
            if (i, j) in filled_rel:
                continue
            if i == 0 and j == 0:
                continue  # seed exempt
            nr = r + i
            nc = c + j
            if g[nr][nc] != 0:
                return False
    return True

def place_shape(output: List[List[int]], r: int, c: int, out_col: int, filled_rel: Set[Tuple[int, int]]):
    for di, dj in filled_rel:
        output[r + di][c + dj] = out_col

def apply_yellow(g: List[List[int]], output: List[List[int]], r: int, c: int):
    n = len(g)
    if r + 3 >= n or c + 3 >= n:
        return
    out_col = 4
    filled_rel = get_yellow_filled()
    if g[r][c] != 2:
        return
    if can_place_shape(g, r, c, out_col, filled_rel):
        place_shape(output, r, c, out_col, filled_rel)

def apply_blue(g: List[List[int]], output: List[List[int]], r: int, c: int):
    n = len(g)
    if r + 3 >= n or c + 3 >= n:
        return
    out_col = 1
    filled_rel = get_blue_filled()
    if g[r][c] != 3:
        return
    if can_place_shape(g, r, c, out_col, filled_rel):
        place_shape(output, r, c, out_col, filled_rel)

def apply_pink(g: List[List[int]], output: List[List[int]], r: int, c: int):
    n = len(g)
    if r + 3 >= n or c + 3 >= n:
        return
    out_col = 6
    filled_rel = get_pink_filled()
    if g[r][c] != 5:
        return
    if can_place_shape(g, r, c, out_col, filled_rel):
        place_shape(output, r, c, out_col, filled_rel)

def apply_darkred(g: List[List[int]], output: List[List[int]], r: int, c: int):
    n = len(g)
    if r + 3 >= n or c + 3 >= n:
        return
    out_col = 7
    filled_rel = get_darkred_filled()
    if g[r][c] != 8:
        return
    if can_place_shape(g, r, c, out_col, filled_rel):
        place_shape(output, r, c, out_col, filled_rel)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    output = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            k = g[r][c]
            if k == 2:
                apply_yellow(g, output, r, c)
            elif k == 3:
                apply_blue(g, output, r, c)
            elif k == 5:
                apply_pink(g, output, r, c)
            elif k == 8:
                apply_darkred(g, output, r, c)
    return output
```