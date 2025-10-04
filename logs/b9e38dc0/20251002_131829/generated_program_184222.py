```python
from typing import List, Tuple, Optional
from collections import Counter, deque
import copy

def is_border_connected(g: List[List[int]], color: int, h: int, w: int) -> bool:
    if color == 0 or h == 0 or w == 0:
        return False
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for i in range(h):
        for j in (0, w - 1):
            if g[i][j] == color and not visited[i][j]:
                q.append((i, j))
                visited[i][j] = True
    for j in range(w):
        for i in (0, h - 1):
            if g[i][j] == color and not visited[i][j]:
                q.append((i, j))
                visited[i][j] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        i, j = q.popleft()
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and g[ni][nj] == color:
                visited[ni][nj] = True
                q.append((ni, nj))
    total = sum(1 for ii in range(h) for jj in range(w) if g[ii][jj] == color)
    vis_cnt = sum(1 for ii in range(h) for jj in range(w) if visited[ii][jj])
    return vis_cnt == total

def find_background(g: List[List[int]]) -> int:
    h = len(g)
    if h == 0:
        return 0
    w = len(g[0])
    flat = [g[i][j] for i in range(h) for j in range(w)]
    count = Counter(flat)
    if not count:
        return 0
    candidates = []
    for color in count:
        if is_border_connected(g, color, h, w):
            candidates.append((count[color], color))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return count.most_common(1)[0][0]

def get_structure_color(g: List[List[int]], bg: int) -> int:
    count = Counter(cell for row in g for cell in row if cell != bg)
    if not count:
        return bg
    return count.most_common(1)[0][0]

def get_all_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    h, w = len(g), len(g[0])
    return [(i, j) for i in range(h) for j in range(w) if g[i][j] == color]

def get_bbox(positions: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not positions:
        return 0, 0, 0, 0
    min_r = min(p[0] for p in positions)
    max_r = max(p[0] for p in positions)
    min_c = min(p[1] for p in positions)
    max_c = max(p[1] for p in positions)
    return min_r, max_r, min_c, max_c

def select_fill_color(g: List[List[int]], bg: int, structure: int, min_r: int, max_r: int, min_c: int, max_c: int) -> Optional[int]:
    h, w = len(g), len(g[0])
    inside_colors = Counter()
    for i in range(max(0, min_r), min(h, max_r + 1)):
        for j in range(max(0, min_c), min(w, max_c + 1)):
            c = g[i][j]
            if c != bg and c != structure:
                inside_colors[c] += 1
    if not inside_colors:
        return None
    max_cnt = inside_colors.most_common(1)[0][1]
    candidates = [c for c, cnt in inside_colors.items() if cnt == max_cnt]
    return min(candidates)

def get_seed_positions(g: List[List[int]], fill_color: int, min_r: int, max_r: int, min_c: int, max_c: int) -> List[Tuple[int, int]]:
    h, w = len(g), len(g[0])
    pos = []
    for i in range(max(0, min_r), min(h, max_r + 1)):
        for j in range(max(0, min_c), min(w, max_c + 1)):
            if g[i][j] == fill_color:
                pos.append((i, j))
    return pos

def internal_flood(g: List[List[int]], seed_pos: List[Tuple[int, int]], fill_color: int, bg: int, min_r: int, max_r: int, min_c: int, max_c: int):
    h, w = len(g), len(g[0])
    if not seed_pos:
        return
    visited = [[False] * w for _ in range(h)]
    q = deque(seed_pos)
    for r, c in seed_pos:
        visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (min_r <= nr <= max_r and min_c <= nc <= max_c and
                0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] == bg):
                g[nr][nc] = fill_color
                visited[nr][nc] = True
                q.append((nr, nc))

def get_intervals(pos_set: set) -> List[Tuple[int, int]]:
    if not pos_set:
        return []
    pl = sorted(pos_set)
    intervals = []
    start = pl[0]
    end = pl[0]
    for p in pl[1:]:
        if p == end + 1:
            end = p
        else:
            intervals.append((start, end))
            start = end = p
    intervals.append((start, end))
    return intervals

def compute_max_gap_and_main_interval(g: List[List[int]], structure: int, side: str, min_r: int, max_r: int, min_c: int, max_c: int) -> Tuple[int, Tuple[int, int]]:
    h, w = len(g), len(g[0])
    gaps = []
    if side in ('top', 'bottom'):
        row = min_r if side == 'top' else max_r
        current_start = None
        for j in range(min_c, max_c + 1):
            if g[row][j] != structure:
                if current_start is None:
                    current_start = j
            else:
                if current_start is not None:
                    gaps.append((current_start, j - 1))
                    current_start = None
        if current_start is not None:
            gaps.append((current_start, max_c))
    else:
        col = min_c if side == 'left' else max_c
        current_start = None
        for i in range(min_r, max_r + 1):
            if g[i][col] != structure:
                if current_start is None:
                    current_start = i
            else:
                if current_start is not None:
                    gaps.append((current_start, i - 1))
                    current_start = None
        if current_start is not None:
            gaps.append((current_start, max_r))
    if not gaps:
        return 0, None
    gap_lengths = [(e - s + 1, (s, e)) for s, e in gaps]
    max_len = max(l for l, _ in gap_lengths)
    main = max((inter for l, inter in gap_lengths if l == max_len), key=lambda x: x[1] - x[0] + 1)[1]
    return max_len, main

def detect_open_side(g: List[List[int]], structure: int, min_r: int, max_r: int, min_c: int, max_c: int, seed_center_r: float, seed_center_c: float) -> Optional[str]:
    sides = ['top', 'bottom', 'left', 'right']
    gaps = {}
    mains = {}
    for side in sides:
        mg, main = compute_max_gap_and_main_interval(g, structure, side, min_r, max_r, min_c, max_c)
        gaps[side] = mg
        mains[side] = main
    overall_max = max(gaps.values()) if gaps else 0
    if overall_max < 3:
        return None
    candidates = [s for s in sides if gaps[s] == overall_max]
    preferred = None
    for s in candidates:
        main_int = mains[s]
        if main_int is None:
            continue
        s_start, s_end = main_int
        if s in ('top', 'bottom'):
            proj = seed_center_c
            if s_start <= proj <= s_end:
                preferred = s
                break
        else:
            proj = seed_center_r
            if s_start <= proj <= s_end:
                preferred = s
                break
    if preferred:
        return preferred
    if 'bottom' in candidates:
        return 'bottom'
    return candidates[0] if candidates else None

def expand_bottom(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, fill_color: int, bg: int):
    h, w = len(g), len(g[0])
    prev_filled = {j for j in range(w) if g[max_r][j] == fill_color}
    current_row = max_r + 1
    while current_row < h:
        if not prev_filled:
            break
        intervals = get_intervals(prev_filled)
        potential_js = set()
        for s, e in intervals:
            new_s = max(0, s - 1)
            new_e = min(w - 1, e + 1)
            for j in range(new_s, new_e + 1):
                potential_js.add(j)
        new_filled = set()
        for j in potential_js:
            if g[current_row][j] != bg:
                continue
            clear = True
            for i in range(max_r + 1, current_row):
                cell = g[i][j]
                if cell != bg and cell != fill_color:
                    clear = False
                    break
            if clear:
                g[current_row][j] = fill_color
                new_filled.add(j)
        prev_filled = new_filled
        current_row += 1

def expand_top(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, fill_color: int, bg: int):
    h, w = len(g), len(g[0])
    prev_filled = {j for j in range(w) if g[min_r][j] == fill_color}
    current_row = min_r - 1
    while current_row >= 0:
        if not prev_filled:
            break
        intervals = get_intervals(prev_filled)
        potential_js = set()
        for s, e in intervals:
            new_s = max(0, s - 1)
            new_e = min(w - 1, e + 1)
            for j in range(new_s, new_e + 1):
                potential_js.add(j)
        new_filled = set()
        for j in potential_js:
            if g[current_row][j] != bg:
                continue
            clear = True
            for i in range(current_row + 1, min_r):
                cell = g[i][j]
                if cell != bg and cell != fill_color:
                    clear = False
                    break
            if clear:
                g[current_row][j] = fill_color
                new_filled.add(j)
        prev_filled = new_filled
        current_row -= 1

def expand_left(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, fill_color: int, bg: int):
    h, w = len(g), len(g[0])
    prev_filled = {i for i in range(h) if g[i][min_c] == fill_color}
    current_col = min_c - 1
    while current_col >= 0:
        if not prev_filled:
            break
        intervals = get_intervals(prev_filled)
        potential_is = set()
        for s, e in intervals:
            new_s = max(0, s - 1)
            new_e = min(h - 1, e + 1)
            for i in range(new_s, new_e + 1):
                potential_is.add(i)
        new_filled = set()
        for i in potential_is:
            if g[i][current_col] != bg:
                continue
            clear = True
            for j in range(current_col + 1, min_c):
                cell = g[i][j]
                if cell != bg and cell != fill_color:
                    clear = False
                    break
            if clear:
                g[i][current_col] = fill_color
                new_filled.add(i)
        prev_filled = new_filled
        current_col -= 1

def expand_right(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, fill_color: int, bg: int):
    h, w = len(g), len(g[0])
    prev_filled = {i for i in range(h) if g[i][max_c] == fill_color}
    current_col = max_c + 1
    while current_col < w:
        if not prev_filled:
            break
        intervals = get_intervals(prev_filled)
        potential_is = set()
        for s, e in intervals:
            new_s = max(0, s - 1)
            new_e = min(h - 1, e + 1)
            for i in range(new_s, new_e + 1):
                potential_is.add(i)
        new_filled = set()
        for i in potential_is:
            if g[i][current_col] != bg:
                continue
            clear = True
            for j in range(max_c + 1, current_col):
                cell = g[i][j]
                if cell != bg and cell != fill_color:
                    clear = False
                    break
            if clear:
                g[i][current_col] = fill_color
                new_filled.add(i)
        prev_filled = new_filled
        current_col += 1

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy.deepcopy(g)
    h = len(out)
    if h == 0:
        return out
    w = len(out[0])
    bg = find_background(out)
    structure_color = get_structure_color(out, bg)
    if structure_color == bg:
        return out
    struct_pos = get_all_positions(out, structure_color)
    if not struct_pos:
        return out
    min_r, max_r, min_c, max_c = get_bbox(struct_pos)
    fill_color = select_fill_color(out, bg, structure_color, min_r, max_r, min_c, max_c)
    if fill_color is None or fill_color == bg or fill_color == structure_color:
        return out
    seed_pos = get_seed_positions(out, fill_color, min_r, max_r, min_c, max_c)
    if not seed_pos:
        return out
    avg_r = sum(r for r, _ in seed_pos) / len(seed_pos)
    avg_c = sum(c for _, c in seed_pos) / len(seed_pos)
    internal_flood(out, seed_pos, fill_color, bg, min_r, max_r, min_c, max_c)
    open_side = detect_open_side(out, structure_color, min_r, max_r, min_c, max_c, avg_r, avg_c)
    if open_side == 'bottom':
        expand_bottom(out, min_r, max_r, min_c, max_c, fill_color, bg)
    elif open_side == 'top':
        expand_top(out, min_r, max_r, min_c, max_c, fill_color, bg)
    elif open_side == 'left':
        expand_left(out, min_r, max_r, min_c, max_c, fill_color, bg)
    elif open_side == 'right':
        expand_right(out, min_r, max_r, min_c, max_c, fill_color, bg)
    return out
```