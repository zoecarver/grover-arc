```python
from typing import List

def get_num_one_neighbors(g: List[List[int]], r: int, c: int) -> int:
    rows = len(g)
    cols = len(g[0])
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    count = 0
    for dr, dc in dirs4:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
            count += 1
    return count

def remove_isolated(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                num_adj = sum(1 for di, dj in directions if 0 <= i + di < rows and 0 <= j + dj < cols and g[i + di][j + dj] == 1)
                if num_adj == 0:
                    out[i][j] = 0
    return out

def remove_remaining_isolated(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                num_adj = sum(1 for di, dj in directions if 0 <= i + di < rows and 0 <= j + dj < cols and g[i + di][j + dj] == 1)
                if num_adj == 0:
                    out[i][j] = 0
    return out

def handle_enclosed_holes(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dirs8 = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    diag_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0:
                num1 = sum(1 for dr, dc in dirs4 if 0 <= r + dr < rows and 0 <= c + dc < cols and g[r + dr][c + dc] == 1)
                if num1 == 4:
                    for dr, dc in dirs8:
                        nr = r + dr
                        nc = c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and out[nr][nc] == 1:
                            out[nr][nc] = 7
                    all_diag_filled = True
                    for ddr, ddc in diag_dirs:
                        nr = r + ddr
                        nc = c + ddc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] != 1:
                            all_diag_filled = False
                            break
                    if all_diag_filled and out[r][c] == 0:
                        out[r][c] = 7
    return out

def handle_double_horizontal_bays(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    c = 1
    while c < cols - 2:
        if g[c // wait no, for r in range(rows-1), for c in range(1, cols-1? 
    for r in range(rows - 1):
        c = 1
        while c < cols - 2:
            if g[r][c] == 0 and g[r][c + 1] == 0:
                num_left = sum(1 for dr, dc in dirs4 if 0 <= r + dr < rows and 0 <= c + dc < cols and g[r + dr][c + dc] == 1)
                num_right = sum(1 for dr, dc in dirs4 if 0 <= r + dr < rows and 0 <= (c + 1) + dc < cols and g[r + dr][(c + 1) + dc] == 1)
                if num_left == 3 and num_right == 3:
                    if out[r][c - 1] == 1:
                        out[r][c - 1] = 7
                    if out[r][c + 2] == 1:
                        out[r][c + 2] = 7
                    if out[r + 1][c - 1] == 1:
                        out[r + 1][c - 1] = 7
                    if out[r + 1][c + 2] == 1:
                        out[r + 1][c + 2] = 7
                    if out[r + 1][c] == 1:
                        out[r + 1][c] = 7
                    if out[r + 1][c + 1] == 1:
                        out[r + 1][c + 1] = 7
                    c += 1
            c += 1
    return out

def handle_double_vertical_bays(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for c in range(cols):
        r = 0
        while r < rows - 1:
            if g[r][c] == 0 and g[r + 1][c] == 0:
                num_upper = get_num_one_neighbors(g, r, c)
                num_lower = get_num_one_neighbors(g, r + 1, c)
                if num_upper == 3 and num_lower == 3:
                    open_dir_upper = None
                    for i in range(4):
                        dr, dc = dirs4[i]
                        nr = r + dr
                        nc = c + dc
                        if not (0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1):
                            open_dir_upper = i
                            break
                    open_dir_lower = None
                    for i in range(4):
                        dr, dc = dirs4[i]
                        nr = (r + 1) + dr
                        nc = c + dc
                        if not (0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1):
                            open_dir_lower = i
                            break
                    if open_dir_upper == open_dir_lower and open_dir_upper in [2, 3]:
                        side_col = c - 1 if open_dir_upper == 2 else c + 1
                        if r - 1 >= 0 and out[r - 1][c] == 1:
                            out[r - 1][c] = 7
                        if r + 2 < rows and out[r + 2][c] == 1:
                            out[r + 2][c] = 7
                        if 0 <= side_col < cols:
                            if r - 1 >= 0 and out[r - 1][side_col] == 1:
                                out[r - 1][side_col] = 7
                            if r + 2 < rows and out[r + 2][side_col] == 1:
                                out[r + 2][side_col] = 7
                            if out[r][side_col] == 1:
                                out[r][side_col] = 7
                            if out[r + 1][side_col] == 1:
                                out[r + 1][side_col] = 7
                r += 1
                if num_upper == 3 and num_lower == 3 and open_dir_upper == open_dir_lower and open_dir_upper in [2, 3]:
                    r += 1
                else:
                    r += 1
    return out

def handle_L_bays(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
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
                        continue
                    for i in one_dirs:
                        nr = r + dirs4[i][0]
                        nc = c + dirs4[i][1]
                        if out[nr][nc] == 1:
                            out[nr][nc] = 7
                    dr_diag = dirs4[i1][0] + dirs4[i2][0]
                    dc_diag = dirs4[i1][1] + dirs4[i2][1]
                    nr = r + dr_diag
                    nc = c + dc_diag
                    if 0 <= nr < rows and 0 <= nc < cols and out[nr][nc] == 1:
                        out[nr][nc] = 7
    return out

def handle_single_bays(g: List[List[int]], out: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0:
                one_dirs = [i for i in range(4) if 0 <= r + dirs4[i][0] < rows and 0 <= c + dirs4[i][1] < cols and g[r + dirs4[i][0]][c + dirs4[i][1]] == 1]
                if len(one_dirs) == 3:
                    open_i = next(i for i in range(4) if i not in one_dirs)
                    dr_open, dc_open = dirs4[open_i]
                    nr_open = r + dr_open
                    nc_open = c + dc_open
                    skip = False
                    if 0 <= nr_open < rows and 0 <= nc_open < cols and g[nr_open][nc_open] == 0:
                        num_open = get_num_one_neighbors(g, nr_open, nc_open)
                        if num_open == 3:
                            skip = True
                    if skip:
                        continue
                    for i in one_dirs:
                        nnr = r + dirs4[i][0]
                        nnc = c + dirs4[i][1]
                        if out[nnr][nnc] == 1:
                            out[nnr][nnc] = 7
                    if open_i == 0:  # open up
                        dlr = r + 1
                        dlc1 = c - 1
                        if 0 <= dlc1 < cols and 0 <= dlr < rows:
                            val = out[dlr][dlc1]
                            n1 = get_num_one_neighbors(g, dlr, dlc1)
                            if val == 1 or (val == 0 and n1 == 0):
                                out[dlr][dlc1] = 7
                        dlc2 = c + 1
                        if 0 <= dlc2 < cols and 0 <= dlr < rows:
                            val = out[dlr][dlc2]
                            n1 = get_num_one_neighbors(g, dlr, dlc2)
                            if val == 1 or (val == 0 and n1 == 0):
                                out[dlr][dlc2] = 7
                    elif open_i == 1:  # open down
                        ulr = r - 1
                        ulc1 = c - 1
                        if 0 <= ulc1 < cols and 0 <= ulr < rows:
                            val = out[ulr][ulc1]
                            n1 = get_num_one_neighbors(g, ulr, ulc1)
                            if val == 1 or (val == 0 and n1 == 0):
                                out[ulr][ulc1] = 7
                        ulc2 = c + 1
                        if 0 <= ulc2 < cols and 0 <= ulr < rows:
                            val = out[ulr][ulc2]
                            n1 = get_num_one_neighbors(g, ulr, ulc2)
                            if val == 1 or (val == 0 and n1 == 0):
                                out[ulr][ulc2] = 7
                    elif open_i == 2:  # open left
                        ur_r = r - 1
                        ur_c = c + 1
                        if 0 <= ur_r < rows and 0 <= ur_c < cols:
                            val = out[ur_r][ur_c]
                            n1 = get_num_one_neighbors(g, ur_r, ur_c)
                            if val == 1 or (val == 0 and n1 == 0):
                                out[ur_r][ur_c] = 7
                        dr_r = r + 1
                        dr_c = c + 1
                        if 0 <= dr_r < rows and 0 <= dr_c < cols:
                            val = out[dr_r][dr_c]
                            n1 = get_num_one_neighbors(g, dr_r, dr_c)
                            if val == 1 or (val == 0 and n1 == 0):
                                out[dr_r][dr_c] = 7
                    elif open_i == 3:  # open right
                        ul_r = r - 1
                        ul_c = c - 1
                        if 0 <= ul_r < rows and 0 <= ul_c < cols:
                            val = out[ul_r][ul_c]
                            n1 = get_num_one_neighbors(g, ul_r, ul_c)
                            if val == 1 or (val == 0 and n1 == 0):
                                out[ul_r][ul_c] = 7
                        dl_r = r + 1
                        dl_c = c - 1
                        if 0 <= dl_r < rows and 0 <= dl_c < cols:
                            val = out[dl_r][dl_c]
                            n1 = get_num_one_neighbors(g, dl_r, dl_c)
                            if val == 1 or (val == 0 and n1 == 0):
                                out[dl_r][dl_c] = 7
                    # fill open center if condition
                    if 0 <= nr_open < rows and 0 <= nc_open < cols and g[nr_open][nc_open] == 0 and out[nr_open][nc_open] == 0:
                        fill_center = True
                        perp_dirs = [2, 3] if open_i in [0, 1] else [0, 1]
                        for p_i in perp_dirs:
                            p_dr, p_dc = dirs4[p_i]
                            p_nr = nr_open + p_dr
                            p_nc = nc_open + p_dc
                            if 0 <= p_nr < rows and 0 <= p_nc < cols and g[p_nr][p_nc] == 0:
                                p_num = get_num_one_neighbors(g, p_nr, p_nc)
                                if p_num > 0:
                                    fill_center = False
                                    break
                        if fill_center:
                            out[nr_open][nc_open] = 7
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = remove_isolated(g)
    out = handle_enclosed_holes(g, out)
    out = handle_double_horizontal_bays(g, out)
    out = handle_double_vertical_bays(g, out)
    out = handle_L_bays(g, out)
    out = handle_single_bays(g, out)
    out = remove_remaining_isolated(out)
    return out
```