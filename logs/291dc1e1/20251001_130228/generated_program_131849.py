```python
from typing import List
from collections import defaultdict

def get_max_run(grid: List[List[int]], start_c: int, end_c: int, n_rows: int, cols: int) -> int:
    max_r = 0
    # horizontal runs
    for r in range(n_rows):
        c = start_c
        while c <= end_c:
            if grid[r][c] == 8 or grid[r][c] == 0:
                c += 1
                continue
            colr = grid[r][c]
            lenh = 1
            c += 1
            while c <= end_c and grid[r][c] == colr:
                lenh += 1
                c += 1
            max_r = max(max_r, lenh)
    # vertical runs
    for c in range(start_c, end_c + 1):
        r = 0
        while r < n_rows:
            if grid[r][c] == 8 or grid[r][c] == 0:
                r += 1
                continue
            colr = grid[r][c]
            lenv = 1
            r += 1
            while r < n_rows and grid[r][c] == colr:
                lenv += 1
                r += 1
            max_r = max(max_r, lenv)
    return max_r

def find_maximal_rects(grid: List[List[int]], start_c: int, end_c: int, n_rows: int, cols: int) -> List[tuple]:
    rects = []
    for rs in range(n_rows):
        for re in range(rs + 1, n_rows + 1):
            for cs in range(start_c, end_c + 1):
                for ce in range(cs + 1, end_c + 2):
                    # check all non-8 and non-0
                    all_non = True
                    for i in range(rs, re):
                        for j in range(cs, ce):
                            if grid[i][j] == 8 or grid[i][j] == 0:
                                all_non = False
                                break
                        if not all_non:
                            break
                    if not all_non:
                        continue
                    # check maximality
                    maxm = True
                    # up
                    if rs > 0:
                        can = True
                        for j in range(cs, ce):
                            if grid[rs - 1][j] == 8 or grid[rs - 1][j] == 0:
                                can = False
                                break
                        if can:
                            maxm = False
                    # down
                    if re < n_rows:
                        can = True
                        for j in range(cs, ce):
                            if grid[re][j] == 8 or grid[re][j] == 0:
                                can = False
                                break
                        if can:
                            maxm = False
                    # left
                    if cs > start_c:
                        can = True
                        for i in range(rs, re):
                            if grid[i][cs - 1] == 8 or grid[i][cs - 1] == 0:
                                can = False
                                break
                        if can:
                            maxm = False
                    # right
                    if ce <= end_c:
                        can = True
                        for i in range(rs, re):
                            if grid[i][ce] == 8 or grid[i][ce] == 0:
                                can = False
                                break
                        if can:
                            maxm = False
                    if maxm:
                        matrix = [[grid[i][j] for j in range(cs, ce)] for i in range(rs, re)]
                        rects.append((rs, matrix, cs, ce))
    return rects

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    cols = len(g[0])
    grid = g[1:]
    n_rows = len(grid)
    if n_rows == 0:
        return []
    # borders
    left_col = [row[0] for row in grid]
    right_col = [row[cols - 1] for row in grid]
    left_uni = len(set(left_col)) == 1 and left_col[0] != 8
    right_uni = len(set(right_col)) == 1 and right_col[0] != 8
    direction_left = not right_uni
    start_c = 1 if left_uni else 0
    end_c = cols - 2 if right_uni else cols - 1
    # max_run
    pad_width = get_max_run(grid, start_c, end_c, n_rows, cols)
    if pad_width == 0:
        return []
    # find rects
    rects = find_maximal_rects(grid, start_c, end_c, n_rows, cols)
    # lanes
    lanes = defaultdict(list)
    for rs, matrix, cs, ce in rects:
        lanes[(cs, ce)].append((rs, matrix))
    lane_keys = list(lanes.keys())
    lane_keys.sort(key=lambda k: k[0], reverse=not direction_left)
    output = []
    for key in lane_keys:
        lane_shapes = lanes[key]
        lane_shapes.sort(key=lambda x: x[0])
        for rs, matrix in lane_shapes:
            h = len(matrix)
            if h == 0:
                continue
            w = len(matrix[0])
            if h > w:
                trans = [[matrix[i][j] for i in range(h)] for j in range(w)]
                trans = trans[::-1]
                rendered = []
                for tr in trans:
                    extra = pad_width - len(tr)
                    lp = extra // 2
                    rp = extra - lp
                    prow = [8] * lp + tr + [8] * rp
                    rendered.append(prow)
            else:
                rendered = []
                for roww in matrix:
                    extra = pad_width - len(roww)
                    lp = extra // 2
                    rp = extra - lp
                    prow = [8] * lp + roww + [8] * rp
                    rendered.append(prow)
            # ensure at least 2 rows by repeating last
            while len(rendered) < 2:
                if rendered:
                    rendered.append(rendered[-1])
                else:
                    rendered.append([8] * pad_width)
            output.extend(rendered)
    return output
```