```python
from typing import List, Tuple, Dict
import collections

def get_4_neighbors(cleaned: List[List[int]], i: int, j: int, rows: int, cols: int) -> Tuple[int, Dict[Tuple[int, int], Tuple[int, int, int]]]:
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neigh_types: Dict[Tuple[int, int], Tuple[int, int, int]] = {}
    count1 = 0
    for di, dj in dirs:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            val = cleaned[ni][nj]
            neigh_types[(di, dj)] = (ni, nj, val)
            if val == 1:
                count1 += 1
        else:
            neigh_types[(di, dj)] = None
    return count1, neigh_types

def set_8_adj_1s_to_7(cleaned: List[List[int]], new_g: List[List[int]], i: int, j: int, rows: int, cols: int):
    for ddi in [-1, 0, 1]:
        for ddj in [-1, 0, 1]:
            if ddi == 0 and ddj == 0:
                continue
            ni = i + ddi
            nj = j + ddj
            if 0 <= ni < rows and 0 <= nj < cols and cleaned[ni][nj] == 1:
                new_g[ni][nj] = 7

def handle_enclosed_hole(cleaned: List[List[int]], new_g: List[List[int]], i: int, j: int, rows: int, cols: int):
    set_8_adj_1s_to_7(cleaned, new_g, i, j, rows, cols)

def handle_bridge(cleaned: List[List[int]], new_g: List[List[int]], i: int, j: int, open_dj: int, rows: int, cols: int):
    if open_dj == 1:  # open right
        end_j = j + 1
        while end_j < cols and cleaned[i][end_j] == 0:
            end_j += 1
        left_c = j - 1
        gap_start = j
        gap_end = end_j - 1
        right_c = end_j if end_j < cols and cleaned[i][end_j] == 1 else end_j
        fill_start = left_c
        fill_end = right_c + 1 if end_j < cols and cleaned[i][end_j] == 1 else end_j
        # current row
        for c in range(max(0, fill_start), min(cols, fill_end)):
            new_g[i][c] = 7
        # above
        if i > 0:
            for c in range(max(0, fill_start), min(cols, fill_end)):
                if cleaned[i - 1][c] == 1:
                    new_g[i - 1][c] = 7
        # below
        if i < rows - 1:
            if 0 <= left_c < cols and cleaned[i + 1][left_c] == 1:
                new_g[i + 1][left_c] = 7
            if 0 <= right_c < cols and cleaned[i + 1][right_c] == 1:
                new_g[i + 1][right_c] = 7
            for c in range(gap_start, gap_end + 1):
                if 0 <= c < cols:
                    new_g[i + 1][c] = 0
    elif open_dj == -1:  # open left
        start_j = j - 1
        while start_j >= 0 and cleaned[i][start_j] == 0:
            start_j -= 1
        start_j += 1
        right_c = j + 1
        gap_start = start_j
        gap_end = j
        left_c = start_j - 1
        if left_c >= 0 and cleaned[i][left_c] == 1:
            fill_start = left_c
        else:
            fill_start = start_j
        fill_end = right_c + 1 if right_c < cols and cleaned[i][right_c] == 1 else right_c
        # current row
        for c in range(max(0, fill_start), min(cols, fill_end)):
            new_g[i][c] = 7
        # above
        if i > 0:
            for c in range(max(0, fill_start), min(cols, fill_end)):
                if cleaned[i - 1][c] == 1:
                    new_g[i - 1][c] = 7
        # below
        if i < rows - 1:
            if 0 <= left_c < cols and cleaned[i + 1][left_c] == 1:
                new_g[i + 1][left_c] = 7
            if 0 <= right_c < cols and cleaned[i + 1][right_c] == 1:
                new_g[i + 1][right_c] = 7
            for c in range(gap_start, gap_end + 1):
                if 0 <= c < cols:
                    new_g[i + 1][c] = 0

def handle_dent_vertical(cleaned: List[List[int]], new_g: List[List[int]], i: int, j: int, open_di: int, rows: int, cols: int):
    set_8_adj_1s_to_7(cleaned, new_g, i, j, rows, cols)
    dir_i = i + open_di
    if 0 <= dir_i < rows:
        for dc in [-1, 0, 1]:
            nc = j + dc
            if 0 <= nc < cols and cleaned[dir_i][nc] == 0:
                new_g[dir_i][nc] = 7

def remove_isolated_1s(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    new_g = [row[:] for row in g]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == 1:
                has_neigh = False
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and g[ni][nj] == 1:
                        has_neigh = True
                        break
                if not has_neigh:
                    new_g[i][j] = 0
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    cleaned = remove_isolated_1s(g)
    new_g = [row[:] for row in cleaned]
    for i in range(rows):
        for j in range(cols):
            if cleaned[i][j] != 0:
                continue
            count1, neigh_types = get_4_neighbors(cleaned, i, j, rows, cols)
            if count1 == 4:
                handle_enclosed_hole(cleaned, new_g, i, j, rows, cols)
            elif count1 == 3:
                # find open dir
                open_dir = None
                for (di, dj), info in neigh_types.items():
                    if info is None or info[2] != 1:
                        open_dir = (di, dj, info)
                        break
                if open_dir is None:
                    continue
                open_di, open_dj, open_info = open_dir
                is_horizontal_open = abs(open_dj) == 1
                up_1 = neigh_types.get((-1, 0), None) is not None and neigh_types[(-1, 0)][2] == 1
                down_1 = neigh_types.get((1, 0), None) is not None and neigh_types[(1, 0)][2] == 1
                if is_horizontal_open and up_1 and down_1:
                    # bridge
                    if open_dj == 1 and j > 0 and cleaned[i][j - 1] == 1:
                        handle_bridge(cleaned, new_g, i, j, open_dj, rows, cols)
                    elif open_dj == -1 and j < cols - 1 and cleaned[i][j + 1] == 1:
                        handle_bridge(cleaned, new_g, i, j, open_dj, rows, cols)
                    else:
                        set_8_adj_1s_to_7(cleaned, new_g, i, j, rows, cols)
                elif open_di == 1 and open_info is not None and open_info[2] == 0:
                    handle_dent_vertical(cleaned, new_g, i, j, open_di, rows, cols)
                elif open_di == -1 and open_info is not None and open_info[2] == 0:
                    handle_dent_vertical(cleaned, new_g, i, j, open_di, rows, cols)
                else:
                    set_8_adj_1s_to_7(cleaned, new_g, i, j, rows, cols)
            elif count1 == 2 and (i == 0 or i == rows - 1 or j == 0 or j == cols - 1):
                set_8_adj_1s_to_7(cleaned, new_g, i, j, rows, cols)
    return new_g
```