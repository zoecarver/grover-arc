```python
from typing import List, Tuple, Optional

def get_background(grid: List[List[int]]) -> int:
    return grid[0][0]

def get_signal_rows(grid: List[List[int]], bg: int, rows: int) -> List[int]:
    signal_rows = []
    for r in range(1, rows, 2):
        has_signal = False
        for c in (1, 3, 5):
            if c < len(grid[0]) and grid[r][c] != bg:
                has_signal = True
                break
        if has_signal:
            signal_rows.append(r)
        else:
            break
    return signal_rows

def get_signal_cols(grid: List[List[int]], signal_rows: List[int], bg: int) -> List[int]:
    signal_cols = [1, 3]
    if any(grid[r][5] != bg for r in signal_rows if 5 < len(grid[0])):
        signal_cols.append(5)
    return signal_cols

def detect_existing_tier(grid: List[List[int]], bg: int, rows: int, cols: int) -> Optional[Tuple[int, int, List[int], List[int], int]]:
    i = 0
    while i < rows:
        pattern = tuple(grid[i])
        j = i + 1
        while j < rows and tuple(grid[j]) == pattern:
            j += 1
        height = j - i
        if height < 2:
            i = j
            continue
        # find bars
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
            if width == height:
                bars.append((start, width, color))
        if bars:
            bar_starts = [b[0] for b in bars]
            existing_colors = [b[2] for b in bars]
            return height, i, bar_starts, existing_colors, len(bars)
        i = j
    return None

def find_existing_k(signal_rows: List[int], signal_cols: List[int], existing_colors: List[int], grid: List[List[int]], bg: int, N: int) -> int:
    T = len(signal_rows)
    for kk in range(T):
        if grid[signal_rows[kk]][signal_cols[0]] == existing_colors[0]:
            return kk + 1
    return 1  # default if no match

def compute_tier_starts(existing_k: int, tier_start_row: int, T: int, N: int, H: int) -> List[int]:
    tier_starts = [0] * (T + 1)
    tier_starts[existing_k] = tier_start_row
    small_step = H + 1
    large_step = H + 2
    step_row = 5 if N == 2 else 0  # placeholder
    # below
    current_start = tier_start_row
    for next_k in range(existing_k + 1, T + 1):
        if N == 2:
            delta = 5
        else:
            interval_num = next_k - 1
            delta = small_step if interval_num % 2 == 1 else large_step
        next_start = current_start + delta
        tier_starts[next_k] = next_start
        current_start = next_start
    # above
    current_start = tier_start_row
    for prev_k in range(existing_k - 1, 0, -1):
        if N == 2:
            delta = 5
        else:
            interval_num = prev_k
            delta = small_step if interval_num % 2 == 1 else large_step
        prev_start = current_start - delta
        tier_starts[prev_k] = prev_start
        current_start = prev_start
    return tier_starts

def get_global_bar_starts(bar_starts: List[int], N: int, H: int, M: int) -> List[int]:
    global_bar_starts = bar_starts[:]
    if M < N:
        step_col = 5 if N == 2 else (H + 1)
        last = bar_starts[-1]
        for _ in range(M, N):
            next_start = last + step_col
            global_bar_starts.append(next_start)
            last = next_start
    return global_bar_starts

def get_tier_colors(signal_rows: List[int], signal_cols: List[int], k: int, grid: List[List[int]], bg: int, N: int) -> List[Optional[int]]:
    r = signal_rows[k - 1]
    colors = []
    for j in range(N):
        c = grid[r][signal_cols[j]]
        colors.append(c if c != bg else None)
    return colors

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
    grid = [row[:] for row in g]
    rows = len(grid)
    cols = len(grid[0])
    bg = get_background(grid)
    signal_rows_list = get_signal_rows(grid, bg, rows)
    T = len(signal_rows_list)
    if T == 0:
        return grid
    signal_cols_list = get_signal_cols(grid, signal_rows_list, bg)
    N = len(signal_cols_list)
    tier_info = detect_existing_tier(grid, bg, rows, cols)
    if tier_info is None:
        return grid  # no tier, nothing to do
    H, tier_start_row, bar_starts, existing_colors, M = tier_info
    existing_k = find_existing_k(signal_rows_list, signal_cols_list, existing_colors, grid, bg, N)
    tier_starts = compute_tier_starts(existing_k, tier_start_row, T, N, H)
    global_bar_starts = get_global_bar_starts(bar_starts, N, H, M)
    for k in range(1, T + 1):
        start_r = tier_starts[k]
        if start_r < 0 or start_r + H > rows:
            continue
        tier_colors = get_tier_colors(signal_rows_list, signal_cols_list, k, grid, bg, N)
        for j in range(N):
            if tier_colors[j] is None:
                continue
            c_start = global_bar_starts[j]
            if c_start + H > cols:
                continue
            fill_if_background(grid, start_r, c_start, H, H, tier_colors[j], bg, rows, cols)
    return grid
```