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

def clean_grid(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if new_g[r][c] == 1 and not (r == 0 or r == rows - 1 or c == 0 or c == cols - 1):
                one_dirs = []
                for i, (dr, dc) in enumerate(dirs4):
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and new_g[nr][nc] == 1:
                        one_dirs.append(i)
                num1 = len(one_dirs)
                if num1 <= 1 or (num1 == 2 and sorted(one_dirs) not in [[0, 1], [2, 3]]):
                    new_g[r][c] = 0
    return new_g

def handle_bays_and_holes(temp: List[List[int]]) -> List[List[int]]:
    rows = len(temp)
    cols = len(temp[0])
    result = [row[:] for row in temp]
    dirs4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    dirs8 = [(dr, dc) for dr in range(-1, 2) for dc in range(-1, 2) if not (dr == 0 and dc == 0)]
    for r in range(rows):
        for c in range(cols):
            if temp[r][c] == 0:
                num1 = get_num_one_neighbors(temp, r, c)
                if num1 >= 3:
                    # Mark all 8 neighbors if 1 to 7
                    for dr, dc in dirs8:
                        nr = r + dr
                        nc = c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and result[nr][nc] == 1:
                            result[nr][nc] = 7
                    if num1 == 3:
                        # Find open direction
                        open_dirs = []
                        for i, (dr, dc) in enumerate(dirs4):
                            nr = r + dr
                            nc = c + dc
                            if not (0 <= nr < rows and 0 <= nc < cols and temp[nr][nc] == 1):
                                open_dirs.append(i)
                        if len(open_dirs) == 1:
                            open_i = open_dirs[0]
                            open_dr, open_dc = dirs4[open_i]
                            open_nr = r + open_dr
                            open_nc = c + open_dc
                            if 0 <= open_nr < rows and 0 <= open_nc < cols and temp[open_nr][open_nc] == 0:
                                open_num1 = get_num_one_neighbors(temp, open_nr, open_nc)
                                if open_num1 < 2:
                                    # Fill the 3 in open direction
                                    if open_i == 0:  # up
                                        for ddc in [-1, 0, 1]:
                                            nnr = r - 1
                                            nnc = c + ddc
                                            if 0 <= nnr < rows and 0 <= nnc < cols:
                                                result[nnr][nnc] = 7
                                    elif open_i == 1:  # down
                                        for ddc in [-1, 0, 1]:
                                            nnr = r + 1
                                            nnc = c + ddc
                                            if 0 <= nnr < rows and 0 <= nnc < cols:
                                                result[nnr][nnc] = 7
                                    elif open_i == 2:  # left
                                        for ddr in [-1, 0, 1]:
                                            nnr = r + ddr
                                            nnc = c - 1
                                            if 0 <= nnr < rows and 0 <= nnc < cols:
                                                result[nnr][nnc] = 7
                                    elif open_i == 3:  # right
                                        for ddr in [-1, 0, 1]:
                                            nnr = r + ddr
                                            nnc = c + 1
                                            if 0 <= nnr < rows and 0 <= nnc < cols:
                                                result[nnr][nnc] = 7
                                if open_num1 == 2:
                                    # Handle double-like, set center to 7 and extra far side
                                    result[r][c] = 7
                                    if open_i == 0 or open_i == 1:  # vertical
                                        far_dr = open_dr * 2
                                        far_r = r + far_dr
                                        if 0 <= far_r < rows:
                                            for sdc in [-1, 0, 1]:
                                                nnc = c + sdc
                                                if 0 <= nnc < cols and result[far_r][nnc] == 1:
                                                    result[far_r][nnc] = 7
                                    else:  # horizontal
                                        far_dc = open_dc * 2
                                        far_c = c + far_dc
                                        if 0 <= far_c < cols:
                                            for sdr in [-1, 0, 1]:
                                                nnr = r + sdr
                                                if 0 <= nnr < rows and result[nnr][far_c] == 1:
                                                    result[nnr][far_c] = 7
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    temp = clean_grid(g)
    return handle_bays_and_holes(temp)
```