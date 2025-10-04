```python
from typing import List, Tuple
from collections import Counter, deque
from copy import deepcopy
import math

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h = len(out)
    if h == 0:
        return out
    w = len(out[0])
    bg = find_background(g, h, w)
    boundary = get_boundary(g, bg, h, w)
    fill = select_fill_color(g, bg, boundary, h, w)
    boundary_pos = get_all_positions(g, boundary, h, w)
    if not boundary_pos:
        return out
    min_r, max_r, min_c, max_c = get_bbox(boundary_pos)
    seed_pos = get_all_positions(g, fill, h, w)
    internal_flood(out, seed_pos, fill, bg, min_r, max_r, min_c, max_c, h, w)
    open_side = detect_open_side(g, bg, boundary, min_r, max_r, min_c, max_c, h, w)
    if open_side == 'bottom':
        expand_bottom(out, g, fill, bg, min_r, max_r, min_c, max_c, h, w)
    elif open_side == 'top':
        expand_top(out, g, fill, bg, min_r, max_r, min_c, max_c, h, w)
    elif open_side == 'left':
        expand_left(out, g, fill, bg, boundary, min_r, max_r, min_c, max_c, h, w)
    elif open_side == 'right':
        expand_right(out, g, fill, bg, boundary, min_r, max_r, min_c, max_c, h, w)
    return out

def find_background(g: List[List[int]], h: int, w: int) -> int:
    flat = [g[i][j] for i in range(h) for j in range(w)]
    count = Counter(flat)
    if not count:
        return 0
    candidates = []
    for color in count:
        if is_border_connected(g, color, h, w):
            candidates.append((count[color], color))
    if candidates:
        candidates.sort(reverse=True, key=lambda x: x[0])
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

def get_boundary(g: List[List[int]], bg: int, h: int, w: int) -> int:
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

    def min_dist(color):
        seed_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == color]
        if not seed_pos:
            return math.inf
        bound_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == boundary]
        if not bound_pos:
            return math.inf
        return min(abs(si - bi) + abs(sj - bj) for si, sj in seed_pos for bi, bj in bound_pos)

    fill_dists = [(c, min_dist(c), non_bg_count[c]) for c in possible_fills]
    fill_dists.sort(key=lambda x: (x[1], -x[2]))
    return fill_dists[0][0]

def get_all_positions(g: List[List[int]], color: int, h: int, w: int) -> List[Tuple[int, int]]:
    return [(i, j) for i in range(h) for j in range(w) if g[i][j] == color]

def get_bbox(positions: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not positions:
        return 0, 0, 0, 0
    min_r = min(i for i, _ in positions)
    max_r = max(i for i, _ in positions)
    min_c = min(j for _, j in positions)
    max_c = max(j for _, j in positions)
    return min_r, max_r, min_c, max_c

def internal_flood(out: List[List[int]], seed_pos: List[Tuple[int, int]], fill: int, bg: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int):
    if not seed_pos:
        return
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for i, j in seed_pos:
        if min_r <= i <= max_r and min_c <= j <= max_c:
            q.append((i, j))
            visited[i][j] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        i, j = q.popleft()
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if (min_r <= ni <= max_r and min_c <= nj <= max_c and
                0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and out[ni][nj] == bg):
                out[ni][nj] = fill
                visited[ni][nj] = True
                q.append((ni, nj))

def compute_max_gap(side: str, min_r: int, max_r: int, min_c: int, max_c: int, g: List[List[int]], bg: int) -> int:
    current = 0
    maxg = 0
    if side == 'top' or side == 'bottom':
        horizontal = True
        fixed = min_r if side == 'top' else max_r
        start, end = min_c, max_c
        for j in range(start, end + 1):
            if g[fixed][j] == bg:
                current += 1
                maxg = max(maxg, current)
            else:
                current = 0
    else:
        horizontal = False
        fixed = min_c if side == 'left' else max_c
        start, end = min_r, max_r
        for i in range(start, end + 1):
            if g[i][fixed] == bg:
                current += 1
                maxg = max(maxg, current)
            else:
                current = 0
    return maxg

def detect_open_side(g: List[List[int]], bg: int, boundary: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int) -> str:
    sides = ['bottom', 'top', 'left', 'right']
    gaps = {s: compute_max_gap(s, min_r, max_r, min_c, max_c, g, bg) for s in sides}
    max_gap = max(gaps.values())
    if max_gap < 3:
        return None
    candidates = [s for s in sides if gaps[s] == max_gap]
    return candidates[0]

def get_intervals(poss: set) -> List[Tuple[int, int]]:
    if not poss:
        return []
    pl = sorted(poss)
    intervals = []
    st = pl[0]
    en = pl[0]
    for p in pl[1:]:
        if p == en + 1:
            en = p
        else:
            intervals.append((st, en))
            st = en = p
    intervals.append((st, en))
    return intervals

def expand_bottom(out: List[List[int]], g: List[List[int]], fill: int, bg: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int):
    blocker_row = [h] * w
    for j in range(w):
        for i in range(max_r + 1, h):
            c = g[i][j]
            if c != bg and c != fill:
                blocker_row[j] = i
                break
    filled_cols = {j for j in range(w) if out[max_r][j] == fill}
    intervals = get_intervals(filled_cols)
    current_row = max_r
    while intervals:
        next_row = current_row + 1
        if next_row >= h:
            break
        new_filled_cols = set()
        for st, en in intervals:
            new_st = max(0, st - 1)
            new_en = min(w - 1, en + 1)
            for j in range(new_st, new_en + 1):
                if out[next_row][j] == bg and next_row < blocker_row[j]:
                    out[next_row][j] = fill
                    new_filled_cols.add(j)
        intervals = get_intervals(new_filled_cols)
        current_row = next_row

def expand_top(out: List[List[int]], g: List[List[int]], fill: int, bg: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int):
    blocker_row = [-1] * w
    for j in range(w):
        for i in range(min_r - 1, -1, -1):
            c = g[i][j]
            if c != bg and c != fill:
                blocker_row[j] = i
                break
    filled_cols = {j for j in range(w) if out[min_r][j] == fill}
    intervals = get_intervals(filled_cols)
    current_row = min_r
    while intervals:
        next_row = current_row - 1
        if next_row < 0:
            break
        new_filled_cols = set()
        for st, en in intervals:
            new_st = max(0, st - 1)
            new_en = min(w - 1, en + 1)
            for j in range(new_st, new_en + 1):
                if out[next_row][j] == bg and next_row > blocker_row[j]:
                    out[next_row][j] = fill
                    new_filled_cols.add(j)
        intervals = get_intervals(new_filled_cols)
        current_row = next_row

def expand_left(out: List[List[int]], g: List[List[int]], fill: int, bg: int, boundary: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int):
    # First, left fill for boundary rows and upper non-boundary rows
    boundary_rows = set()
    leftmost_per_row = [w] * h
    for r in range(h):
        bound_js = [j for j in range(w) if g[r][j] == boundary]
        if bound_js:
            boundary_rows.add(r)
            leftmost_per_row[r] = min(bound_js)
            # Fill left in this row
            lm = leftmost_per_row[r]
            for j in range(lm):
                if out[r][j] == bg:
                    out[r][j] = fill
    # For upper non-boundary rows
    for r in range(min_r):
        min_d = math.inf
        base_lm = w
        for rb in boundary_rows:
            if rb >= r:  # only from below
                d = rb - r
                if d < min_d:
                    min_d = d
                    base_lm = leftmost_per_row[rb]
        if min_d < math.inf:
            effective_lm = base_lm - min_d
            if effective_lm > 0:
                for j in range(effective_lm):
                    if out[r][j] == bg:
                        out[r][j] = fill
    # Now, internal vertical flood per column j >= min_c
    for j in range(min_c, w):
        visited = [False] * h
        q = deque()
        for i in range(h):
            if out[i][j] == fill and not visited[i]:
                q.append(i)
                visited[i] = True
        dirs = [-1, 1]
        while q:
            i = q.popleft()
            for di in dirs:
                ni = i + di
                if 0 <= ni < h and not visited[ni] and out[ni][j] == bg:
                    out[ni][j] = fill
                    visited[ni] = True
                    q.append(ni)

def expand_right(out: List[List[int]], g: List[List[int]], fill: int, bg: int, boundary: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int):
    # Symmetric to left, but rightward
    boundary_rows = set()
    rightmost_per_row = [-1] * h
    for r in range(h):
        bound_js = [j for j in range(w) if g[r][j] == boundary]
        if bound_js:
            boundary_rows.add(r)
            rightmost_per_row[r] = max(bound_js)
            # Fill right in this row
            rm = rightmost_per_row[r]
            for j in range(rm + 1, w):
                if out[r][j] == bg:
                    out[r][j] = fill
    # For lower non-boundary rows (symmetric to upper for left)
    for r in range(max_r + 1, h):
        min_d = math.inf
        base_rm = -1
        for rb in boundary_rows:
            if rb <= r:  # only from above
                d = r - rb
                if d < min_d:
                    min_d = d
                    base_rm = rightmost_per_row[rb]
        if min_d < math.inf:
            effective_rm = base_rm + min_d
            if effective_rm < w - 1:
                for j in range(effective_rm + 1, w):
                    if out[r][j] == bg:
                        out[r][j] = fill
    # Internal vertical flood per column j <= max_c
    for j in range(max_c + 1):
        visited = [False] * h
        q = deque()
        for i in range(h):
            if out[i][j] == fill and not visited[i]:
                q.append(i)
                visited[i] = True
        dirs = [-1, 1]
        while q:
            i = q.popleft()
            for di in dirs:
                ni = i + di
                if 0 <= ni < h and not visited[ni] and out[ni][j] == bg:
                    out[ni][j] = fill
                    visited[ni] = True
                    q.append(ni)
```