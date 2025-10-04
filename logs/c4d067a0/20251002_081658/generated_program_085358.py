```python
from typing import List, Optional, Tuple
from collections import Counter

def get_background(grid: List[List[int]]) -> int:
    flat = [cell for row in grid for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_signal_list(grid: List[List[int]], bg: int, rows: int, cols: int) -> List[Tuple[int, List[int], List[int]]]:
    signal_list = []
    for r in range(1, rows, 2):
        sig_cols = [c for c in range(1, cols, 2) if grid[r][c] != bg]
        if sig_cols:
            colors = [grid[r][c] for c in sig_cols]
            signal_list.append((r, colors, sig_cols))
    return signal_list

def detect_existing_tier(grid: List[List[int]], bg: int, rows: int, cols: int) -> Optional[Tuple[int, int, List[int], List[int], int, int]]:
    i = 0
    while i < rows:
        pattern = tuple(grid[i])
        j = i + 1
        while j < rows and tuple(grid[j]) == pattern:
            j += 1
        height = j - i
        if height < 1:
            i = j
            continue
        bars = []
        c = 0
        while c < cols:
            if pattern[c] == bg:
                c += 1
                continue
            color = pattern[c]
            start = c
            while c < cols and pattern[c] == color:
                c += 1
            width = c - start
            bars.append((start, width, color))
        if bars:
            widths = [b[1] for b in bars]
            if len(set(widths)) == 1:
                bar_w = widths[0]
                bar_starts = [b[0] for b in bars]
                bar_colors = [b[2] for b in bars]
                M = len(bars)
                return height, i, bar_starts, bar_colors, M, bar_w
        i = j
    return None

def fill_if_background(grid: List[List[int]], r_start: int, c_start: int, h: int, w: int, color: int, bg: int, rows: int, cols: int):
    for dr in range(h):
        r = r_start + dr
        if not (0 <= r < rows):
            continue
        for dc in range(w):
            c = c_start + dc
            if 0 <= c < cols and grid[r][c] == bg:
                grid[r][c] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    grid = [row[:] for row in g]
    bg = get_background(grid)
    signal_list = get_signal_list(grid, bg, n, n)
    T = len(signal_list)
    if T == 0:
        return grid
    existing = detect_existing_tier(grid, bg, n, n)
    if existing is None:
        return grid
    h, start_r, bar_starts, bar_colors, M, bar_w = existing
    if M < 1:
        return grid
    step_col = bar_starts[1] - bar_starts[0] if M >= 2 else bar_w + 1
    # Find k_existing
    k_existing = -1
    for kk in range(T):
        colors_k = signal_list[kk][1]
        found = False
        for o in range(len(colors_k) - M + 1):
            if colors_k[o:o + M] == bar_colors:
                found = True
                break
        if found:
            k_existing = kk
            break
    if k_existing == -1:
        return grid
    tier_h = bar_w
    # Fill missing bars for existing level
    colors_k = signal_list[k_existing][1]
    N_k = len(colors_k)
    if N_k > M:
        current_last = bar_starts[-1]
        for ii in range(M, N_k):
            next_start = current_last + step_col
            colr = colors_k[ii]
            fill_if_background(grid, start_r, next_start, h, bar_w, colr, bg, n, n)
            current_last = next_start
    # Complete top if reaches bottom
    reaches_bottom = (start_r + h - 1 == n - 1)
    if reaches_bottom:
        top_start = start_r - 1
        if top_start >= 0:
            # Check if row top_start is bg in original bar pos
            can_fill = True
            for bs in bar_starts:
                for dc in range(bar_w):
                    cc = bs + dc
                    if cc < n and grid[top_start][cc] != bg:
                        can_fill = False
                        break
                if not can_fill:
                    break
            if can_fill:
                # Fill the top row
                for ib, bs in enumerate(bar_starts):
                    colr = bar_colors[ib]
                    fill_if_background(grid, top_start, bs, 1, bar_w, colr, bg, n, n)
    # Now fill new tiers
    starts_dict = {}
    # Below
    current_start = start_r
    for dk in range(1, T - k_existing):
        current_k = k_existing + dk
        if dk == 1:
            adj = max(0, tier_h - h)
            step = step_col - adj
        else:
            step = step_col
        new_start = current_start + step
        if new_start < 0 or new_start + tier_h > n:
            break
        starts_dict[current_k] = new_start
        current_start = new_start
    # Above
    current_start = start_r
    adjust_first = 1 if reaches_bottom else 0
    for dk in range(1, k_existing + 1):
        current_k = k_existing - dk
        if dk == 1:
            step = step_col + adjust_first
        else:
            step = step_col
        new_start = current_start - step
        if new_start < 0 or new_start + tier_h > n:
            break
        starts_dict[current_k] = new_start
        current_start = new_start
    # Now fill for each j != k_existing
    for j in range(T):
        if j == k_existing:
            continue
        if j not in starts_dict:
            continue
        tier_start = starts_dict[j]
        colors_j = signal_list[j][1]
        N_j = len(colors_j)
        if N_j == 0:
            continue
        # Compute bar starts for this j
        local_starts = bar_starts[:min(N_j, M)]
        if N_j > M:
            current_last = bar_starts[-1] if M > 0 else 0  # assume if M=0 rare
            for ii in range(M, N_j):
                next_s = current_last + step_col
                local_starts.append(next_s)
                current_last = next_s
        # Now fill each bar
        for ib in range(N_j):
            if ib >= len(local_starts):
                break
            bs = local_starts[ib]
            colr = colors_j[ib]
            fill_if_background(grid, tier_start, bs, tier_h, bar_w, colr, bg, n, n)
    return grid
```