```python
from typing import List
import collections

def remove_isolated(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if out[i][j] == 1:
                num_adj = sum(1 for di, dj in directions if 0 <= i + di < rows and 0 <= j + dj < cols and out[i + di][j + dj] == 1)
                if num_adj == 0:
                    out[i][j] = 0
    return out

def handle_enclosed_holes(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0:
                num1 = 0
                for dr, dc in dirs4:
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
                        num1 += 1
                if num1 == 4:
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if dr == 0 and dc == 0:
                                continue
                            nr = r + dr
                            nc = c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and new_g[nr][nc] == 1:
                                new_g[nr][nc] = 7
    return new_g

def handle_double_horizontal_bays(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows - 1):
        for c in range(1, cols - 2):
            if g[r][c] == 0 and g[r][c + 1] == 0:
                # check left 0 has 3 ones
                num_left = sum(1 for dr, dc in dirs4 if 0 <= r + dr < rows and 0 <= c + dc < cols and g[r + dr][c + dc] == 1)
                # check right 0 has 3 ones
                num_right = sum(1 for dr, dc in dirs4 if 0 <= r + dr < rows and 0 <= (c + 1) + dc < cols and g[r + dr][(c + 1) + dc] == 1)
                if num_left == 3 and num_right == 3:
                    # set sides in bay row
                    new_g[r][c - 1] = 7
                    new_g[r][c + 2] = 7
                    # set sides in down row
                    new_g[r + 1][c - 1] = 7
                    new_g[r + 1][c + 2] = 7
                    # set centers in down row to 0 if 1
                    if new_g[r + 1][c] == 1:
                        new_g[r + 1][c] = 0
                    if new_g[r + 1][c + 1] == 1:
                        new_g[r + 1][c + 1] = 0
                    # skip next c to avoid double
                    c += 1
    return new_g

def handle_L_bays(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    opposites = [(0, 1), (2, 3)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0:
                one_dirs = []
                for i, (dr, dc) in enumerate(dirs4):
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
                        one_dirs.append(i)
                if len(one_dirs) == 2:
                    i1, i2 = sorted(one_dirs)
                    if (i1, i2) in opposites:
                        continue  # skip opposite
                    # L shape, set two orthogonal and diagonal
                    for i in one_dirs:
                        nr = r + dirs4[i][0]
                        nc = c + dirs4[i][1]
                        if new_g[nr][nc] == 1:
                            new_g[nr][nc] = 7
                    # diagonal
                    dr_diag = dirs4[i1][0] + dirs4[i2][0]
                    dc_diag = dirs4[i1][1] + dirs4[i2][1]
                    nr = r + dr_diag
                    nc = c + dc_diag
                    if 0 <= nr < rows and 0 <= nc < cols and new_g[nr][nc] == 1:
                        new_g[nr][nc] = 7
    return new_g

def handle_single_bays(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0:
                one_dirs = []
                for i, (dr, dc) in enumerate(dirs4):
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
                        one_dirs.append(i)
                if len(one_dirs) == 3:
                    open_i = next(i for i in range(4) if i not in one_dirs)
                    # check skip condition
                    dr, dc = dirs4[open_i]
                    nr_open = r + dr
                    nc_open = c + dc
                    skip = False
                    if 0 <= nr_open < rows and 0 <= nc_open < cols and g[nr_open][nc_open] == 0:
                        num_open = sum(1 for ddr, ddc in dirs4 if 0 <= nr_open + ddr < rows and 0 <= nc_open + ddc < cols and g[nr_open + ddr][nc_open + ddc] == 1)
                        if num_open == 3:
                            skip = True
                    if skip:
                        continue
                    # set 3 orthogonal closed
                    for i in one_dirs:
                        nnr = r + dirs4[i][0]
                        nnc = c + dirs4[i][1]
                        new_g[nnr][nnc] = 7
                    # set 2 closed diagonals
                    if open_i == 0:  # open up
                        # closed diagonals: down left, down right
                        dlr = r + 1
                        dlc = c - 1
                        if 0 <= dlr < rows and 0 <= dlc < cols and new_g[dlr][dlc] == 1:
                            new_g[dlr][dlc] = 7
                        drc = c + 1
                        if 0 <= dlr < rows and 0 <= drc < cols and new_g[dlr][drc] == 1:
                            new_g[dlr][drc] = 7
                    elif open_i == 1:  # open down
                        # closed diagonals: up left, up right
                        ulr = r - 1
                        ulc = c - 1
                        if 0 <= ulr < rows and 0 <= ulc < cols and new_g[ulr][ulc] == 1:
                            new_g[ulr][ulc] = 7
                        urc = c + 1
                        if 0 <= ulr < rows and 0 <= urc < cols and new_g[ulr][urc] == 1:
                            new_g[ulr][urc] = 7
                    elif open_i == 2:  # open left
                        # closed diagonals: up right, down right
                        ur_r = r - 1
                        ur_c = c + 1
                        if 0 <= ur_r < rows and 0 <= ur_c < cols and new_g[ur_r][ur_c] == 1:
                            new_g[ur_r][ur_c] = 7
                        dr_r = r + 1
                        dr_c = c + 1
                        if 0 <= dr_r < rows and 0 <= dr_c < cols and new_g[dr_r][dr_c] == 1:
                            new_g[dr_r][dr_c] = 7
                    elif open_i == 3:  # open right
                        # closed diagonals: up left, down left
                        ul_r = r - 1
                        ul_c = c - 1
                        if 0 <= ul_r < rows and 0 <= ul_c < cols and new_g[ul_r][ul_c] == 1:
                            new_g[ul_r][ul_c] = 7
                        dl_r = r + 1
                        dl_c = c - 1
                        if 0 <= dl_r < rows and 0 <= dl_c < cols and new_g[dl_r][dl_c] == 1:
                            new_g[dl_r][dl_c] = 7
                    # additional open fill for vertical opens if applicable
                    if open_i == 1 and r + 1 < rows and g[r + 1][c] == 0:  # open down, open cell 0
                        for dc2 in [-1, 0, 1]:
                            nc2 = c + dc2
                            if 0 <= nc2 < cols:
                                new_g[r + 1][nc2] = 7
                    elif open_i == 0 and r - 1 >= 0 and g[r - 1][c] == 0:  # open up, open cell 0
                        for dc2 in [-1, 0, 1]:
                            nc2 = c + dc2
                            if 0 <= nc2 < cols:
                                new_g[r - 1][nc2] = 7
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    temp = remove_isolated(g)
    temp = handle_enclosed_holes(temp)
    temp = handle_double_horizontal_bays(temp)
    temp = handle_L_bays(temp)
    temp = handle_single_bays(temp)
    return temp
```