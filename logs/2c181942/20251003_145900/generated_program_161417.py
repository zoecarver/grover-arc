```python
from typing import List, Dict
from collections import defaultdict

def create_background_grid(h: int, w: int) -> List[List[int]]:
    return [[8] * w for _ in range(h)]

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def has_color(g: List[List[int]], c: int) -> bool:
    for row in g:
        if c in row:
            return True
    return False

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    new_g = copy_grid(g)
    if has_color(g, 6):
        h = len(new_g)
        w = len(new_g[0]) if h > 0 else 0
        for i in range(h):
            for j in range(w):
                if new_g[i][j] == 4:
                    new_g[i][j] = 8
    return new_g

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    counts = defaultdict(int)
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    for i in range(h):
        for j in range(w):
            c = g[i][j]
            if c != 8:
                counts[c] += 1
    return dict(counts)

def compute_avg_cols(g: List[List[int]]) -> Dict[int, float]:
    totals = defaultdict(float)
    counts = defaultdict(int)
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    for i in range(h):
        for j in range(w):
            c = g[i][j]
            if c != 8:
                totals[c] += j
                counts[c] += 1
    avgs = {}
    for c in counts:
        avgs[c] = totals[c] / counts[c]
    return avgs

def get_color_order(avgs: Dict[int, float], colors: List[int]) -> List[int]:
    def key_func(c: int) -> tuple[float, int]:
        return (avgs.get(c, float('inf')), -c)
    return sorted(colors, key=key_func)

def get_shape_params(n: int, c: int) -> tuple[List[int], int]:
    if n <= 2:
        is_odd = (c % 2 == 1)
        if is_odd:
            return [0, 0, 0, n], n
        else:
            return [n, 0, 0, 0], n
    is_odd = (c % 2 == 1)
    k = 5 if is_odd else 7
    w = (n + k) // 4
    t = max(0, n // 2 - w)
    widths = [t, w, w, t]
    base = sum(widths)
    remaining = n - base
    if remaining > 0:
        widths[1] += remaining // 2
        widths[2] += remaining - (remaining // 2)
    elif remaining < 0:
        diff = -remaining
        widths[1] -= diff // 2
        widths[2] -= diff - (diff // 2)
        widths = [max(0, x) for x in widths]
    bw = max(widths) if any(widths) else 0
    return widths, bw

def place_shape(out: List[List[int]], c: int, widths: List[int], place_col: int, start_row: int, bw: int, h: int, w: int) -> None:
    is_odd = (c % 2 == 1)
    for rel in range(4):
        r = start_row + rel
        if not (0 <= r < h):
            continue
        wi = widths[rel]
        if wi == 0:
            continue
        offset = 0 if is_odd else (bw - wi)
        if is_odd and 1 <= rel <= 2:
            offset += 1
        sc = place_col + offset
        for k in range(wi):
            cc = sc + k
            if 0 <= cc < w:
                out[r][cc] = c

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    cleaned = remove_yellow_if_pink(g)
    counts = count_colors(cleaned)
    colors = [c for c in range(1, 8) if counts.get(c, 0) > 0]
    avgs = compute_avg_cols(cleaned)
    order = get_color_order(avgs, colors)
    out = create_background_grid(h, w)
    start_row = (h - 4) // 2 - (1 if h % 2 == 1 else 0)
    current_col = 2
    prev_col = None
    prev_avg = None
    for c in order:
        n = counts.get(c, 0)
        if n == 0:
            continue
        widths, bw = get_shape_params(n, c)
        is_odd = (c % 2 == 1)
        if n <= 2 and prev_avg is not None and abs(avgs.get(c, 0) - prev_avg) < 5:
            # stack on previous
            place_col = prev_col
            rel = 3 if is_odd else 0
            r = start_row + rel
            wi = n
            sc = place_col
            if 0 <= r < h:
                for k in range(wi):
                    cc = sc + k
                    if 0 <= cc < w:
                        out[r][cc] = c
            # do not advance current_col
        else:
            # normal placement
            place_col = current_col
            place_shape(out, c, widths, place_col, start_row, bw, h, w)
            sep = 0 if n <= 2 else 1
            current_col += bw + sep
            prev_col = place_col
        prev_avg = avgs.get(c, 0)
    return out
```