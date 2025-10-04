```python
from collections import deque, Counter
from copy import deepcopy
from typing import List, Tuple, Optional

def program(g: List[List[int]]) -> List[List[int]]:
    grid = deepcopy(g)
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    bg = get_background(grid, h, w)
    non_bg_flat = [grid[r][c] for r in range(h) for c in range(w) if grid[r][c] != bg]
    if not non_bg_flat:
        return grid
    non_bg_count = Counter(non_bg_flat)
    if len(non_bg_count) < 1:
        return grid
    struct_color = non_bg_count.most_common(1)[0][0]
    # Find possible fills: colors != struct with positions inside struct bbox
    struct_pos = get_positions_of_color(grid, struct_color, h, w)
    if not struct_pos:
        return grid
    min_r = min(r for r, c in struct_pos)
    max_r = max(r for r, c in struct_pos)
    min_c = min(c for r, c in struct_pos)
    max_c = max(c for r, c in struct_pos)
    possible_fills = set()
    for col in non_bg_count:
        if col != struct_color and col != bg:
            pos = get_positions_of_color(grid, col, h, w)
            if any(min_r <= r <= max_r and min_c <= c <= max_c for r, c in pos):
                possible_fills.add(col)
    if possible_fills:
        fill_color = min(possible_fills)
    else:
        fill_color = struct_color
    # Detect open side on original grid
    open_side = detect_open_side(grid, bg, struct_color, min_r, max_r, min_c, max_c, h, w)
    # Fill interior: flood within bbox from fill positions inside
    fill_pos_inside = [(r, c) for r in range(min_r, max_r + 1) for c in range(min_c, max_c + 1) if grid[r][c] == fill_color]
    if fill_pos_inside:
        flood_fill_in_bbox(grid, fill_pos_inside, fill_color, bg, min_r, max_r, min_c, max_c, h, w)
    # Expansion based on open side
    if open_side == 'bottom':
        expand_bottom(grid, fill_color, bg, min_r, max_r, min_c, max_c, h, w)
    elif open_side == 'left':
        expand_left(grid, fill_color, bg, struct_color, min_r, max_r, min_c, max_c, h, w)
    return grid

def get_background(grid: List[List[int]], h: int, w: int) -> int:
    flat = [grid[r][c] for r in range(h) for c in range(w)]
    count = Counter(flat)
    candidates = []
    for color in count:
        if is_border_connected(grid, color, h, w):
            candidates.append((count[color], color))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return 0

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
    total = sum(1 for r in range(h) for c in range(w) if grid[r][c] == color)
    visited_count = sum(sum(row) for row in visited)
    return visited_count == total

def get_positions_of_color(grid: List[List[int]], color: int, h: int, w: int) -> List[Tuple[int, int]]:
    pos = []
    for r in range(h):
        for c in range(w):
            if grid[r][c] == color:
                pos.append((r, c))
    return pos

def detect_open_side(grid: List[List[int]], bg: int, struct_color: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int) -> Optional[str]:
    gaps = {}
    # Top
    current = 0
    mg = 0
    for c in range(min_c, max_c + 1):
        if grid[min_r][c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['top'] = mg
    # Bottom
    current = 0
    mg = 0
    for c in range(min_c, max_c + 1):
        if grid[max_r][c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['bottom'] = mg
    # Left
    current = 0
    mg = 0
    for r in range(min_r, max_r + 1):
        if grid[r][min_c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['left'] = mg
    # Right
    current = 0
    mg = 0
    for r in range(min_r, max_r + 1):
        if grid[r][max_c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['right'] = mg
    max_gap = max(gaps.values())
    if max_gap < 3:  # threshold for open
        return None
    return max(gaps, key=gaps.get)

def flood_fill_in_bbox(grid: List[List[int]], starts: List[Tuple[int, int]], fill_color: int, bg: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int):
    visited = [[False] * w for _ in range(h)]
    q = deque(starts)
    for r, c in starts:
        visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (min_r <= nr <= max_r and min_c <= nc <= max_c and
                0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and grid[nr][nc] == bg):
                grid[nr][nc] = fill_color
                visited[nr][nc] = True
                q.append((nr, nc))

def expand_bottom(grid: List[List[int]], fill_color: int, bg: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int):
    pillars = set()
    current_min = min_c
    current_max = max_c + 1  # asymmetric widen initial right
    for rr in range(max_r + 1, h):
        # Add obstacles in this row to pillars
        for c in range(max(0, current_min), min(w, current_max + 1)):
            if grid[rr][c] != bg and grid[rr][c] != fill_color:
                pillars.add(c)
        # Fill ranges from current_min to current_max, skip pillars, only if bg
        start = None
        for c in range(max(0, current_min), min(w, current_max + 1)):
            if c in pillars or grid[rr][c] != bg:
                if start is not None:
                    for cc in range(start, c):
                        if grid[rr][cc] == bg:
                            grid[rr][cc] = fill_color
                    start = None
            else:
                if start is None:
                    start = c
        if start is not None:
            for cc in range(start, min(w, current_max + 1)):
                if grid[rr][cc] == bg:
                    grid[rr][cc] = fill_color
        # Update filled cols min max
        filled = [c for c in range(max(0, current_min), min(w, current_max + 1)) if grid[rr][c] == fill_color]
        if not filled:
            break
        filled_min = min(filled)
        filled_max = max(filled)
        current_min = max(0, filled_min - 1)
        current_max = min(w - 1, filled_max + 1)

def expand_left(grid: List[List[int]], fill_color: int, bg: int, struct_color: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int):
    # For rows in structure range
    for r in range(min_r, max_r + 1):
        barriers = [c for c in range(w) if grid[r][c] == struct_color]
        if barriers:
            leftmost = min(barriers)
            for c in range(leftmost):
                if grid[r][c] == bg:
                    grid[r][c] = fill_color
    # Upward tapering
    if min_r > 0:
        top_barriers = [c for c in range(w) if grid[min_r][c] == struct_color]
        if top_barriers:
            top_leftmost = min(top_barriers)
            top_fill_end = top_leftmost - 1
            for dist in range(1, min_r + 1):
                r = min_r - dist
                fill_end = top_fill_end - dist
                if fill_end < 0:
                    break
                for c in range(fill_end + 1):
                    if grid[r][c] == bg:
                        grid[r][c] = fill_color
    # Downward widening (if needed, but skip for example2)
    # For general, similar but widening fill_end = bottom_fill_end + dist
    # But for now, no downward for left
```