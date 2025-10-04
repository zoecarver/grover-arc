```python
from collections import deque, Counter
from copy import deepcopy
from typing import List, Tuple, Optional

def is_border_connected(grid: List[List[int]], color: int, h: int, w: int) -> bool:
    if color == 0:
        return False
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        if grid[r][0] == color and not visited[r][0]:
            q.append((r, 0))
            visited[r][0] = True
        if grid[r][w - 1] == color and not visited[r][w - 1]:
            q.append((r, w - 1))
            visited[r][w - 1] = True
    for c in range(w):
        if grid[0][c] == color and not visited[0][c]:
            q.append((0, c))
            visited[0][c] = True
        if grid[h - 1][c] == color and not visited[h - 1][c]:
            q.append((h - 1, c))
            visited[h - 1][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] == color:
                visited[nr][nc] = True
                q.append((nr, nc))
    total_count = sum(1 for row in grid for cell in row if cell == color)
    visited_count = sum(1 for row in visited for cell in row if cell)
    return visited_count == total_count

def get_background(grid: List[List[int]]) -> int:
    h = len(grid)
    if h == 0:
        return 0
    w = len(grid[0])
    flat = [cell for row in grid for cell in row]
    counter = Counter(flat)
    candidates = [(counter[color], color) for color in counter if is_border_connected(grid, color, h, w)]
    if not candidates:
        return 0
    candidates.sort(reverse=True)
    return candidates[0][1]

def get_freq_non_bg(grid: List[List[int]], bg: int) -> Counter:
    flat = [cell for row in grid for cell in row if cell != bg]
    return Counter(flat)

def get_bbox_for_color(grid: List[List[int]], color: int, h: int, w: int) -> Optional[Tuple[int, int, int, int]]:
    min_r = h
    max_r = -1
    min_c = w
    max_c = -1
    for r in range(h):
        for c in range(w):
            if grid[r][c] == color:
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    if max_r < 0:
        return None
    return min_r, max_r, min_c, max_c

def get_intervals_on_row(grid: List[List[int]], orig: List[List[int]], row: int, min_c: int, max_c: int, bg: int, ccol: int, h: int) -> List[Tuple[int, int]]:
    intervals = []
    start = None
    for c in range(min_c, max_c + 1):
        if 0 <= row < h and grid[row][c] == ccol and orig[row][c] == bg:
            if start is None:
                start = c
        else:
            if start is not None:
                intervals.append((start, c - 1))
                start = None
    if start is not None:
        intervals.append((start, max_c))
    return intervals

def get_intervals_on_col(grid: List[List[int]], orig: List[List[int]], col: int, min_r: int, max_r: int, bg: int, ccol: int, w: int) -> List[Tuple[int, int]]:
    intervals = []
    start = None
    for r in range(min_r, max_r + 1):
        if 0 <= col < w and grid[r][col] == ccol and orig[r][col] == bg:
            if start is None:
                start = r
        else:
            if start is not None:
                intervals.append((start, r - 1))
                start = None
    if start is not None:
        intervals.append((start, max_r))
    return intervals

def get_new_intervals_and_fill_row(grid: List[List[int]], current_ints: List[Tuple[int, int]], new_row: int, min_c: int, max_c: int, bg: int, ccol: int, h: int, is_first: bool) -> List[Tuple[int, int]]:
    if not current_ints:
        return []
    new_intvs = []
    prop_ranges = set()
    # leftmost
    li = current_ints[0]
    p_l = max(0, li[0] - 1)
    p_r = li[1]
    prop_ranges.add((p_l, p_r))
    # rightmost
    ri = current_ints[-1]
    p_l = ri[0]
    add_r = 0 if is_first else 1
    p_r = min(max_c, ri[1] + add_r)
    prop_ranges.add((p_l, p_r))
    # fill
    for pl, pr in prop_ranges:
        c = max(min_c, pl)
        while c <= min(max_c, pr):
            if 0 <= new_row < h and grid[new_row][c] == bg:
                l_fill = c
                while c <= min(max_c, pr) and 0 <= new_row < h and grid[new_row][c] == bg:
                    grid[new_row][c] = ccol
                    c += 1
                new_intvs.append((l_fill, c - 1))
            else:
                c += 1
    return new_intvs

def get_new_intervals_and_fill_col(grid: List[List[int]], current_ints: List[Tuple[int, int]], new_col: int, min_r: int, max_r: int, bg: int, ccol: int, w: int, is_first: bool) -> List[Tuple[int, int]]:
    if not current_ints:
        return []
    new_intvs = []
    prop_ranges = set()
    # topmost (small r)
    ti = current_ints[0]
    p_s = max(0, ti[0] - 1)
    p_e = ti[1]
    prop_ranges.add((p_s, p_e))
    # bottommost (large r)
    bi = current_ints[-1]
    p_s = bi[0]
    add_e = 0 if is_first else 1
    p_e = min(max_r, bi[1] + add_e)
    prop_ranges.add((p_s, p_e))
    # fill
    for ps, pe in prop_ranges:
        r = max(min_r, ps)
        while r <= min(max_r, pe):
            if 0 <= new_col < w and grid[r][new_col] == bg:
                l_fill = r
                while r <= min(max_r, pe) and 0 <= new_col < w and grid[r][new_col] == bg:
                    grid[r][new_col] = ccol
                    r += 1
                new_intvs.append((l_fill, r - 1))
            else:
                r += 1
    return new_intvs

def detect_open_side(grid: List[List[int]], bg: int, s_color: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int) -> Optional[str]:
    gaps = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}
    # top
    current = 0
    mg = 0
    for c in range(min_c, max_c + 1):
        if grid[min_r][c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['top'] = mg
    # bottom
    current = 0
    mg = 0
    for c in range(min_c, max_c + 1):
        if grid[max_r][c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['bottom'] = mg
    # left
    current = 0
    mg = 0
    for r in range(min_r, max_r + 1):
        if grid[r][min_c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['left'] = mg
    # right
    current = 0
    mg = 0
    for r in range(min_r, max_r + 1):
        if grid[r][max_c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['right'] = mg
    max_g = max(gaps.values())
    if max_g < 3:
        return None
    for s in ['bottom', 'top', 'left', 'right']:
        if gaps[s] == max_g:
            return s
    return None

def expand_in_direction(work: List[List[int]], side: str, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int, bg: int, c_color: int, original_g: List[List[int]]):
    if side == 'bottom':
        intervals = get_intervals_on_row(work, original_g, max_r, min_c, max_c, bg, c_color, h)
        if not intervals:
            return
        current_intervals = sorted(intervals)
        for delta in range(1, h - max_r):
            new_row = max_r + delta
            if new_row >= h:
                break
            new_intvs = get_new_intervals_and_fill_row(work, current_intervals, new_row, 0, w - 1, bg, c_color, h, delta == 1)
            current_intervals = sorted(new_intvs)
            if not current_intervals:
                break
    elif side == 'top':
        intervals = get_intervals_on_row(work, original_g, min_r, min_c, max_c, bg, c_color, h)
        if not intervals:
            return
        current_intervals = sorted(intervals)
        for delta in range(1, min_r + 1):
            new_row = min_r - delta
            if new_row < 0:
                break
            new_intvs = get_new_intervals_and_fill_row(work, current_intervals[::-1], new_row, 0, w - 1, bg, c_color, h, delta == 1)  # reverse for small index
            current_intervals = sorted(new_intvs[::-1])
            if not current_intervals:
                break
    elif side == 'left':
        intervals = get_intervals_on_col(work, original_g, min_c, min_r, max_r, bg, c_color, w)
        if not intervals:
            return
        current_intervals = sorted(intervals)
        for delta in range(1, min_c + 1):
            new_col = min_c - delta
            if new_col < 0:
                break
            new_intvs = get_new_intervals_and_fill_col(work, current_intervals, new_col, 0, h - 1, bg, c_color, w, delta == 1)
            current_intervals = sorted(new_intvs)
            if not current_intervals:
                break
    elif side == 'right':
        intervals = get_intervals_on_col(work, original_g, max_c, min_r, max_r, bg, c_color, w)
        if not intervals:
            return
        current_intervals = sorted(intervals)
        for delta in range(1, w - max_c):
            new_col = max_c + delta
            if new_col >= w:
                break
            new_intvs = get_new_intervals_and_fill_col(work, current_intervals[::-1], new_col, 0, h - 1, bg, c_color, w, delta == 1)
            current_intervals = sorted(new_intvs[::-1])
            if not current_intervals:
                break

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    work = deepcopy(g)
    bg = get_background(work)
    non_bg_freq = get_freq_non_bg(work, bg)
    if not non_bg_freq:
        return work
    s_color = max(non_bg_freq, key=non_bg_freq.get)
    bbox = get_bbox_for_color(work, s_color, h, w)
    if bbox is None:
        return work
    min_r, max_r, min_c, max_c = bbox
    # candidate seeds
    candidates = {}
    for color, count in non_bg_freq.items():
        if color == bg or color == s_color:
            continue
        has_inside = any(min_r <= r <= max_r and min_c <= c <= max_c and work[r][c] == color for r in range(h) for c in range(w))
        if has_inside:
            candidates[color] = count
    if not candidates:
        return work
    c_color = min(candidates, key=candidates.get)
    # internal fill
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for c in range(w):
            if work[r][c] == c_color and min_r <= r <= max_r and min_c <= c <= max_c and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (min_r <= nr <= max_r and min_c <= nc <= max_c and 0 <= nr < h and 0 <= nc < w and
                not visited[nr][nc] and work[nr][nc] == bg):
                work[nr][nc] = c_color
                visited[nr][nc] = True
                q.append((nr, nc))
    # detect open side
    open_side = detect_open_side(work, bg, s_color, min_r, max_r, min_c, max_c, h, w)
    if open_side:
        expand_in_direction(work, open_side, min_r, max_r, min_c, max_c, h, w, bg, c_color, g)
    return work
```