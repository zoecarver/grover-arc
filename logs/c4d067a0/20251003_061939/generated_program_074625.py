```python
def get_background(g: List[List[int]]) -> int:
    n = len(g)
    count = {}
    for row in g:
        for c in row:
            count[c] = count.get(c, 0) + 1
    return max(count, key=count.get)

def find_runs(row: List[int], bg: int, n: int) -> List[tuple]:
    runs = []
    i = 0
    while i < n:
        if row[i] == bg:
            i += 1
            continue
        start = i
        color = row[i]
        i += 1
        while i < n and row[i] == color:
            i += 1
        length = i - start
        if length >= 2:
            runs.append((start, length, color))
    return runs

def find_existing_blocks(g: List[List[int]], bg: int, key_set: set, n: int) -> tuple:
    for start_r in range(n):
        first_row_runs = find_runs(g[start_r], bg, n)
        if not first_row_runs:
            continue
        max_possible_h = n - start_r
        for hh in range(2, max_possible_h + 1):
            same_runs = True
            for r_off in range(1, hh):
                r = start_r + r_off
                this_runs = find_runs(g[r], bg, n)
                if len(this_runs) != len(first_row_runs):
                    same_runs = False
                    break
                for idx in range(len(first_row_runs)):
                    tr_start, tr_len, _ = this_runs[idx]
                    fr_start, fr_len, _ = first_row_runs[idx]
                    if tr_start != fr_start or tr_len != fr_len:
                        same_runs = False
                        break
                if not same_runs:
                    break
            if not same_runs:
                continue
            all_widths = {run[1] for run in first_row_runs}
            if len(all_widths) != 1:
                continue
            ww = next(iter(all_widths))
            consistent = True
            for run_idx in range(len(first_row_runs)):
                s_col, _, colr = first_row_runs[run_idx]
                for r_off in range(hh):
                    r = start_r + r_off
                    for off_c in range(ww):
                        c = s_col + off_c
                        if g[r][c] != colr:
                            consistent = False
                            break
                    if not consistent:
                        break
                if not consistent:
                    break
            if consistent:
                block_starts = [run[0] for run in first_row_runs]
                block_colors = [run[2] for run in first_row_runs]
                return start_r, hh, block_starts, block_colors, ww
    return None

def get_line_colors(i: int, key_rows: List[int], g: List[List[int]], bg: int, n: int) -> List[int]:
    r = key_rows[i]
    colors = []
    j = 0
    while True:
        c = 2 * j + 1
        if c >= n:
            break
        if g[r][c] != bg:
            colors.append(g[r][c])
        j += 1
    return colors

def find_i_existing(line_colors_list: List[List[int]], block_colors: List[int]) -> int:
    best_score = -1
    i_existing = -1
    for ii in range(len(line_colors_list)):
        key_seq = line_colors_list[ii]
        match_count = 0
        key_it = 0
        for col in block_colors:
            found = False
            while key_it < len(key_seq):
                if key_seq[key_it] == col:
                    match_count += 1
                    key_it += 1
                    found = True
                    break
                key_it += 1
            if not found:
                break
        if match_count > best_score:
            best_score = match_count
            i_existing = ii
    return i_existing

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_background(g)
    max_key_r = 0
    for r in range(1, n, 2):
        has_non_bg = any(g[r][c] != bg for c in range(1, n, 2))
        if has_non_bg:
            max_key_r = r
    key_rows = list(range(1, max_key_r + 2, 2))
    m = len(key_rows)
    key_set = set(key_rows)
    existing_info = find_existing_blocks(g, bg, key_set, n)
    if existing_info is None:
        return [row[:] for row in g]
    existing_start_row, h, block_starts, block_colors, w = existing_info
    if w != h:
        return [row[:] for row in g]  # invalid, copy
    k = len(block_colors)
    if k < 2:
        return [row[:] for row in g]
    horiz_d = block_starts[1] - block_starts[0]
    first_col = block_starts[0]
    line_colors_list = [get_line_colors(i, key_rows, g, bg, n) for i in range(m)]
    i_existing = find_i_existing(line_colors_list, block_colors)
    if i_existing == -1:
        return [row[:] for row in g]
    d = horiz_d
    output_grid = [row[:] for row in g]
    for i in range(m):
        line_colors = line_colors_list[i]
        num_b = len(line_colors)
        delta_i = i - i_existing
        s = existing_start_row + delta_i * d
        if s < 0 or s + h > n:
            continue
        for jj in range(num_b):
            b_color = line_colors[jj]
            c_start = first_col + jj * d
            c_end = c_start + w - 1
            if c_end >= n:
                continue
            all_bg_flag = True
            for dr in range(h):
                rr = s + dr
                for dc in range(w):
                    cc = c_start + dc
                    if output_grid[rr][cc] != bg:
                        all_bg_flag = False
                        break
                if not all_bg_flag:
                    break
            if all_bg_flag:
                for dr in range(h):
                    rr = s + dr
                    for dc in range(w):
                        cc = c_start + dc
                        output_grid[rr][cc] = b_color
    return output_grid
```