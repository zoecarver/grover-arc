```python
from typing import List

dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
opposites = [(0, 1), (2, 3)]

def get_num_one_neighbors(g: List[List[int]], r: int, c: int) -> int:
    count = 0
    rows = len(g)
    cols = len(g[0])
    for dr, dc in dirs4:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
            count += 1
    return count

def get_in_dir(g: List[List[int]], r: int, c: int, i: int) -> int:
    dr, dc = dirs4[i]
    nr = r + dr
    nc = c + dc
    rows = len(g)
    cols = len(g[0])
    if 0 <= nr < rows and 0 <= nc < cols:
        return g[nr][nc]
    return 0

def remove_low_connect(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 1:
                num = get_num_one_neighbors(g, r, c)
                if num <= 1:
                    out[r][c] = 0
    return out

def mark_8_adj(out: List[List[int]], r: int, c: int, rows: int, cols: int, exclude_up: bool = False):
    for dr in range(-1, 2):
        if exclude_up and dr == -1:
            continue
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols and out[nr][nc] == 1:
                out[nr][nc] = 7

def remove_thin_protrusions(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    for r in range(rows):
        for c in range(cols):
            if out[r][c] == 1:
                num_non1 = 0
                for dr, dc in dirs4:
                    nr = r + dr
                    nc = c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols):
                        num_non1 += 1
                    elif out[nr][nc] != 1:
                        num_non1 += 1
                if num_non1 >= 3:
                    out[r][c] = 0
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = remove_low_connect(g)
    # first marking pass
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0:
                one_dirs = [i for i in range(4) if get_in_dir(g, r, c, i) == 1]
                num = len(one_dirs)
                if num < 1:
                    continue
                skip = False
                if num == 1:
                    closed_i = one_dirs[0]
                    if closed_i != 3:
                        continue
                    # compute up chain count
                    count = 0
                    cr = r
                    while cr >= 0 and g[cr][c] == 0:
                        count += 1
                        cr -= 1
                    if count != 3:
                        continue
                    # mark 3 right at r
                    for dc2 in range(1, 4):
                        nc2 = c + dc2
                        if nc2 < cols and out[r][nc2] == 1:
                            out[r][nc2] = 7
                    continue
                if num == 3:
                    open_i = next(i for i in range(4) if i not in one_dirs)
                    dr, dc = dirs4[open_i]
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 0 and get_num_one_neighbors(g, nr, nc) == 3:
                        skip = True
                elif num == 2:
                    i1, i2 = sorted(one_dirs)
                    if (i1, i2) in opposites:
                        open_is = [i for i in range(4) if i not in one_dirs]
                        skip = False
                        up_i = 0
                        dr, dc = dirs4[up_i]
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 0 and get_num_one_neighbors(g, nr, nc) >= 2:
                            skip = True
                        if skip:
                            continue
                        # mark 3 right for horizontal
                        if i1 == 2 and i2 == 3:
                            # right
                            if c + 1 < cols and out[r][c + 1] == 1:
                                out[r][c + 1] = 7
                            # up right
                            if r - 1 >= 0 and c + 1 < cols and out[r - 1][c + 1] == 1:
                                out[r - 1][c + 1] = 7
                            # down right
                            if r + 1 < rows and c + 1 < cols and out[r + 1][c + 1] == 1:
                                out[r + 1][c + 1] = 7
                            # up right right
                            if r - 1 >= 0 and c + 2 < cols and out[r - 1][c + 2] == 1:
                                out[r - 1][c + 2] = 7
                            # down right right
                            if r + 1 < rows and c + 2 < cols and out[r + 1][c + 2] == 1:
                                out[r + 1][c + 2] = 7
                        else:
                            # vertical, mark down 3
                            if r + 1 < rows and out[r + 1][c] == 1:
                                out[r + 1][c] = 7
                            if r + 1 < rows and c - 1 >= 0 and out[r + 1][c - 1] == 1:
                                out[r + 1][c - 1] = 7
                            if r + 1 < rows and c + 1 < cols and out[r + 1][c + 1] == 1:
                                out[r + 1][c + 1] = 7
                    else:
                        # L
                        open_is = [i for i in range(4) if i not in one_dirs]
                        skip = True
                        for oi in open_is:
                            drr, dcc = dirs4[oi]
                            nnr = r + drr
                            nnc = c + dcc
                            if not (0 <= nnr < rows and 0 <= nnc < cols and g[nnr][nnc] == 0):
                                skip = False
                                break
                            nnum = get_num_one_neighbors(g, nnr, nnc)
                            if nnum > 1:
                                skip = False
                                break
                        if skip:
                            continue
                        mark_8_adj(out, r, c, rows, cols)
                if not skip:
                    open_i = -1
                    if num == 3:
                        open_i = next(i for i in range(4) if i not in one_dirs)
                    exclude_up = (num == 3 and open_i in [2, 3])
                    mark_8_adj(out, r, c, rows, cols, exclude_up)
    # thin removal
    out = remove_thin_protrusions(out)
    # second marking
    for r in range(rows):
        for c in range(cols):
            if out[r][c] == 0 and g[r][c] == 1:
                one_dirs = [i for i in range(4) if get_in_dir(out, r, c, i) == 1]
                num = len(one_dirs)
                if num == 1:
                    closed_i = one_dirs[0]
                    if closed_i in [1, 3]:
                        dr, dc = dirs4[closed_i]
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and out[nr][nc] == 1:
                            out[nr][nc] = 7
    return out
```