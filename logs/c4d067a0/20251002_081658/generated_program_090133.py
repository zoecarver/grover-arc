```python
from typing import List, Optional, Tuple
from collections import Counter

def get_background(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_signal_colors(grid: List[List[int]], bg: int, n: int) -> List[List[int]]:
    signal_colors = []
    for r in range(1, n, 2):
        level = []
        for c in range(1, n, 2):
            if 0 <= c < n and grid[r][c] != bg:
                left_bg = (c <= 0 or grid[r][c - 1] == bg)
                right_bg = (c >= n - 1 or grid[r][c + 1] == bg)
                if left_bg and right_bg:
                    level.append(grid[r][c])
        if level:
            signal_colors.append(level)
    return signal_colors

def extract_bars(grid: List[List[int]], r: int, n: int, bg: int, min_w: int = 2) -> List[Tuple[int, int, int]]:
    row = grid[r]
    bars = []
    c = 0
    while c < n:
        if row[c] == bg:
            c += 1
            continue
        colr = row[c]
        start = c
        while c < n and row[c] == colr:
            c += 1
        w = c - start
        if w >= min_w:
            bars.append((start, w, colr))
    return bars

def detect_existing_tier(grid: List[List[int]], bg: int, n: int) -> Optional[Tuple[int, int, List[int], List[int], int, int]]:
    for start_r in range(n):
        bars0 = extract_bars(grid, start_r, n, bg)
        if not bars0:
            continue
        widths = [b[1] for b in bars0]
        if len(set(widths)) != 1:
            continue
        bar_w = widths[0]
        bar_struct = bars0
        h = 1
        for rr in range(start_r + 1, n):
            if rr - start_r >= bar_w:
                break
            bars_rr = extract_bars(grid, rr, n, bg)
            if bars_rr != bar_struct:
                break
            h += 1
        if h == bar_w:
            bar_starts = [b[0] for b in bar_struct]
            colors = [b[2] for b in bar_struct]
            M = len(bar_struct)
            step = bar_starts[1] - bar_starts[0] if M >= 2 else bar_w + 2
            return start_r, bar_w, bar_starts, colors, M, step
        if h < bar_w:
            add_up = bar_w - h
            new_start = start_r - add_up
            if new_start >= 0:
                bar_cols = set()
                for start_c, _, _ in bar_struct:
                    for dc in range(bar_w):
                        if start_c + dc < n:
                            bar_cols.add(start_c + dc)
                can_complete = True
                for rr in range(new_start, start_r):
                    for cc in bar_cols:
                        if grid[rr][cc] != bg:
                            can_complete = False
                            break
                    if not can_complete:
                        break
                if can_complete:
                    bar_starts = [b[0] for b in bar_struct]
                    colors = [b[2] for b in bar_struct]
                    M = len(bar_struct)
                    step = bar_starts[1] - bar_starts[0] if M >= 2 else bar_w + 2
                    return new_start, bar_w, bar_starts, colors, M, step
    return None

def fill_if_background(grid: List[List[int]], r_start: int, c_start: int, h: int, w: int, color: int, bg: int, n: int):
    for dr in range(h):
        r = r_start + dr
        if not (0 <= r < n):
            continue
        for dc in range(w):
            c = c_start + dc
            if 0 <= c < n and grid[r][c] == bg:
                grid[r][c] = color

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    n = len(grid)
    bg = get_background(grid)
    signal_colors = get_signal_colors(grid, bg, n)
    T = len(signal_colors)
    if T == 0:
        return grid
    tier_info = detect_existing_tier(grid, bg, n)
    if tier_info is None:
        return grid
    start_r_exist, tier_h, bar_starts, exist_colors, M, step = tier_info
    k_exist = -1
    j_offset = -1
    for k in range(T):
        sig = signal_colors[k]
        for j in range(len(sig) - M + 1):
            if sig[j:j + M] == exist_colors:
                k_exist = k
                j_offset = j
                break
        if k_exist != -1:
            break
    if k_exist == -1:
        return grid
    base_start = bar_starts[0] - j_offset * step
    for k in range(T):
        sig = signal_colors[k]
        N = len(sig)
        start_r_k = start_r_exist + (k - k_exist) * step
        if start_r_k < 0 or start_r_k + tier_h > n:
            continue
        for ll in range(N):
            c_start = base_start + ll * step
            if c_start < 0 or c_start + tier_h > n:
                continue
            color = sig[ll]
            fill_if_background(grid, start_r_k, c_start, tier_h, tier_h, color, bg, n)
    return grid
```