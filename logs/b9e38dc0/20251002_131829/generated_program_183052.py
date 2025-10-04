```python
from typing import List, Tuple, Set
from collections import Counter, deque

def get_dimensions(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    return len(g), len(g[0])

def is_border_connected(g: List[List[int]], color: int, h: int, w: int) -> bool:
    if h == 0 or w == 0 or color == 0:
        return False
    visited = [[False] * w for _ in range(h)]
    q = deque()
    added = False
    for r in range(h):
        for c in (0, w - 1):
            if g[r][c] == color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
                added = True
    for c in range(1, w - 1):
        for r in (0, h - 1):
            if g[r][c] == color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
                added = True
    if not added:
        return False
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] == color:
                visited[nr][nc] = True
                q.append((nr, nc))
    total = sum(1 for rr in range(h) for cc in range(w) if g[rr][cc] == color)
    vis_count = sum(1 for rr in range(h) for cc in range(w) if visited[rr][cc])
    return vis_count == total

def find_background(g: List[List[int]]) -> int:
    h, w = get_dimensions(g)
    flat = [g[r][c] for r in range(h) for c in range(w)]
    count = Counter(flat)
    candidates = []
    for color in count:
        if is_border_connected(g, color, h, w):
            candidates.append((count[color], color))
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    return count.most_common(1)[0][0] if count else 0

def select_fill_color(g: List[List[int]], bg: int, boundary: int) -> int:
    h, w = get_dimensions(g)
    flat = [g[i][j] for i in range(h) for j in range(w)]
    non_bg_count = Counter(c for c in flat if c != bg)
    possible_fills = [c for c in non_bg_count if c != boundary and non_bg_count[c] > 0]
    if not possible_fills:
        return boundary

    def min_dist(color):
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

def max_consecutive_bg(g: List[List[int]], bg: int, fixed: int, start: int, end: int, horizontal: bool) -> int:
    max_run = 0
    current = 0
    if horizontal:
        for j in range(start, end + 1):
            if g[fixed][j] == bg:
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0
    else:
        for i in range(start, end + 1):
            if g[i][fixed] == bg:
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0
    return max_run

def get_intervals(poss: Set[int]) -> List[Tuple[int, int]]:
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

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h = len(out)
    if h == 0:
        return out
    w = len(out[0])
    bg = find_background(out)
    non_bg_flat = [c for row in out for c in row if c != bg]
    if not non_bg_flat:
        return out
    non_bg_count = Counter(non_bg_flat)
    boundary = non_bg_count.most_common(1)[0][0]
    fill = select_fill_color(out, bg, boundary)
    if fill in (bg, boundary):
        return out
    bound_pos = [(i, j) for i in range(h) for j in range(w) if out[i][j] == boundary]
    if not bound_pos:
        return out
    min_r = min(p[0] for p in bound_pos)
    max_r = max(p[0] for p in bound_pos)
    min_c = min(p[1] for p in bound_pos)
    max_c = max(p[1] for p in bound_pos)
    top_gap = max_consecutive_bg(out, bg, min_r, min_c, max_c, horizontal=True)
    bottom_gap = max_consecutive_bg(out, bg, max_r, min_c, max_c, horizontal=True)
    left_gap = max_consecutive_bg(out, bg, min_c, min_r, max_r, horizontal=False)
    right_gap = max_consecutive_bg(out, bg, max_c, min_r, max_r, horizontal=False)
    gaps = {'top': top_gap, 'bottom': bottom_gap, 'left': left_gap, 'right': right_gap}
    max_g = max(gaps.values())
    open_sides = [s for s, gg in gaps.items() if gg == max_g]
    open_side = next((s for s in ['bottom', 'left', 'top', 'right'] if s in open_sides), None)
    is_open_left = left_gap > 3
    is_open_bottom = bottom_gap > 3
    is_closed = max_g < 3
    # local seed flood within bbox
    fill_pos = [(ii, jj) for ii in range(h) for jj in range(w) if out[ii][jj] == fill]
    if fill_pos:
        visited = [[False] * w for _ in range(h)]
        q = deque()
        for r, c in fill_pos:
            if min_r <= r <= max_r and min_c <= c <= max_c:
                if not visited[r][c]:
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
    # span fill if not open left
    if not is_open_left:
        for i in range(min_r, max_r + 1):
            bound_js = [j for j in range(w) if out[i][j] == boundary]
            if len(bound_js) >= 2:
                l = min(bound_js)
                r = max(bound_js)
                for j in range(l + 1, r):
                    if out[i][j] == bg:
                        out[i][j] = fill
    # left fill if open left
    if is_open_left:
        structure_rows_right = {}
        for i in range(h):
            bound_js = [j for j in range(w) if out[i][j] == boundary]
            if bound_js:
                l_min = min(bound_js)
                structure_rows_right[i] = l_min - 1
                for j in range(l_min):
                    if out[i][j] == bg:
                        out[i][j] = fill
        # upward narrowing
        if structure_rows_right:
            top_struct = min(structure_rows_right)
            current_right = structure_rows_right[top_struct]
            for i in range(top_struct - 1, -1, -1):
                current_right = max(-1, current_right - 1)
                for j in range(current_right + 1):
                    if out[i][j] == bg:
                        out[i][j] = fill
        # downward widening
            bottom_struct = max(structure_rows_right)
            current_right = structure_rows_right[bottom_struct]
            for i in range(bottom_struct + 1, h):
                current_right = min(w - 1, current_right + 1)
                for j in range(current_right + 1):
                    if out[i][j] == bg:
                        out[i][j] = fill
    # bottom expansion if open bottom
    if is_open_bottom:
        shadowed: Set[int] = set()
        for j in range(w):
            for ii in range(max_r + 1, h):
                if g[ii][j] != bg and g[ii][j] != fill:
                    shadowed.add(j)
                    break
        filled_cols = [j for j in range(w) if out[max_r][j] == fill]
        current_intervals = get_intervals(set(filled_cols))
        for i in range(max_r + 1, h):
            new_filled = set()
            for l, r in current_intervals:
                new_l = max(0, l - 1)
                new_r = min(w - 1, r + 1)
                for j in range(new_l, new_r + 1):
                    if j not in shadowed and out[i][j] == bg:
                        out[i][j] = fill
                        new_filled.add(j)
            current_intervals = get_intervals(new_filled)
            if not current_intervals:
                break
    # vertical propagation for closed
    if is_closed:
        # upward
        for i in range(1, h):
            for j in range(w):
                if out[i][j] == bg and out[i - 1][j] == fill:
                    out[i][j] = fill
        # downward
        for i in range(h - 2, -1, -1):
            for j in range(w):
                if out[i][j] == bg and out[i + 1][j] == fill:
                    out[i][j] = fill
    return out
```