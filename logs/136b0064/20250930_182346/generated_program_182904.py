```python
from typing import List, Tuple

def get_type(subgrid: List[List[int]]) -> Tuple[int, str]:
    positions = []
    color = None
    for r in range(3):
        for c in range(3):
            val = subgrid[r][c]
            if val != 0:
                if color is None:
                    color = val
                elif color != val:
                    raise ValueError("Inconsistent color in shape")
                positions.append((r, c))
    pos_set = set(positions)
    w_pos = {(0, 0), (0, 1), (1, 0), (1, 2), (2, 1)}
    u_pos = {(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
    c_pos = {(0, 0), (0, 2), (1, 1), (2, 1)}
    h_pos = {(0, 0), (0, 1), (0, 2), (1, 1), (2, 0), (2, 2)}
    if pos_set == w_pos:
        return color, 'W'
    if pos_set == u_pos:
        return color, 'U'
    if pos_set == c_pos:
        return color, 'C'
    if pos_set == h_pos:
        return color, 'H'
    raise ValueError("Unknown shape pattern")

def place_stroke(out: List[List[int]], current_r: int, current_c: int, color: int, typ: str, N: int) -> Tuple[int, int]:
    if typ == 'W':
        start_c = current_c
        for dc in range(3):
            cc = start_c + dc
            if 0 <= cc < 7:
                out[current_r][cc] = color
        current_c = start_c + 2
    elif typ == 'U':
        start_c = current_c
        for dc in range(2):
            cc = start_c - dc
            if 0 <= cc < 7:
                out[current_r][cc] = color
        current_c = start_c - 1
    elif typ == 'C':
        start_r = current_r
        for dr in range(2):
            rr = start_r + dr
            if 0 <= rr < N:
                out[rr][current_c] = color
        current_r = start_r + 1
    elif typ == 'H':
        start_c = current_c
        for dc in range(4):
            cc = start_c - dc
            if 0 <= cc < 7:
                out[current_r][cc] = color
        current_c = start_c - 3
    current_r += 1
    return current_r, current_c

def program(g: List[List[int]]) -> List[List[int]]:
    N = len(g)
    S = -1
    for j in range(15):
        if g[0][j] == 5:
            S = j - 8
            break
    out = [[0] * 7 for _ in range(N)]
    if 0 <= S < 7:
        out[0][S] = 5
    lefts = []
    rights = []
    i = 0
    while i < N:
        if all(g[i][j] == 0 for j in range(7)):
            i += 1
            continue
        if i + 2 >= N:
            break
        block_r = [g[i + k] for k in range(3)]
        left_sub = [[block_r[r][c] for c in range(3)] for r in range(3)]
        right_sub = [[block_r[r][4 + c] for c in range(3)] for r in range(3)]
        l_color, l_typ = get_type(left_sub)
        r_color, r_typ = get_type(right_sub)
        lefts.append((l_color, l_typ))
        rights.append((r_color, r_typ))
        i += 3
    current_r = 1
    current_c = S
    for color, typ in lefts:
        current_r, current_c = place_stroke(out, current_r, current_c, color, typ, N)
    for color, typ in rights:
        current_r, current_c = place_stroke(out, current_r, current_c, color, typ, N)
    return out
```