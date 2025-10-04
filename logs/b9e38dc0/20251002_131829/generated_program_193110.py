```python
from typing import List, Tuple, Dict
from collections import Counter, deque

def get_bg_and_boundary(g: List[List[int]]) -> Tuple[int, int]:
    if not g or not g[0]:
        return 0, 0
    h, w = len(g), len(g[0])
    flat = [g[i][j] for i in range(h) for j in range(w)]
    count_all = Counter(flat)
    bg = count_all.most_common(1)[0][0] if count_all else 0
    non_bg_count = Counter(c for c in flat if c != bg)
    boundary = non_bg_count.most_common(1)[0][0] if non_bg_count else bg
    return bg, boundary

def select_fill_color(g: List[List[int]], bg: int, boundary: int) -> int:
    h, w = len(g), len(g[0])
    flat = [g[i][j] for i in range(h) for j in range(w)]
    non_bg_count = Counter(c for c in flat if c != bg)
    if len(non_bg_count) <= 1:
        return boundary

    def min_dist_to_boundary(color):
        if color in (bg, boundary):
            return float('inf')
        seed_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == color]
        if not seed_pos:
            return float('inf')
        bound_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == boundary]
        if not bound_pos:
            return float('inf')
        min_d = float('inf')
        for si, sj in seed_pos:
            for bi, bj in bound_pos:
                d = abs(si - bi) + abs(sj - bj)
                min_d = min(min_d, d)
        return min_d

    possible_fills = [c for c in non_bg_count if c != boundary]
    if not possible_fills:
        return boundary
    fill_dists = [(c, min_dist_to_boundary(c), non_bg_count[c]) for c in possible_fills]
    fill_dists.sort(key=lambda x: (x[1], -x[2], x[0]))
    return fill_dists[0][0]

def get_blockers(g: List[List[int]], bg: int, boundary: int, fill: int, h: int, w: int) -> Dict[int, int]:
    blockers = {}
    for j in range(w):
        min_r = float('inf')
        for i in range(h):
            c = g[i][j]
            if c != bg and c != boundary and c != fill:
                min_r = min(min_r, i)
        if min_r != float('inf'):
            blockers[j] = min_r
    return blockers

def get_up_blockers(g: List[List[int]], bg: int, boundary: int, fill: int, h: int, w: int) -> Dict[int, int]:
    blockers = {}
    for j in range(w):
        max_r = float('-inf')
        for i in range(h):
            c = g[i][j]
            if c != bg and c != boundary and c != fill:
                max_r = max(max_r, i)
        if max_r != float('-inf'):
            blockers[j] = max_r
    return blockers

def get_left_blockers(g: List[List[int]], bg: int, boundary: int, fill: int, h: int, w: int) -> Dict[int, int]:
    blockers = {}
    for i in range(h):
        min_c = float('inf')
        for j in range(w):
            c = g[i][j]
            if c != bg and c != boundary and c != fill:
                min_c = min(min_c, j)
        if min_c != float('inf'):
            blockers[i] = min_c
    return blockers

def get_right_blockers(g: List[List[int]], bg: int, boundary: int, fill: int, h: int, w: int) -> Dict[int, int]:
    blockers = {}
    for i in range(h):
        max_c = float('-inf')
        for j in range(w):
            c = g[i][j]
            if c != bg and c != boundary and c != fill:
                max_c = max(max_c, j)
        if max_c != float('-inf'):
            blockers[i] = max_c
    return blockers

def get_intervals(poss: set[int]) -> List[Tuple[int, int]]:
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

def internal_flood(g: List[List[int]], out: List[List[int]], fill: int, bg: int, boundary_pos: List[Tuple[int, int]]) -> None:
    if not boundary_pos:
        return
    min_r = min(i for i, _ in boundary_pos)
    max_r = max(i for i, _ in boundary_pos)
    min_c = min(j for _, j in boundary_pos)
    max_c = max(j for _, j in boundary_pos)
    h, w = len(g), len(g[0])
    seeds = [(i, j) for i in range(min_r, max_r + 1) for j in range(min_c, max_c + 1) if g[i][j] == fill]
    if not seeds:
        return
    visited = [[False] * w for _ in range(h)]
    q = deque(seeds)
    for i, j in seeds:
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

def get_side_gaps(g: List[List[int]], bg: int, min_r: int, max_r: int, min_c: int, max_c: int, h: int, w: int) -> Dict[str, int]:
    gaps = {}
    # top
    current = 0
    mg = 0
    for j in range(min_c, max_c + 1):
        if g[min_r][j] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['top'] = mg
    # bottom
    current = 0
    mg = 0
    for j in range(min_c, max_c + 1):
        if g[max_r][j] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['bottom'] = mg
    # left
    current = 0
    mg = 0
    for i in range(min_r, max_r + 1):
        if g[i][min_c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['left'] = mg
    # right
    current = 0
    mg = 0
    for i in range(min_r, max_r + 1):
        if g[i][max_c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['right'] = mg
    return gaps

def propagate_down(out: List[List[int]], fill: int, bg: int, down_blockers: Dict[int, int], h: int, w: int, start_i: int) -> None:
    current_i = start_i
    while current_i < h - 1:
        filled_cols_set = {j for j in range(w) if out[current_i][j] == fill}
        if not filled_cols_set:
            break
        intervals = get_intervals(filled_cols_set)
        next_i = current_i + 1
        changed = False
        for l, r in intervals:
            new_l = max(0, l - 1)
            new_r = min(w - 1, r + 1)
            for j in range(new_l, new_r + 1):
                if out[next_i][j] == bg and not (j in down_blockers and next_i >= down_blockers[j]):
                    out[next_i][j] = fill
                    changed = True
        if not changed:
            break
        current_i = next_i

def propagate_up(out: List[List[int]], fill: int, bg: int, up_blockers: Dict[int, int], h: int, w: int, start_i: int) -> None:
    current_i = start_i
    while current_i > 0:
        filled_cols_set = {j for j in range(w) if out[current_i][j] == fill}
        if not filled_cols_set:
            break
        intervals = get_intervals(filled_cols_set)
        next_i = current_i - 1
        changed = False
        for l, r in intervals:
            new_l = max(0, l - 1)
            new_r = min(w - 1, r + 1)
            for j in range(new_l, new_r + 1):
                if out[next_i][j] == bg and not (j in up_blockers and next_i <= up_blockers[j]):
                    out[next_i][j] = fill
                    changed = True
        if not changed:
            break
        current_i = next_i

def propagate_left(out: List[List[int]], fill: int, bg: int, left_blockers: Dict[int, int], h: int, w: int, start_j: int) -> None:
    current_j = start_j
    while current_j > 0:
        filled_rows_set = {i for i in range(h) if out[i][current_j] == fill}
        if not filled_rows_set:
            break
        intervals = get_intervals(filled_rows_set)
        next_j = current_j - 1
        changed = False
        for t, b in intervals:
            new_t = max(0, t - 1)
            new_b = min(h - 1, b + 1)
            for i in range(new_t, new_b + 1):
                if out[i][next_j] == bg and not (i in left_blockers and next_j < left_blockers[i]):
                    out[i][next_j] = fill
                    changed = True
        if not changed:
            break
        current_j = next_j

def propagate_right(out: List[List[int]], fill: int, bg: int, right_blockers: Dict[int, int], h: int, w: int, start_j: int) -> None:
    current_j = start_j
    while current_j < w - 1:
        filled_rows_set = {i for i in range(h) if out[i][current_j] == fill}
        if not filled_rows_set:
            break
        intervals = get_intervals(filled_rows_set)
        next_j = current_j + 1
        changed = False
        for t, b in intervals:
            new_t = max(0, t - 1)
            new_b = min(h - 1, b + 1)
            for i in range(new_t, new_b + 1):
                if out[i][next_j] == bg and not (i in right_blockers and next_j > right_blockers[i]):
                    out[i][next_j] = fill
                    changed = True
        if not changed:
            break
        current_j = next_j

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    out = [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    bg, boundary = get_bg_and_boundary(g)
    fill = select_fill_color(g, bg, boundary)
    boundary_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == boundary]
    internal_flood(g, out, fill, bg, boundary_pos)
    if not boundary_pos:
        return out
    min_r = min(i for i, _ in boundary_pos)
    max_r = max(i for i, _ in boundary_pos)
    min_c = min(j for _, j in boundary_pos)
    max_c = max(j for _, j in boundary_pos)
    side_gaps = get_side_gaps(g, bg, min_r, max_r, min_c, max_c, h, w)
    open_side = max(side_gaps, key=side_gaps.get)
    if side_gaps[open_side] < 2:
        return out
    down_blockers = get_blockers(g, bg, boundary, fill, h, w)
    up_blockers = get_up_blockers(g, bg, boundary, fill, h, w)
    left_blockers = get_left_blockers(g, bg, boundary, fill, h, w)
    right_blockers = get_right_blockers(g, bg, boundary, fill, h, w)
    if open_side == 'bottom':
        propagate_down(out, fill, bg, down_blockers, h, w, max_r)
    elif open_side == 'top':
        propagate_up(out, fill, bg, up_blockers, h, w, min_r)
    elif open_side == 'left':
        propagate_left(out, fill, bg, left_blockers, h, w, min_c)
    elif open_side == 'right':
        propagate_right(out, fill, bg, right_blockers, h, w, max_c)
    return out
```