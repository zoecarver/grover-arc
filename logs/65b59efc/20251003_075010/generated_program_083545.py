```python
from typing import List

def find_wall_cols(g: List[List[int]]) -> List[int]:
    if not g:
        return []
    n_cols = len(g[0])
    return [j for j in range(n_cols) if g[0][j] == 5]

def find_panel_starts(wall_cols: List[int], cols: int) -> List[int]:
    starts = [0]
    for wall in wall_cols:
        if wall + 1 < cols:
            starts.append(wall + 1)
    return starts

def get_w(starts: List[int], wall_cols: List[int], cols: int) -> int:
    if not starts:
        return 0
    next_wall = wall_cols[0] if wall_cols else cols
    return next_wall - starts[0]

def find_seed_row(g: List[List[int]]) -> int:
    rows = len(g)
    for i in range(rows - 1, -1, -1):
        if any(cell != 0 and cell != 5 for cell in g[i]):
            return i
    return 0

def get_colors(g: List[List[int]], seed_row: int, starts: List[int], w: int, m: int) -> List[int]:
    colors = []
    n_cols = len(g[0]) if g else 0
    for k in range(m):
        center = starts[k] + w // 2
        color = g[seed_row][center] if center < n_cols and seed_row < len(g) else 0
        colors.append(color)
    return colors

def get_patterns(g: List[List[int]], starts: List[int], w: int, m: int, colors: List[int]) -> List[List[List[int]]]:
    patterns = []
    n_rows = len(g)
    n_cols = len(g[0]) if g else 0
    for k in range(m):
        pat = []
        for r in range(w):
            if r >= n_rows:
                this_row = [0] * w
            else:
                row = g[r]
                five_count = 0
                for jj in range(w):
                    pos = starts[k] + jj
                    if pos < n_cols and row[pos] == 5:
                        five_count += 1
                is_wall_row = five_count > w // 2
                this_row = []
                for jj in range(w):
                    pos = starts[k] + jj
                    if pos >= n_cols:
                        this_row.append(0)
                        continue
                    cell = row[pos]
                    if is_wall_row:
                        if jj == w // 2:
                            this_row.append(0)
                        else:
                            this_row.append(colors[k])
                    elif cell != 0 and cell != 5:
                        this_row.append(colors[k])
                    else:
                        this_row.append(0)
            pat.append(this_row)
        patterns.append(pat)
    return patterns

def is_block(pattern: List[List[int]], w: int) -> bool:
    return all(sum(1 for x in row if x != 0) == w for row in pattern)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n_rows = len(g)
    n_cols = len(g[0])
    if n_cols == 0:
        return []
    wall_cols = find_wall_cols(g)
    starts = find_panel_starts(wall_cols, n_cols)
    if not starts:
        starts = [0]
    w = get_w(starts, wall_cols, n_cols)
    if w == 0:
        s = n_cols * n_cols
        return [[0] * s for _ in range(s)]
    m = min(3, len(starts))
    starts = starts[:m]
    seed_row = find_seed_row(g)
    colors = get_colors(g, seed_row, starts, w, m)
    patterns = get_patterns(g, starts, w, m, colors)
    # Pad to 3
    while len(patterns) < 3:
        empty_pat = [[0] * w for _ in range(w)]
        patterns.append(empty_pat)
        colors.append(0)
    p0, p1, p2 = patterns
    is_block_p0 = is_block(p0, w)
    s = w * w
    out = [[0] * s for _ in range(s)]
    if is_block_p0:
        # Block mode
        for i in range(w):
            # Place p1 at super col i
            col_start = i * w
            for lr in range(w):
                gr = i * w + lr
                for jj in range(w):
                    out[gr][col_start + jj] = p1[lr][jj]
            # Place p2 at super cols i+1 to w-1
            for sc in range(i + 1, w):
                col_start = sc * w
                for lr in range(w):
                    gr = i * w + lr
                    for jj in range(w):
                        out[gr][col_start + jj] = p2[lr][jj]
        # Add p0 at bottom left super row w-1 col 0
        i = w - 1
        col_start = 0
        for lr in range(w):
            gr = i * w + lr
            for jj in range(w):
                out[gr][col_start + jj] = p0[lr][jj]
    else:
        # Pointy mode
        for si in range(w - 1):
            gr_start = si * w
            # Left p2 super col 0
            col_start = 0
            for lr in range(w):
                gr = gr_start + lr
                for jj in range(w):
                    out[gr][col_start + jj] = p2[lr][jj]
            # Right p0 super col w-1
            col_start = (w - 1) * w
            for lr in range(w):
                gr = gr_start + lr
                for jj in range(w):
                    out[gr][col_start + jj] = p0[lr][jj]
        # Lower band p1 (w-1) horizontal tiles super cols 0 to w-2
        gr_start = (w - 1) * w
        for sc in range(w - 1):
            col_start = sc * w
            for lr in range(w):
                gr = gr_start + lr
                for jj in range(w):
                    out[gr][col_start + jj] = p1[lr][jj]
    return out
```