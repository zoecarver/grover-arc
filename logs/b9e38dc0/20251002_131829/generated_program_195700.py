```python
from typing import List, Tuple, Optional
from collections import deque, Counter

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h = len(g)
    if h == 0:
        return out
    w = len(g[0])
    bg = find_background(g, h, w)
    boundary = find_boundary(g, bg, h, w)
    fill = select_fill_color(g, bg, boundary, h, w)
    boundary_pos = get_all_positions(g, boundary, h, w)
    if not boundary_pos:
        return out
    min_r, max_r, min_c, max_c = get_bbox(boundary_pos)
    seed_pos = get_all_positions(g, fill, h, w)
    internal_flood(out, fill, bg, min_r, max_r, min_c, max_c, h, w, seed_pos)
    open_side = detect_open_side(g, bg, min_r, max_r, min_c, max_c, h, w)
    if open_side == 'bottom':
        expand_bottom(out, g, fill, bg, blocked_cols_for_bottom(g, fill, bg, max_r, h, w), max_r, h, w)
    elif open_side == 'top':
        expand_top(out, g, fill, bg, blocked_cols_for_top(g, fill, bg, min_r, h, w), min_r, h, w)
    elif open_side == 'left':
        expand_left(out, g, fill, bg, blocked_rows_for_left(g, fill, bg, min_c, h, w), min_c, h, w)
    elif open_side == 'right':
        expand_right(out, g, fill, bg, blocked_rows_for_right(g, fill, bg, max_c, h, w), max_c, h, w)
    return out

def find_background(g: List[List[int]], h: int, w: int) -> int:
    flat = [g[i][j] for i in range(h) for j in range(w)]
    count = Counter(flat)
    if not count:
        return 0
    candidates = [(count[color], color) for color in count if is_border_connected(g, color, h, w)]
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return count.most_common(1)[0][0]

def is_border_connected(g: List[List[int]], color: int, h: int, w: int) -> bool:
    if h == 0 or w == 0 or color == 0:
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
    vis_count = sum(1 for ii in range(h) for jj in range(w) if visited[ii][jj])
    return vis_count == total

def find_boundary(g: List[List[int]], bg: int, h: int, w: int) -> int:
    flat = [g[i][j] for i in range(h) for j in range(w) if g[i][j] != bg]
    if not flat:
        return bg
    count = Counter(flat)
    return count.most_common(1)[0][0]

def select_fill_color(g: List[List[int]], bg: int, boundary: int, h: int, w: int) -> int:
    flat = [g[i][j] for i in range(h) for j in range(w)]
    non_bg_count = Counter(c for c in flat if c != bg)
    possible_fills = [c for c in non_bg_count if c != boundary and non_bg_count[c] > 0]
    if not possible_fills:
        return boundary

    def min_dist(color: int) -> float:
        seed_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == color]
        if not seed_pos:
            return float('inf')
        bound_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == boundary]
        if not bound_pos:
            return float('inf')
        return min(abs(si - bi) + abs(sj - bj) for si, sj in seed_pos for bi, bj in bound_pos)

    fill_dists = [(c, min_dist(c), non_bg_count[c]) for c in possible_fills]
    fill_dists.sort(key=lambda x: (x[1], -x[2]))
    return fill_dists[0][0]

def get_all_positions(g: List[List[int]], color: int, h: int, w: int) -> List[Tuple[int, int]]:
    return [(i, j) for i in range(h) for j in range(w) if g[i][j] == color]

def get_bbox(positions: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not positions:
        return 0, h - 1, 0, 0  # dummy, but checked earlier
    min_r = min(r for r, c in positions)
    max_r = max(r for r, c in positions)
    min_c = min(c for r, c in positions)
    max_c = max(c for r, c in positions)
    return min_r, max_r, min_c, max_c

def internal_flood(out: List[List[int]], fill: int, bg: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int, seed_pos: List[Tuple[int, int]]):
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for r, c in seed_pos:
        if min_r <= r <= max_r and min_c <= c <= max_c and not visited[r][c]:
            q.append((r, c))
            visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc
            if min_r <= nr <= max_r and min_c <= nc <= max_c and 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and out[nr][nc] == bg:
                out[nr][nc] = fill
                visited[nr][nc] = True
                q.append((nr, nc))

def detect_open_side(g: List[List[int]], bg: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int) -> Optional[str]:
    gaps = {}
    gaps['top'] = max_consecutive(g[min_r], bg, min_c, max_c)
    gaps['bottom'] = max_consecutive(g[max_r], bg, min_c, max_c)
    gaps['left'] = max_vertical_consecutive(g, bg, min_c, min_r, max_r, h)
    gaps['right'] = max_vertical_consecutive(g, bg, max_c, min_r, max_r, h)
    max_gap = max(gaps.values())
    if max_gap < 2:
        return None
    candidates = [side for side, gap in gaps.items() if gap == max_gap]
    order = ['bottom', 'left', 'top', 'right']
    for pref in order:
        if pref in candidates:
            return pref
    return None

def max_consecutive(row: List[int], bg: int, start: int, end: int) -> int:
    current = 0
    mx = 0
    for j in range(start, end + 1):
        if row[j] == bg:
            current += 1
            mx = max(mx, current)
        else:
            current = 0
    return mx

def max_vertical_consecutive(g: List[List[int]], bg: int, fixed_c: int, start_r: int, end_r: int, h: int) -> int:
    current = 0
    mx = 0
    for i in range(start_r, end_r + 1):
        if g[i][fixed_c] == bg:
            current += 1
            mx = max(mx, current)
        else:
            current = 0
    return mx

def get_intervals(poss: set[int]) -> List[Tuple[int, int]]:
    if not poss:
        return []
    pl = sorted(poss)
    res = []
    st = pl[0]
    en = pl[0]
    for p in pl[1:]:
        if p == en + 1:
            en = p
        else:
            res.append((st, en))
            st = en = p
    res.append((st, en))
    return res

def blocked_cols_for_bottom(g: List[List[int]], fill: int, bg: int, max_r: int, h: int, w: int) -> set[int]:
    blocked = set()
    for c in range(w):
        for r in range(max_r + 1, h):
            if g[r][c] != bg and g[r][c] != fill:
                blocked.add(c)
                break
    return blocked

def expand_bottom(out: List[List[int]], g: List[List[int]], fill: int, bg: int, blocked_cols: set[int], max_r: int, h: int, w: int):
    filled_cols = {c for c in range(w) if out[max_r][c] == fill}
    if not filled_cols:
        return
    current_filled_cols = filled_cols
    for r in range(max_r + 1, h):
        new_filled_cols = set()
        intervals = get_intervals(current_filled_cols)
        for s, e in intervals:
            new_s = s
            if s > 0:
                cand = s - 1
                if cand not in blocked_cols and out[r][cand] == bg:
                    new_s = cand
            new_e = e
            if e < w - 1:
                cand = e + 1
                if cand not in blocked_cols and out[r][cand] == bg:
                    new_e = cand
            for c in range(new_s, new_e + 1):
                if c not in blocked_cols and out[r][c] == bg:
                    out[r][c] = fill
                    new_filled_cols.add(c)
        current_filled_cols = new_filled_cols
        if not current_filled_cols:
            break

def blocked_cols_for_top(g: List[List[int]], fill: int, bg: int, min_r: int, h: int, w: int) -> set[int]:
    blocked = set()
    for c in range(w):
        for r in range(min_r):
            if g[r][c] != bg and g[r][c] != fill:
                blocked.add(c)
                break
    return blocked

def expand_top(out: List[List[int]], g: List[List[int]], fill: int, bg: int, blocked_cols: set[int], min_r: int, h: int, w: int):
    filled_cols = {c for c in range(w) if out[min_r][c] == fill}
    if not filled_cols:
        return
    current_filled_cols = filled_cols
    for r in range(min_r - 1, -1, -1):
        new_filled_cols = set()
        intervals = get_intervals(current_filled_cols)
        for s, e in intervals:
            new_s = s
            if s > 0:
                cand = s - 1
                if cand not in blocked_cols and out[r][cand] == bg:
                    new_s = cand
            new_e = e
            if e < w - 1:
                cand = e + 1
                if cand not in blocked_cols and out[r][cand] == bg:
                    new_e = cand
            for c in range(new_s, new_e + 1):
                if c not in blocked_cols and out[r][c] == bg:
                    out[r][c] = fill
                    new_filled_cols.add(c)
        current_filled_cols = new_filled_cols
        if not current_filled_cols:
            break

def blocked_rows_for_left(g: List[List[int]], fill: int, bg: int, min_c: int, h: int, w: int) -> set[int]:
    blocked = set()
    for r in range(h):
        for c in range(min_c):
            if g[r][c] != bg and g[r][c] != fill:
                blocked.add(r)
                break
    return blocked

def expand_left(out: List[List[int]], g: List[List[int]], fill: int, bg: int, blocked_rows: set[int], min_c: int, h: int, w: int):
    filled_rows = {r for r in range(h) if out[r][min_c] == fill}
    if not filled_rows:
        return
    current_filled_rows = filled_rows
    for c in range(min_c - 1, -1, -1):
        new_filled_rows = set()
        intervals = get_intervals(current_filled_rows)
        for s, e in intervals:
            new_s = s
            if s > 0:
                cand = s - 1
                if cand not in blocked_rows and out[cand][c] == bg:
                    new_s = cand
            new_e = e
            if e < h - 1:
                cand = e + 1
                if cand not in blocked_rows and out[cand][c] == bg:
                    new_e = cand
            for r in range(new_s, new_e + 1):
                if r not in blocked_rows and out[r][c] == bg:
                    out[r][c] = fill
                    new_filled_rows.add(r)
        current_filled_rows = new_filled_rows
        if not current_filled_rows:
            break

def blocked_rows_for_right(g: List[List[int]], fill: int, bg: int, max_c: int, h: int, w: int) -> set[int]:
    blocked = set()
    for r in range(h):
        for c in range(max_c + 1, w):
            if g[r][c] != bg and g[r][c] != fill:
                blocked.add(r)
                break
    return blocked

def expand_right(out: List[List[int]], g: List[List[int]], fill: int, bg: int, blocked_rows: set[int], max_c: int, h: int, w: int):
    filled_rows = {r for r in range(h) if out[r][max_c] == fill}
    if not filled_rows:
        return
    current_filled_rows = filled_rows
    for c in range(max_c + 1, w):
        new_filled_rows = set()
        intervals = get_intervals(current_filled_rows)
        for s, e in intervals:
            new_s = s
            if s > 0:
                cand = s - 1
                if cand not in blocked_rows and out[cand][c] == bg:
                    new_s = cand
            new_e = e
            if e < h - 1:
                cand = e + 1
                if cand not in blocked_rows and out[cand][c] == bg:
                    new_e = cand
            for r in range(new_s, new_e + 1):
                if r not in blocked_rows and out[r][c] == bg:
                    out[r][c] = fill
                    new_filled_rows.add(r)
        current_filled_rows = new_filled_rows
        if not current_filled_rows:
            break
```