```python
from typing import List, Tuple

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def get_bg(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def get_small_rows(g: List[List[int]], bg: int) -> List[int]:
    candidates = [1, 3, 5, 7]
    n = len(g)
    return [r for r in candidates if r < n and g[r][1] != bg and g[r][3] != bg]

def has_col5(g: List[List[int]], bg: int, r: int) -> bool:
    n = len(g)
    return 0 <= r < n and g[r][5] != bg

def find_large_layer(g: List[List[int]], bg: int) -> Tuple[int, int, List[Tuple[int, int, int]]]:
    n = len(g)
    if n == 0:
        return 0, 0, []
    m = len(g[0])
    large_rs = [r for r in range(n) if any(c != bg for c in g[r][8:m])]
    if not large_rs:
        return 0, 0, []
    start_r = min(large_rs)
    h = max(large_rs) - start_r + 1
    blocks = []
    i = 8
    while i < m:
        if g[start_r][i] == bg:
            i += 1
            continue
        colr = g[start_r][i]
        j = i + 1
        while j < m and g[start_r][j] == colr:
            j += 1
        w = j - i
        blocks.append((i, w, colr))
        i = j
    return start_r, h, blocks

def program(g: List[List[int]]) -> List[List[int]]:
    g_out = copy_grid(g)
    bg = get_bg(g)
    small_rows = get_small_rows(g, bg)
    t = len(small_rows)
    if t == 0:
        return g_out
    large_start, h, blocks = find_large_layer(g, bg)
    if not blocks:
        return g_out
    p = len(blocks)
    spacing = blocks[1][0] - blocks[0][0] if p >= 2 else 0
    n = len(g)
    m = len(g[0]) if n > 0 else 0
    is_top = large_start < n // 2
    layer_starts = [0] * t
    if is_top:
        layer_starts[0] = large_start
        num_full = max(0, t - 2)
        for k in range(1, t):
            if k - 1 < num_full:
                d = 2 * h
            else:
                d = 2 * h - 1
            layer_starts[k] = layer_starts[k - 1] + d
    else:
        d = 2 * h + 1
        layer_starts[t - 1] = large_start
        for k in range(t - 2, -1, -1):
            layer_starts[k] = layer_starts[k + 1] - d
    # clip added layers
    for k in range(1, t):
        st = layer_starts[k]
        if st + h - 1 >= n:
            layer_starts[k] = n - h
        if st < 0:
            layer_starts[k] = 0
    # input st_cols and ws
    input_st_cols = [b[0] for b in blocks]
    input_ws = [b[1] for b in blocks]
    w = input_ws[0] if input_ws else h  # assume square
    # add added layers
    for k in range(1, t):
        sr = small_rows[k]
        color1 = g[sr][1]
        color2 = g[sr][3]
        layer_colors = [color1, color2][:p]
        layer_st_cols = list(input_st_cols)
        layer_ws_list = list(input_ws)
        if has_col5(g, bg, sr) and p >= 1:
            extra_st = input_st_cols[-1] + spacing
            layer_st_cols.append(extra_st)
            layer_ws_list.append(w)
            layer_colors.append(g[sr][5])
        st_r = layer_starts[k]
        for bi in range(len(layer_st_cols)):
            sc = layer_st_cols[bi]
            ww = layer_ws_list[bi]
            cl = layer_colors[bi]
            for rr in range(st_r, st_r + h):
                if 0 <= rr < n:
                    for cc in range(sc, min(sc + ww, m)):
                        if g_out[rr][cc] == bg:
                            g_out[rr][cc] = cl
    return g_out
```