```python
import copy

def get_doubled_sequence(row_data: List[int], center: int) -> List[int]:
    blocks = []
    first_non4 = -1
    n_non4 = 0
    i = 0
    while i < center:
        if row_data[i] == 4:
            i += 1
            continue
        if first_non4 == -1:
            first_non4 = i
        val = row_data[i]
        j = i
        while j < center and row_data[j] == val:
            j += 1
        length = j - i
        blocks.append((val, length))
        n_non4 += length
        i = j
    if not blocks:
        return [4] * center
    shift = n_non4 // 2
    start_col = max(0, first_non4 - shift)
    new_row = [4] * center
    pos = start_col
    for val, length in blocks:
        for _ in range(2 * length):
            if pos < center:
                new_row[pos] = val
            pos += 1
    return new_row

def extract_uniques(g: List[List[int]]) -> tuple[List[tuple[List[int], int, int, List[int], int]], int]:
    seen = set()
    uniques = []
    num_non4_rows = 0
    for r in range(13):
        row_data = g[r][:13]
        t = tuple(row_data)
        has_non4 = any(v != 4 for v in row_data)
        if has_non4:
            num_non4_rows += 1
        if has_non4 and t not in seen:
            non4_pos = [i for i in range(13) if row_data[i] != 4]
            min_c = min(non4_pos)
            max_c = max(non4_pos)
            seq = [row_data[i] for i in range(min_c, max_c + 1)]
            rev_seq = seq[::-1]
            uniques.append((row_data, min_c, max_c, rev_seq, max_c - min_c + 1))
            seen.add(t)
    return uniques, num_non4_rows

def set_central_cross(grid: List[List[int]]) -> None:
    for r in range(27):
        grid[r][13] = 1
    for c in range(27):
        grid[13][c] = 1

def process_upper(grid: List[List[int]]) -> None:
    for r in range(13):
        i = 0
        while i < 13:
            if grid[r][i] == 4:
                i += 1
                continue
            j = i
            while j < 13 and grid[r][j] != 4:
                j += 1
            seq = grid[r][i:j]
            rev_seq = seq[::-1]
            min_c = i
            max_c = j - 1
            t_start = 26 - max_c
            t_end = 26 - min_c
            pos = 0
            for tc in range(t_start, t_end + 1):
                if grid[r][tc] == 4:
                    grid[r][tc] = rev_seq[pos]
                pos += 1
            i = j
    for r in range(12):
        if grid[r][5:9] == [2, 2, 3, 3] and all(grid[r + 1][c] == 4 for c in range(13)):
            for tc in range(18, 22):
                grid[r][tc] = 4
    pairs = [(14, 15), (16, 17), (18, 19), (20, 21), (22, 23), (24, 25)]
    for r in range(1, 13):
        for p1, p2 in pairs:
            if (grid[r][p1] == 4 and grid[r][p2] == 4 and
                grid[r + 1][p1] == 8 and grid[r + 1][p2] == 8):
                grid[r][p1] = 8
                grid[r][p2] = 8

def has_nines(grid: List[List[int]]) -> bool:
    return any(9 in row for row in grid)

def process_lower_no_nine(grid: List[List[int]]) -> None:
    for r in range(14, 27):
        i = 0
        while i < 13:
            if grid[r][i] != 2:
                i += 1
                continue
            j = i
            while j < 13 and grid[r][j] == 2:
                j += 1
            length = j - i
            for d in range(1, length + 1):
                c = j + d - 1
                if c > 12 or grid[r][c] != 4:
                    break
                grid[r][c] = 3
            i = j
        i = 14
        while i <= 26:
            if grid[r][i] != 2:
                i += 1
                continue
            j = i
            while j <= 26 and grid[r][j] == 2:
                j += 1
            length = j - i
            for d in range(1, length + 1):
                c = i - d
                if c < 14 or grid[r][c] != 4:
                    break
                grid[r][c] = 3
            i = j
    for r in range(13):
        for c in range(13):
            if grid[r][c] != 4:
                tr = 26 - r
                tc = 26 - c
                if tr >= 14 and tc >= 14 and grid[tr][tc] == 4:
                    grid[tr][tc] = grid[r][c]
    for r in range(14, 26):
        for c in range(13):
            if grid[r][c] == 2:
                is_isolated = (c == 0 or grid[r][c - 1] != 2) and (c == 12 or grid[r][c + 1] != 2)
                if is_isolated and grid[r + 1][c] == 4:
                    grid[r + 1][c] = 8
    for r in range(14, 27):
        i = 14
        while i <= 26:
            if grid[r][i] != 8:
                i += 1
                continue
            j = i
            while j <= 26 and grid[r][j] == 8:
                j += 1
            if i > 14 and grid[r][i - 1] == 4:
                grid[r][i - 1] = 8
            i = j
    for r in range(14, 26):
        i = 14
        while i <= 26:
            if grid[r][i] != 8:
                i += 1
                continue
            j = i
            while j <= 26 and grid[r][j] == 8:
                j += 1
            run_start = i
            run_end = j - 1
            if r + 1 <= 26 and all(grid[r + 1][cc] == 4 for cc in range(run_start, run_end + 1)):
                for cc in range(run_start, run_end + 1):
                    grid[r + 1][cc] = 8
            i = j

def process_lower_has_nine(grid: List[List[int]]) -> None:
    uniques, _ = extract_uniques(grid)
    if not uniques:
        return
    block_info = []
    current = 26
    for k in range(len(uniques)):
        num = 1 << k
        top = current - num + 1
        bottom = current
        block_info.append((top, bottom))
        current = top - 1
    for k in range(len(uniques)):
        top, bottom = block_info[k]
        row_data = uniques[k][0]
        doubled = get_doubled_sequence(row_data, 13)
        for rr in range(top, bottom + 1):
            for c in range(13):
                grid[rr][c] = doubled[c]
        has_nine_u = 9 in row_data[:13]
        min_c = uniques[k][1]
        rev_seq = uniques[k][3]
        len_r = len(rev_seq)
        start_col_r = 14 + min_c
        if has_nine_u and top < bottom:
            for rr in range(top + 1, bottom):
                for ii in range(len_r):
                    tc = start_col_r + ii
                    if tc > 26:
                        break
                    grid[rr][tc] = rev_seq[ii]
        if k >= 2:
            prev_k = k - 1
            prev_min_c = uniques[prev_k][1]
            prev_rev = uniques[prev_k][3]
            prev_len = len(prev_rev)
            prev_start = 14 + prev_min_c
            rr = bottom
            for ii in range(prev_len):
                tc = prev_start + ii
                if tc > 26:
                    break
                grid[rr][tc] = prev_rev[ii]
        if not has_nine_u:
            partial_len = len_r // 2
            if partial_len > 0:
                rr = top
                for ii in range(partial_len):
                    tc = start_col_r + ii
                    if tc > 26:
                        break
                    grid[rr][tc] = rev_seq[ii]
    for r in range(14, 27):
        grid[r][13] = 1

def program(g: List[List[int]]) -> List[List[int]]:
    grid = copy.deepcopy(g)
    set_central_cross(grid)
    process_upper(grid)
    if not has_nines(grid):
        process_lower_no_nine(grid)
    else:
        process_lower_has_nine(grid)
    return grid
```