```python
from typing import List
import collections

dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
opposites = [(0, 1), (2, 3)]

def count_one_neighbors(g: List[List[int]], r: int, c: int) -> int:
    rows, cols = len(g), len(g[0])
    count = 0
    for dr, dc in dirs4:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
            count += 1
    return count

def remove_isolated(g: List[List[int]]) -> List[List[int]]:
    rows, cols = len(g), len(g[0])
    result = [row[:] for row in g]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                num_adj = 0
                for di, dj in dirs4:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == 1:
                        num_adj += 1
                if num_adj == 0:
                    result[i][j] = 0
    return result

def handle_enclosed(g: List[List[int]], result: List[List[int]]) -> List[List[int]]:
    rows, cols = len(g), len(g[0])
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 0:
                num1 = 0
                for dr, dc in dirs4:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
                        num1 += 1
                if num1 == 4:
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and result[nr][nc] == 1:
                                result[nr][nc] = 7
    return result

def handle_double_horizontal_bays(g: List[List[int]], result: List[List[int]]) -> List[List[int]]:
    rows, cols = len(g), len(g[0])
    for r in range(rows - 1):
        c = 1
        while c < cols - 2:
            if g[r][c] == 0 and g[r][c + 1] == 0:
                num_left = count_one_neighbors(g, r, c)
                num_right = count_one_neighbors(g, r, c + 1)
                if num_left == 3 and num_right == 3:
                    # Mark sides in bay row
                    if result[r][c - 1] == 1:
                        result[r][c - 1] = 7
                    if result[r][c + 2] == 1:
                        result[r][c + 2] = 7
                    # Mark sides in down row
                    if result[r + 1][c - 1] == 1:
                        result[r + 1][c - 1] = 7
                    if result[r + 1][c + 2] == 1:
                        result[r + 1][c + 2] = 7
                    # Set centers in down row
                    center_val = 0 if r + 1 == rows - 1 else 7
                    if result[r + 1][c] == 1:
                        result[r + 1][c] = center_val
                    if result[r + 1][c + 1] == 1:
                        result[r + 1][c + 1] = center_val
                    c += 2  # Skip next to avoid overlap
                else:
                    c += 1
            else:
                c += 1
    return result

def handle_edge_straights(g: List[List[int]], result: List[List[int]]) -> List[List[int]]:
    rows, cols = len(g), len(g[0])
    # Horizontal straights on top/bottom edges
    for r in [0, rows - 1]:
        for c in range(1, cols - 1):
            if g[r][c] == 0:
                left_one = 0 <= c - 1 < cols and g[r][c - 1] == 1
                right_one = 0 <= c + 1 < cols and g[r][c + 1] == 1
                up_one = (r > 0 and g[r - 1][c] == 1) or (r == 0 and False)
                down_one = (r < rows - 1 and g[r + 1][c] == 1) or (r == rows - 1 and False)
                if left_one and right_one and not up_one and not down_one:
                    if result[r][c - 1] == 1:
                        result[r][c - 1] = 7
                    if result[r][c + 1] == 1:
                        result[r][c + 1] = 7
    # Vertical straights on left/right edges
    for c in [0, cols - 1]:
        for r in range(1, rows - 1):
            if g[r][c] == 0:
                up_one = g[r - 1][c] == 1
                down_one = g[r + 1][c] == 1
                left_one = (c > 0 and g[r][c - 1] == 1) or (c == 0 and False)
                right_one = (c < cols - 1 and g[r][c + 1] == 1) or (c == cols - 1 and False)
                if up_one and down_one and not left_one and not right_one:
                    if result[r - 1][c] == 1:
                        result[r - 1][c] = 7
                    if result[r + 1][c] == 1:
                        result[r + 1][c] = 7
    return result

def handle_L_bays(g: List[List[int]], result: List[List[int]]) -> List[List[int]]:
    rows, cols = len(g), len(g[0])
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
                    # L shape, mark two orthogonal and diagonal
                    for i in one_dirs:
                        nr = r + dirs4[i][0]
                        nc = c + dirs4[i][1]
                        if result[nr][nc] == 1:
                            result[nr][nc] = 7
                    # diagonal
                    dr_diag = dirs4[i1][0] + dirs4[i2][0]
                    dc_diag = dirs4[i1][1] + dirs4[i2][1]
                    nr = r + dr_diag
                    nc = c + dc_diag
                    if 0 <= nr < rows and 0 <= nc < cols and result[nr][nc] == 1:
                        result[nr][nc] = 7
    return result

def handle_single_bays(g: List[List[int]], result: List[List[int]]) -> List[List[int]]:
    rows, cols = len(g), len(g[0])
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
                    dr, dc = dirs4[open_i]
                    nr_open = r + dr
                    nc_open = c + dc
                    skip = False
                    if 0 <= nr_open < rows and 0 <= nc_open < cols and g[nr_open][nc_open] == 0:
                        num_open = count_one_neighbors(g, nr_open, nc_open)
                        if num_open == 3:
                            skip = True
                        elif num_open == 2:
                            open_one_dirs = [i for i in range(4) if 0 <= nr_open + dirs4[i][0] < rows and 0 <= nc_open + dirs4[i][1] < cols and g[nr_open + dirs4[i][0]][nc_open + dirs4[i][1]] == 1]
                            oi1, oi2 = sorted(open_one_dirs)
                            if open_i in [2, 3] and (oi1, oi2) == (0, 1):
                                skip = True
                            elif open_i in [0, 1] and (oi1, oi2) == (2, 3):
                                skip = True
                    if skip:
                        continue
                    # set 3 orthogonal closed
                    for i in one_dirs:
                        nnr = r + dirs4[i][0]
                        nnc = c + dirs4[i][1]
                        if result[nnr][nnc] == 1:
                            result[nnr][nnc] = 7
                    # set 2 closed diagonals
                    if open_i == 0:  # open up
                        dlr = r + 1
                        dlc1 = c - 1
                        if 0 <= dlr < rows and 0 <= dlc1 < cols and result[dlr][dlc1] == 1:
                            result[dlr][dlc1] = 7
                        dlc2 = c + 1
                        if 0 <= dlr < rows and 0 <= dlc2 < cols and result[dlr][dlc2] == 1:
                            result[dlr][dlc2] = 7
                    elif open_i == 1:  # open down
                        ulr = r - 1
                        ulc1 = c - 1
                        if 0 <= ulr < rows and 0 <= ulc1 < cols and result[ulr][ulc1] == 1:
                            result[ulr][ulc1] = 7
                        ulc2 = c + 1
                        if 0 <= ulr < rows and 0 <= ulc2 < cols and result[ulr][ulc2] == 1:
                            result[ulr][ulc2] = 7
                    elif open_i == 2:  # open left
                        ur_r = r - 1
                        ur_c = c + 1
                        if 0 <= ur_r < rows and 0 <= ur_c < cols and result[ur_r][ur_c] == 1:
                            result[ur_r][ur_c] = 7
                        dr_r = r + 1
                        dr_c = c + 1
                        if 0 <= dr_r < rows and 0 <= dr_c < cols and result[dr_r][dr_c] == 1:
                            result[dr_r][dr_c] = 7
                    elif open_i == 3:  # open right
                        ul_r = r - 1
                        ul_c = c - 1
                        if 0 <= ul_r < rows and 0 <= ul_c < cols and result[ul_r][ul_c] == 1:
                            result[ul_r][ul_c] = 7
                        dl_r = r + 1
                        dl_c = c - 1
                        if 0 <= dl_r < rows and 0 <= dl_c < cols and result[dl_r][dl_c] == 1:
                            result[dl_r][dl_c] = 7
                    # additional fill for open direction if open cell is 0
                    if 0 <= nr_open < rows and 0 <= nc_open < cols and g[nr_open][nc_open] == 0:
                        if open_i == 0 or open_i == 1:  # vertical open
                            fill_r = nr_open
                            for ddc in [-1, 0, 1]:
                                nnc2 = nc_open + ddc
                                if 0 <= nnc2 < cols:
                                    result[fill_r][nnc2] = 7
                        else:  # horizontal open
                            fill_c = nc_open
                            for drr in [-1, 0, 1]:
                                nrr = r + drr
                                if 0 <= nrr < rows:
                                    result[nrr][fill_c] = 7
    return result

def handle_double_vertical_bays(g: List[List[int]], result: List[List[int]]) -> List[List[int]]:
    rows, cols = len(g), len(g[0])
    # Open right
    for r in range(rows - 2):
        for c in range(cols - 1):
            if g[r][c] == 0 and g[r + 1][c] == 0:
                num_upper = count_one_neighbors(g, r, c)
                num_lower = count_one_neighbors(g, r + 1, c)
                if num_upper == 3 and num_lower == 3:
                    # Check configuration for open right
                    if (0 <= r - 1 < rows and g[r - 1][c] == 1) and (0 <= r + 2 < rows and g[r + 2][c] == 1) and \
                       g[r][c - 1] == 1 and g[r + 1][c - 1] == 1 and \
                       g[r][c + 1] == 0 and g[r + 1][c + 1] == 0:
                        # Mark left sides
                        if result[r][c - 1] == 1:
                            result[r][c - 1] = 7
                        if result[r + 1][c - 1] == 1:
                            result[r + 1][c - 1] = 7
                        # Mark top and bottom sides
                        if 0 <= r - 1 < rows and result[r - 1][c] == 1:
                            result[r - 1][c] = 7
                        if 0 <= r + 2 < rows and result[r + 2][c] == 1:
                            result[r + 2][c] = 7
                        # Set centers in right col
                        center_val = 0 if c + 1 == cols - 1 else 7
                        if result[r][c + 1] == 1:
                            result[r][c + 1] = center_val
                        if result[r + 1][c + 1] == 1:
                            result[r + 1][c + 1] = center_val
                        r += 1  # Skip next r
    # Open left (symmetric)
    for r in range(rows - 2):
        for c in range(1, cols):
            if g[r][c] == 0 and g[r + 1][c] == 0:
                num_upper = count_one_neighbors(g, r, c)
                num_lower = count_one_neighbors(g, r + 1, c)
                if num_upper == 3 and num_lower == 3:
                    # Check configuration for open left
                    if (0 <= r - 1 < rows and g[r - 1][c] == 1) and (0 <= r + 2 < rows and g[r + 2][c] == 1) and \
                       g[r][c + 1] == 1 and g[r + 1][c + 1] == 1 and \
                       g[r][c - 1] == 0 and g[r + 1][c - 1] == 0:
                        # Mark right sides
                        if result[r][c + 1] == 1:
                            result[r][c + 1] = 7
                        if result[r + 1][c + 1] == 1:
                            result[r + 1][c + 1] = 7
                        # Mark top and bottom sides
                        if 0 <= r - 1 < rows and result[r - 1][c] == 1:
                            result[r - 1][c] = 7
                        if 0 <= r + 2 < rows and result[r + 2][c] == 1:
                            result[r + 2][c] = 7
                        # Set centers in left col
                        center_val = 0 if c - 1 == 0 else 7
                        if result[r][c - 1] == 1:
                            result[r][c - 1] = center_val
                        if result[r + 1][c - 1] == 1:
                            result[r + 1][c - 1] = center_val
                        r += 1  # Skip next r
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    result = remove_isolated(g)
    result = handle_enclosed(g, result)
    result = handle_double_horizontal_bays(g, result)
    result = handle_double_vertical_bays(g, result)
    result = handle_edge_straights(g, result)
    result = handle_L_bays(g, result)
    result = handle_single_bays(g, result)
    return result
```