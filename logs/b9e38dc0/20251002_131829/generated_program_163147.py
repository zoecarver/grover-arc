```python
from collections import deque, Counter, defaultdict
from copy import deepcopy
from typing import List, Tuple

def is_border_connected(grid: List[List[int]], color: int, h: int, w: int) -> bool:
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r in range(h):
        for c in [0, w - 1]:
            if grid[r][c] == color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
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
    candidates = []
    for color in counter:
        if is_border_connected(grid, color, h, w):
            candidates.append((counter[color], color))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return 0

def get_non_bg_components(grid: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    h = len(grid)
    if h == 0:
        return []
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if grid[i][j] != bg and not visited[i][j]:
                color = grid[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == color and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if component:
                    components.append((color, component))
    return components

def compute_gaps(side: str, min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int, structure_color: int) -> int:
    h, w = len(g), len(g[0])
    maxg = 0
    if side == 'top':
        r = min_r
        if 0 <= r < h:
            current = 0
            for c in range(min_c, max_c + 1):
                if g[r][c] == structure_color:
                    current = 0
                else:
                    current += 1
                    maxg = max(maxg, current)
    elif side == 'bottom':
        r = max_r
        if 0 <= r < h:
            current = 0
            for c in range(min_c, max_c + 1):
                if g[r][c] == structure_color:
                    current = 0
                else:
                    current += 1
                    maxg = max(maxg, current)
    elif side == 'left':
        c = min_c
        if 0 <= c < w:
            current = 0
            for r in range(min_r, max_r + 1):
                if g[r][c] == structure_color:
                    current = 0
                else:
                    current += 1
                    maxg = max(maxg, current)
    elif side == 'right':
        c = max_c
        if 0 <= c < w:
            current = 0
            for r in range(min_r, max_r + 1):
                if g[r][c] == structure_color:
                    current = 0
                else:
                    current += 1
                    maxg = max(maxg, current)
    return maxg

def has_contain_in_main_gap(side: str, min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int, structure_color: int, seed_center_r: float, seed_center_c: float, maxg: int) -> bool:
    if maxg <= 1:
        return False
    h, w = len(g), len(g[0])
    if side == 'top' or side == 'bottom':
        r = min_r if side == 'top' else max_r
        if not (0 <= r < h):
            return False
        current = 0
        for c in range(min_c, max_c + 2):
            is_bg = c <= max_c and g[r][c] == bg
            if is_bg:
                current += 1
            else:
                if current == maxg:
                    gap_start = c - current
                    gap_end = c - 1
                    if gap_start <= seed_center_c <= gap_end:
                        return True
                current = 0
        if current == maxg:
            gap_start = max_c - current + 1
            gap_end = max_c
            if gap_start <= seed_center_c <= gap_end:
                return True
    else:  # left or right
        c = min_c if side == 'left' else max_c
        if not (0 <= c < w):
            return False
        current = 0
        for r in range(min_r, max_r + 2):
            is_bg = r <= max_r and g[r][c] == bg
            if is_bg:
                current += 1
            else:
                if current == maxg:
                    gap_start = r - current
                    gap_end = r - 1
                    if gap_start <= seed_center_r <= gap_end:
                        return True
                current = 0
        if current == maxg:
            gap_start = max_r - current + 1
            gap_end = max_r
            if gap_start <= seed_center_r <= gap_end:
                return True
    return False

def detect_open_side(min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int, structure_color: int, seed_center_r: float, seed_center_c: float) -> str or None:
    gaps = {
        'top': compute_gaps('top', min_r, max_r, min_c, max_c, g, bg, structure_color),
        'bottom': compute_gaps('bottom', min_r, max_r, min_c, max_c, g, bg, structure_color),
        'left': compute_gaps('left', min_r, max_r, min_c, max_c, g, bg, structure_color),
        'right': compute_gaps('right', min_r, max_r, min_c, max_c, g, bg, structure_color)
    }
    max_gap = max(gaps.values())
    if max_gap <= 1:
        return None
    candidates = [s for s in gaps if gaps[s] == max_gap]
    preferred = []
    for s in candidates:
        if has_contain_in_main_gap(s, min_r, max_r, min_c, max_c, g, bg, structure_color, seed_center_r, seed_center_c, max_gap):
            preferred.append(s)
    if preferred:
        return preferred[0]
    if 'bottom' in candidates:
        return 'bottom'
    return candidates[0]

def expand_bottom(out: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int, structure_color: int, seed_color: int, gaps_intervals: List[Tuple[int, int]]):
    permanent_gaps = set()
    k = 1
    current_r = max_r + 1
    h, w = len(g), len(g[0])
    while current_r < h:
        this_row_filled = False
        for start, end in gaps_intervals:
            new_start = max(0, start - k)
            new_end = min(w - 1, end + k)
            for c in range(new_start, new_end + 1):
                if c in permanent_gaps:
                    continue
                if g[current_r][c] == bg:
                    out[current_r][c] = seed_color
                    this_row_filled = True
        for c in range(0, w):
            if g[current_r][c] == structure_color:
                permanent_gaps.add(c)
        if not this_row_filled:
            break
        k += 1
        current_r += 1

def get_gaps_intervals_horizontal(side: str, min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int) -> List[Tuple[int, int]]:
    r = min_r if side == 'top' else max_r
    intervals = []
    i = min_c
    while i <= max_c:
        if g[r][i] != bg:
            i += 1
            continue
        start = i
        i += 1
        while i <= max_c and g[r][i] == bg:
            i += 1
        end = i - 1
        intervals.append((start, end))
    return intervals

def expand_top(out: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int, structure_color: int, seed_color: int, gaps_intervals: List[Tuple[int, int]]):
    permanent_gaps = set()
    k = 1
    current_r = min_r - 1
    h, w = len(g), len(g[0])
    while current_r >= 0:
        this_row_filled = False
        for start, end in gaps_intervals:
            new_start = max(0, start - k)
            new_end = min(w - 1, end + k)
            for c in range(new_start, new_end + 1):
                if c in permanent_gaps:
                    continue
                if g[current_r][c] == bg:
                    out[current_r][c] = seed_color
                    this_row_filled = True
        for c in range(0, w):
            if g[current_r][c] == structure_color:
                permanent_gaps.add(c)
        if not this_row_filled:
            break
        k += 1
        current_r -= 1

def get_gaps_intervals_vertical(side: str, min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int) -> List[Tuple[int, int]]:
    c = min_c if side == 'left' else max_c
    intervals = []
    i = min_r
    while i <= max_r:
        if g[i][c] != bg:
            i += 1
            continue
        start = i
        i += 1
        while i <= max_r and g[i][c] == bg:
            i += 1
        end = i - 1
        intervals.append((start, end))
    return intervals

def expand_left(out: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int, structure_color: int, seed_color: int, gaps_intervals: List[Tuple[int, int]]):
    permanent_gaps = set()
    k = 1
    current_c = min_c - 1
    h, w = len(g), len(g[0])
    while current_c >= 0:
        this_col_filled = False
        for start, end in gaps_intervals:
            new_start = max(0, start - k)
            new_end = min(h - 1, end + k)
            for r in range(new_start, new_end + 1):
                if r in permanent_gaps:
                    continue
                if g[r][current_c] == bg:
                    out[r][current_c] = seed_color
                    this_col_filled = True
        for r in range(0, h):
            if g[r][current_c] == structure_color:
                permanent_gaps.add(r)
        if not this_col_filled:
            break
        k += 1
        current_c -= 1

def expand_right(out: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int, structure_color: int, seed_color: int, gaps_intervals: List[Tuple[int, int]]):
    permanent_gaps = set()
    k = 1
    current_c = max_c + 1
    h, w = len(g), len(g[0])
    while current_c < w:
        this_col_filled = False
        for start, end in gaps_intervals:
            new_start = max(0, start - k)
            new_end = min(h - 1, end + k)
            for r in range(new_start, new_end + 1):
                if r in permanent_gaps:
                    continue
                if g[r][current_c] == bg:
                    out[r][current_c] = seed_color
                    this_col_filled = True
        for r in range(0, h):
            if g[r][current_c] == structure_color:
                permanent_gaps.add(r)
        if not this_col_filled:
            break
        k += 1
        current_c += 1

def fill_open_edge(out: List[List[int]], open_side: str, min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int, seed_color: int):
    h, w = len(g), len(g[0])
    if open_side == 'top':
        r = min_r
        for c in range(min_c, max_c + 1):
            if 0 <= r < h and g[r][c] == bg:
                out[r][c] = seed_color
    elif open_side == 'bottom':
        r = max_r
        for c in range(min_c, max_c + 1):
            if 0 <= r < h and g[r][c] == bg:
                out[r][c] = seed_color
    elif open_side == 'left':
        c = min_c
        for r in range(min_r, max_r + 1):
            if 0 <= r < h and g[r][c] == bg:
                out[r][c] = seed_color
    elif open_side == 'right':
        c = max_c
        for r in range(min_r, max_r + 1):
            if 0 <= r < h and g[r][c] == bg:
                out[r][c] = seed_color

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    bg = get_background(g)
    components = get_non_bg_components(g, bg)
    comp_by_color = defaultdict(list)
    total = Counter()
    for color, comp in components:
        comp_by_color[color].append(comp)
        total[color] += len(comp)
    if not total:
        return deepcopy(g)
    structure_color = max(total, key=total.get)
    structure_comps = comp_by_color[structure_color]
    all_rs = []
    all_cs = []
    for comp in structure_comps:
        for p in comp:
            all_rs.append(p[0])
            all_cs.append(p[1])
    if not all_rs:
        return deepcopy(g)
    union_min_r = min(all_rs)
    union_max_r = max(all_rs)
    union_min_c = min(all_cs)
    union_max_c = max(all_cs)
    seed_candidates = []
    for color in total:
        if color == structure_color or color == bg:
            continue
        for comp in comp_by_color[color]:
            comp_rs = [p[0] for p in comp]
            comp_cs = [p[1] for p in comp]
            if not comp_rs:
                continue
            c_min_r = min(comp_rs)
            c_max_r = max(comp_rs)
            c_min_c = min(comp_cs)
            c_max_c = max(comp_cs)
            if c_max_r < union_min_r or c_min_r > union_max_r or c_max_c < union_min_c or c_min_c > union_max_c:
                continue
            seed_candidates.append((total[color], color))
            break  # at least one comp overlaps
    if not seed_candidates:
        return deepcopy(g)
    seed_candidates.sort()
    _, seed_color = seed_candidates[0]
    # seed center
    seed_cells = []
    for comp in comp_by_color[seed_color]:
        seed_cells.extend(comp)
    if seed_cells:
        seed_center_r = sum(p[0] for p in seed_cells) / len(seed_cells)
        seed_center_c = sum(p[1] for p in seed_cells) / len(seed_cells)
    else:
        seed_center_r = (union_min_r + union_max_r) / 2
        seed_center_c = (union_min_c + union_max_c) / 2
    out = deepcopy(g)
    h, w = len(g), len(g[0])
    open_side = detect_open_side(union_min_r, union_max_r, union_min_c, union_max_c, g, bg, structure_color, seed_center_r, seed_center_c)
    # internal fill
    visited = [[False] * w for _ in range(h)]
    q = deque()
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # seed closed sides all bg
    closed_sides = ['top', 'bottom', 'left', 'right']
    if open_side:
        closed_sides.remove(open_side)
    for side in closed_sides:
        if side == 'top':
            r = union_min_r
            for c in range(union_min_c, union_max_c + 1):
                if 0 <= r < h and 0 <= c < w and g[r][c] == bg and not visited[r][c]:
                    q.append((r, c))
                    visited[r][c] = True
        elif side == 'bottom':
            r = union_max_r
            for c in range(union_min_c, union_max_c + 1):
                if 0 <= r < h and 0 <= c < w and g[r][c] == bg and not visited[r][c]:
                    q.append((r, c))
                    visited[r][c] = True
        elif side == 'left':
            c = union_min_c
            for r in range(union_min_r, union_max_r + 1):
                if 0 <= r < h and 0 <= c < w and g[r][c] == bg and not visited[r][c]:
                    q.append((r, c))
                    visited[r][c] = True
        elif side == 'right':
            c = union_max_c
            for r in range(union_min_r, union_max_r + 1):
                if 0 <= r < h and 0 <= c < w and g[r][c] == bg and not visited[r][c]:
                    q.append((r, c))
                    visited[r][c] = True
    # flood within union bbox
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc
            if (union_min_r <= nr <= union_max_r and union_min_c <= nc <= union_max_c and
                0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] == bg):
                visited[nr][nc] = True
                q.append((nr, nc))
    # fill unmarked bg in union bbox
    for rr in range(union_min_r, union_max_r + 1):
        for cc in range(union_min_c, union_max_c + 1):
            if 0 <= rr < h and 0 <= cc < w and g[rr][cc] == bg and not visited[rr][cc]:
                out[rr][cc] = seed_color
    # fill open edge after
    if open_side:
        fill_open_edge(out, open_side, union_min_r, union_max_r, union_min_c, union_max_c, g, bg, seed_color)
    # expansion if open_side
    if open_side:
        if open_side == 'bottom':
            gaps_intervals = get_gaps_intervals_horizontal('bottom', union_min_r, union_max_r, union_min_c, union_max_c, g, bg)
            expand_bottom(out, union_min_r, union_max_r, union_min_c, union_max_c, g, bg, structure_color, seed_color, gaps_intervals)
        elif open_side == 'top':
            gaps_intervals = get_gaps_intervals_horizontal('top', union_min_r, union_max_r, union_min_c, union_max_c, g, bg)
            expand_top(out, union_min_r, union_max_r, union_min_c, union_max_c, g, bg, structure_color, seed_color, gaps_intervals)
        elif open_side == 'left':
            gaps_intervals = get_gaps_intervals_vertical('left', union_min_r, union_max_r, union_min_c, union_max_c, g, bg)
            expand_left(out, union_min_r, union_max_r, union_min_c, union_max_c, g, bg, structure_color, seed_color, gaps_intervals)
        elif open_side == 'right':
            gaps_intervals = get_gaps_intervals_vertical('right', union_min_r, union_max_r, union_min_c, union_max_c, g, bg)
            expand_right(out, union_min_r, union_max_r, union_min_c, union_max_c, g, bg, structure_color, seed_color, gaps_intervals)
    return out
```