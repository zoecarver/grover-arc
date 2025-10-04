```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    # Find start_row: first row with non-8
    start_row = next(r for r in range(n) if any(c != 8 for c in g[r]))
    # Find start_col from that row
    start_col = next(c for c in range(n) if g[start_row][c] != 8)
    # Extract pattern 9x9
    pattern = [[g[start_row + i][start_col + j] for j in range(9)] for i in range(9)]
    # Output grid all 8
    out_grid = [[8] * n for _ in range(n)]
    # out_start
    out_start = max(0, start_row - 3)
    # Compute active_top
    active_top = [i for i in range(3) if not all(x == 8 for x in pattern[i][3:6])]
    active_top = active_top[::-1]
    while len(active_top) < 3:
        active_top.append(active_top[-1])
    # Compute added_top_rows
    added_top_rows = []
    for kk in range(3):
        pat_ii = active_top[kk]
        row = pattern[pat_ii]
        l_g = row[6:9]
        m_g = row[3:6]
        r_g = row[0:3]
        temp_row = [8] * n
        pos_l = start_col - 3
        for jj in range(3):
            temp_row[pos_l + jj] = l_g[jj]
        pos_m = start_col + 3
        for jj in range(3):
            temp_row[pos_m + jj] = m_g[jj]
        pos_r = start_col + 9
        for jj in range(3):
            temp_row[pos_r + jj] = r_g[jj]
        added_top_rows.append(temp_row)
    # Set added top
    for kk in range(3):
        out_r = out_start + kk
        out_grid[out_r] = added_top_rows[kk][:]
    # Set added bottom: reverse of top
    for kk in range(3):
        out_r = out_start + 12 + kk
        out_grid[out_r] = added_top_rows[2 - kk][:]
    # Preserved top
    for ii in range(3):
        out_r = out_start + 3 + ii
        out_grid[out_r] = g[start_row + ii][:]
    # Preserved bottom
    for ii in range(3):
        out_r = out_start + 9 + ii
        out_grid[out_r] = g[start_row + 6 + ii][:]
    # Modified middle
    for mm in range(3):
        ii = 3 + mm
        out_r = out_start + 6 + mm
        row = pattern[ii]
        swapped_left = row[6:9]
        orig_left = row[0:3]
        if mm == 1:  # i=4
            core = [row[2], pattern[2][5], row[6]]
        else:  # i=3 or 5
            core = [pattern[2][2], pattern[2][4], pattern[2][6]]
        orig_right = row[6:9]
        swapped_right = row[0:3]
        expanded = swapped_left + orig_left + core + orig_right + swapped_right
        pos_start = start_col - 3
        for jj in range(15):
            out_grid[out_r][pos_start + jj] = expanded[jj]
    return out_grid
```