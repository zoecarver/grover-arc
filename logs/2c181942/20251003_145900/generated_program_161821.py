```python
from typing import List, Dict
from collections import defaultdict, deque

def create_background_grid(h: int, w: int) -> List[List[int]]:
    return [[8] * w for _ in range(h)]

def has_color(g: List[List[int]], c: int) -> bool:
    return any(c in row for row in g)

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if has_color(new_g, 6):
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
            if g[i][j] != 8:
                counts[g[i][j]] += 1
    return dict(counts)

def compute_avg_col(g: List[List[int]], c: int) -> float:
    total = 0.0
    count = 0
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    for i in range(h):
        for j in range(w):
            if g[i][j] == c:
                total += j
                count += 1
    return total / count if count > 0 else 0.0

def get_shape_widths(n: int, c: int) -> List[int]:
    is_odd = c % 2 == 1
    if n <= 2:
        if is_odd:
            return [0, 0, 0, n]
        else:
            return [n, 0, 0, 0]
    k = 5 if is_odd else 7
    w_base = (n + k) // 4
    t = max(0, n // 2 - w_base)
    widths = [t, w_base, w_base, t]
    base_sum = sum(widths)
    remaining = n - base_sum
    if remaining > 0:
        widths[1] += remaining // 2
        widths[2] += remaining - (remaining // 2)
    elif remaining < 0:
        diff = -remaining
        widths[1] -= diff // 2
        widths[2] -= diff - (diff // 2)
        widths = [max(0, x) for x in widths]
    return widths

def max_component_size(g: List[List[int]], c: int) -> int:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    visited = [[False] * w for _ in range(h)]
    max_size = 0
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == c and not visited[i][j]:
                size = 0
                q = deque([(i, j)])
                visited[i][j] = True
                while q:
                    x, y = q.popleft()
                    size += 1
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == c:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                max_size = max(max_size, size)
    return max_size

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    cleaned = remove_yellow_if_pink(g)
    color_counts = count_colors(cleaned)
    colors = [k for k in color_counts if k != 8 and color_counts[k] > 0]
    if not colors:
        return create_background_grid(h, w)
    avgs = {c: compute_avg_col(cleaned, c) for c in colors}
    ordered_colors = sorted(colors, key=lambda c: (avgs[c], -c))
    start_row = (h - 4) // 2
    out = create_background_grid(h, w)
    current_col = 0
    for c in ordered_colors:
        n = color_counts[c]
        max_comp = max_component_size(cleaned, c)
        widths = get_shape_widths(n, c)
        bw = max(widths) if widths else 0
        if bw == 0:
            continue
        is_odd = c % 2 == 1
        box_start = current_col
        for r in range(4):
            wi = widths[r]
            if wi == 0:
                continue
            row_idx = start_row + r
            if not (0 <= row_idx < h):
                continue
            offset = 0 if is_odd else (bw - wi)
            col_start = box_start + offset
            for k in range(wi):
                col = col_start + k
                if 0 <= col < w:
                    out[row_idx][col] = c
        current_col += bw + 1
    # Center horizontally
    used_cols = set()
    for row in out:
        for col in range(w):
            if row[col] != 8:
                used_cols.add(col)
    if used_cols:
        min_c = min(used_cols)
        max_c = max(used_cols)
        span = max_c - min_c + 1
        left_margin = (w - span) // 2
        shift = left_margin - min_c
        new_out = create_background_grid(h, w)
        for r in range(h):
            for col in range(w):
                if out[r][col] != 8:
                    new_col = col + shift
                    if 0 <= new_col < w:
                        new_out[r][new_col] = out[r][col]
        out = new_out
    return out
```