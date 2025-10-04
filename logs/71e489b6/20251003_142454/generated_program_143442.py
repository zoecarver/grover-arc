```python
from typing import List

def get_neighbor(g: List[List[int]], i: int, j: int, di: int, dj: int) -> int:
    rows = len(g)
    cols = len(g[0])
    ni = i + di
    nj = j + dj
    if 0 <= ni < rows and 0 <= nj < cols:
        return g[ni][nj]
    return 0

def remove_isolated(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if out[i][j] == 1:
                num_adj = sum(1 for di, dj in directions if get_neighbor(out, i, j, di, dj) == 1)
                if num_adj == 0:
                    out[i][j] = 0
    return out

def handle_patterns(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    eight_dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    def get(i: int, j: int) -> int:
        if 0 <= i < rows and 0 <= j < cols:
            return out[i][j]
        return 0
    def setv(i: int, j: int, val: int):
        if 0 <= i < rows and 0 <= j < cols:
            out[i][j] = val
    for i in range(rows):
        for j in range(cols):
            if out[i][j] == 0:
                num_1 = sum(1 for di, dj in directions if get(i + di, j + dj) == 1)
                if num_1 == 4:
                    for di, dj in eight_dirs:
                        ni = i + di
                        nj = j + dj
                        if get(ni, nj) == 1:
                            setv(ni, nj, 7)
                elif num_1 == 3:
                    open_dir = -1
                    for k in range(4):
                        di, dj = directions[k]
                        if get(i + di, j + dj) != 1:
                            open_dir = k
                            break
                    if open_dir != -1:
                        di, dj = directions[open_dir]
                        ni0 = i + di
                        nj0 = j + dj
                        is_internal = 0 <= ni0 < rows and 0 <= nj0 < cols and out[ni0][nj0] == 0
                        # set closed orthogonals
                        for k in range(4):
                            if k != open_dir:
                                ddi, ddj = directions[k]
                                setv(i + ddi, j + ddj, 7)
                        if open_dir == 0:  # open up
                            # fill interior down 3 horizontal
                            setv(i + 1, j - 1, 7)
                            setv(i + 1, j, 7)
                            setv(i + 1, j + 1, 7)
                            # set sides already done
                            if is_internal:
                                # fill open up 3 horizontal, with condition
                                for off in [-1, 0, 1]:
                                    pi = i - 1
                                    pj = j + off
                                    if get(pi, pj) == 0:
                                        p_num = sum(1 for ddi, ddj in directions if get(pi + ddi, pj + ddj) == 1)
                                        if p_num < 2:
                                            setv(pi, pj, 7)
                                    else:
                                        setv(pi, pj, 7)
                        elif open_dir == 1:  # open down
                            # fill interior up 3 horizontal
                            setv(i - 1, j - 1, 7)
                            setv(i - 1, j, 7)
                            setv(i - 1, j + 1, 7)
                            # fill open down 3 horizontal, with condition
                            for off in [-1, 0, 1]:
                                pi = i + 1
                                pj = j + off
                                if get(pi, pj) == 0:
                                    p_num = sum(1 for ddi, ddj in directions if get(pi + ddi, pj + ddj) == 1)
                                    if p_num < 2:
                                        setv(pi, pj, 7)
                                else:
                                    setv(pi, pj, 7)
                        elif open_dir == 2:  # open left
                            # fill interior right 3 vertical
                            setv(i - 1, j + 1, 7)
                            setv(i, j + 1, 7)
                            setv(i + 1, j + 1, 7)
                            if is_internal:
                                # fill open left 3 vertical, with condition
                                for off in [-1, 0, 1]:
                                    pi = i + off
                                    pj = j - 1
                                    if get(pi, pj) == 0:
                                        p_num = sum(1 for ddi, ddj in directions if get(pi + ddi, pj + ddj) == 1)
                                        if p_num < 2:
                                            setv(pi, pj, 7)
                                    else:
                                        setv(pi, pj, 7)
                        elif open_dir == 3:  # open right
                            # fill interior left 3 vertical
                            setv(i - 1, j - 1, 7)
                            setv(i, j - 1, 7)
                            setv(i + 1, j - 1, 7)
                            if is_internal:
                                # fill open right 3 vertical, with condition
                                for off in [-1, 0, 1]:
                                    pi = i + off
                                    pj = j + 1
                                    if get(pi, pj) == 0:
                                        p_num = sum(1 for ddi, ddj in directions if get(pi + ddi, pj + ddj) == 1)
                                        if p_num < 2:
                                            setv(pi, pj, 7)
                                    else:
                                        setv(pi, pj, 7)
                elif num_1 == 2:
                    up1 = get(i - 1, j) == 1
                    down1 = get(i + 1, j) == 1
                    left1 = get(i, j - 1) == 1
                    right1 = get(i, j + 1) == 1
                    if not up1 and not right1 and left1 and down1:
                        setv(i, j - 1, 7)
                        setv(i + 1, j - 1, 7)
                        setv(i + 1, j, 7)
                    if not up1 and not left1 and right1 and down1:
                        setv(i, j + 1, 7)
                        setv(i + 1, j + 1, 7)
                        setv(i + 1, j, 7)
                    if not down1 and not right1 and up1 and left1:
                        setv(i, j - 1, 7)
                        setv(i - 1, j - 1, 7)
                        setv(i - 1, j, 7)
                    if not down1 and not left1 and up1 and right1:
                        setv(i, j + 1, 7)
                        setv(i - 1, j + 1, 7)
                        setv(i - 1, j, 7)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = remove_isolated(g)
    out = handle_patterns(out)
    return out
```