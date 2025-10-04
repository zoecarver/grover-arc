```python
def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    orig_w = len(g[0])
    label_col = next(i for i, val in enumerate(g[0]) if val == 0)
    content_grid = [row[:label_col] + row[label_col + 1:] for row in g[1:]]
    if not content_grid:
        return []
    w = len(content_grid[0])
    reverse = label_col > (orig_w - 1) // 2
    if reverse:
        content_grid = [row[::-1] for row in content_grid]
    if w > 7:
        # Wide mode
        def get_max_h_run(grid):
            max_r = 0
            for row in grid:
                j = 0
                n = len(row)
                while j < n:
                    if row[j] == 8:
                        j += 1
                        continue
                    c = row[j]
                    start = j
                    j += 1
                    while j < n and row[j] == c:
                        j += 1
                    max_r = max(max_r, j - start)
            return max_r
        max_w = get_max_h_run(content_grid)
        if max_w == 0:
            return []
        output = []
        i = 0
        h_c = len(content_grid)
        while i < h_c:
            row = content_grid[i]
            if all(x == 8 for x in row):
                i += 1
                continue
            start = i
            i += 1
            while i < h_c and content_grid[i] == row:
                i += 1
            group_h = i - start
            # Extract runs >=2
            runs = []
            j = 0
            n = len(row)
            while j < n:
                if row[j] == 8:
                    j += 1
                    continue
                c = row[j]
                l = 1
                j += 1
                while j < n and row[j] == c:
                    l += 1
                    j += 1
                if l >= 2:
                    runs.append((c, l))
            for c, l in runs:
                pad_l = (max_w - l) // 2
                pad_r = max_w - l - pad_l
                bar = [8] * pad_l + [c] * l + [8] * pad_r
                for _ in range(group_h):
                    output.append(bar)
        return output
    else:
        # Tall mode
        content_cols = [1, 2, 4, 5]
        def get_max_v_run(grid, cols):
            max_r = 0
            h = len(grid)
            for col in cols:
                if col >= len(grid[0]):
                    continue
                i = 0
                while i < h:
                    if grid[i][col] == 8:
                        i += 1
                        continue
                    c = grid[i][col]
                    start = i
                    i += 1
                    while i < h and grid[i][col] == c:
                        i += 1
                    max_r = max(max_r, i - start)
            return max_r
        max_w = get_max_v_run(content_grid, content_cols)
        if max_w == 0:
            return []
        def process_band(grid, band_l_col, band_r_col, max_w):
            sub_out = []
            h = len(grid)
            i = 0
            while i < h:
                if grid[i][band_l_col] == 8 and grid[i][band_r_col] == 8:
                    i += 1
                    continue
                start = i
                i += 1
                while i < h and not (grid[i][band_l_col] == 8 and grid[i][band_r_col] == 8):
                    i += 1
                group_h = i - start
                # Seq for right col of band
                seq_r = [grid[start + j][band_r_col] for j in range(group_h)]
                l_r = len(seq_r)
                p_l_r = (max_w - l_r) // 2
                p_r_r = max_w - l_r - p_l_r
                row_r = [8] * p_l_r + seq_r + [8] * p_r_r
                sub_out.append(row_r)
                # Seq for left col of band
                seq_l = [grid[start + j][band_l_col] for j in range(group_h)]
                l_l = len(seq_l)
                p_l_l = (max_w - l_l) // 2
                p_r_l = max_w - l_l - p_l_l
                row_l = [8] * p_l_l + seq_l + [8] * p_r_l
                sub_out.append(row_l)
            return sub_out
        left_out = process_band(content_grid, 1, 2, max_w)
        right_out = process_band(content_grid, 4, 5, max_w)
        return left_out + right_out
```