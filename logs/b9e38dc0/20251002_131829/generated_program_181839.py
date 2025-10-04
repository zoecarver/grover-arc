```python
from typing import List, Tuple
from collections import deque, Counter, defaultdict

def is_border_connected(g: List[List[int]], color: int, rows: int, cols: int) -> bool:
    if color == 0:
        return False
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in (0, cols - 1):
            if g[r][c] == color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
    for c in range(cols):
        for r in (0, rows - 1):
            if g[r][c] == color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                visited[nr][nc] = True
                q.append((nr, nc))
    total = sum(1 for rr in range(rows) for cc in range(cols) if g[rr][cc] == color)
    vis_count = sum(sum(1 for cc in range(cols) if visited[rr][cc]) for rr in range(rows))
    return vis_count == total

def get_bg(g: List[List[int]]) -> int:
    rows = len(g)
    if rows == 0:
        return 0
    cols = len(g[0])
    flat_count = Counter(cell for row in g for cell in row)
    candidates = [(flat_count[color], color) for color in flat_count if is_border_connected(g, color, rows, cols)]
    if not candidates:
        return 0
    candidates.sort(reverse=True)
    return candidates[0][1]

def get_components(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                comp = []
                q = deque([(r, c)])
                visited[r][c] = True
                while q:
                    cr, cc = q.popleft()
                    comp.append((cr, cc))
                    for dr, dc in dirs:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                components.append((color, comp))
    return components

def get_structure_color_and_pos(components: List[Tuple[int, List[Tuple[int, int]]]], bg: int) -> Tuple[int, List[Tuple[int, int]]]:
    color_sizes = Counter()
    color_pos = defaultdict(list)
    for color, comp in components:
        if color != bg:
            color_sizes[color] += len(comp)
            color_pos[color].extend(comp)
    if not color_sizes:
        return None, []
    struct_color = max(color_sizes, key=color_sizes.get)
    return struct_color, color_pos[struct_color]

def get_bbox(pos: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not pos:
        return 0, 0, 0, 0
    min_r = min(r for r, c in pos)
    max_r = max(r for r, c in pos)
    min_c = min(c for r, c in pos)
    max_c = max(c for r, c in pos)
    return min_r, max_r, min_c, max_c

def get_seed_color(g: List[List[int]], components: List[Tuple[int, List[Tuple[int, int]]]], struct_color: int, min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> int:
    inside_counts = Counter()
    rows, cols = len(g), len(g[0])
    for color, comp in components:
        if color == struct_color or color == bg:
            continue
        inside = 0
        for r, c in comp:
            if min_r <= r <= max_r and min_c <= c <= max_c:
                inside += 1
        if inside > 0:
            inside_counts[color] = inside
    if not inside_counts:
        return None
    return min(inside_counts, key=inside_counts.get)

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def internal_fill(work: List[List[int]], seed_color: int, struct_color: int, min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> List[List[int]]:
    rows, cols = len(work), len(work[0])
    visited = [[False] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if work[r][c] == seed_color and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if (min_r <= nr <= max_r and min_c <= nc <= max_c and 0 <= nr < rows and 0 <= nc < cols and
                not visited[nr][nc] and work[nr][nc] == bg):
                work[nr][nc] = seed_color
                visited[nr][nc] = True
                q.append((nr, nc))
    return work

def detect_open_side(g: List[List[int]], struct_color: int, min_r: int, max_r: int, min_c: int, max_c: int, bg: int) -> str:
    gaps = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}
    # top
    current = 0
    mg = 0
    for c in range(min_c, max_c + 1):
        if g[min_r][c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['top'] = mg
    # bottom
    current = 0
    mg = 0
    for c in range(min_c, max_c + 1):
        if g[max_r][c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['bottom'] = mg
    # left
    current = 0
    mg = 0
    for r in range(min_r, max_r + 1):
        if g[r][min_c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['left'] = mg
    # right
    current = 0
    mg = 0
    for r in range(min_r, max_r + 1):
        if g[r][max_c] == bg:
            current += 1
            mg = max(mg, current)
        else:
            current = 0
    gaps['right'] = mg
    max_gap = max(gaps.values())
    if max_gap < 3:
        return None
    for side in ['bottom', 'top', 'left', 'right']:
        if gaps[side] == max_gap:
            return side
    return None

def get_intervals(poss: set[int]) -> List[Tuple[int, int]]:
    if not poss:
        return []
    pl = sorted(poss)
    intervals = []
    st = pl[0]
    en = st
    for i in range(1, len(pl)):
        if pl[i] == en + 1:
            en = pl[i]
        else:
            intervals.append((st, en))
            st = en = pl[i]
    intervals.append((st, en))
    return intervals

def expand_bottom(work: List[List[int]], original: List[List[int]], seed_color: int, min_r: int, max_r: int, min_c: int, max_c: int, bg: int, rows: int, cols: int):
    shadowed = set()
    for c in range(cols):
        for r in range(max_r + 2):
            if r < rows and original[r][c] != bg and original[r][c] != seed_color:
                shadowed.add(c)
                break
    gaps = []
    start = None
    for c in range(min_c, max_c + 1):
        if original[max_r][c] == bg:
            if start is None:
                start = c
        else:
            if start is not None:
                gaps.append((start, c - 1))
                start = None
    if start is not None:
        gaps.append((start, max_c))
    spill_r = max_r + 1
    if spill_r >= rows:
        return
    filled_cs = set()
    for s, e in gaps:
        for c in range(s, e + 1):
            if work[spill_r][c] == bg:
                work[spill_r][c] = seed_color
                filled_cs.add(c)
    limit_min = min_c - 1
    limit_max = max_c + 1
    temp = set()
    for c in filled_cs:
        for dc in [-1, 1]:
            nc = c + dc
            if limit_min <= nc <= limit_max and 0 <= nc < cols and work[spill_r][nc] == bg:
                work[spill_r][nc] = seed_color
                temp.add(nc)
    filled_cs.update(temp)
    current_r = spill_r
    while current_r + 1 < rows:
        current_r += 1
        if not filled_cs:
            break
        intervals = get_intervals(filled_cs)
        widened = []
        for st, en in intervals:
            nst = max(0, st - 1)
            nen = min(cols - 1, en + 1)
            widened.append((nst, nen))
        new_filled_cs = set()
        for st, en in widened:
            for c in range(st, en + 1):
                if work[current_r][c] == bg and c not in shadowed:
                    work[current_r][c] = seed_color
                    new_filled_cs.add(c)
        filled_cs = new_filled_cs

def expand_left(work: List[List[int]], original: List[List[int]], seed_color: int, min_r: int, max_r: int, min_c: int, max_c: int, bg: int, rows: int, cols: int):
    shadowed = set()  # no shadow for left
    gaps = []
    start = None
    for r in range(min_r, max_r + 1):
        if original[r][min_c] == bg:
            if start is None:
                start = r
        else:
            if start is not None:
                gaps.append((start, r - 1))
                start = None
    if start is not None:
        gaps.append((start, max_r))
    spill_c = min_c - 1
    if spill_c < 0:
        return
    filled_rs = set()
    for s, e in gaps:
        for r in range(s, e + 1):
            if work[r][spill_c] == bg:
                work[r][spill_c] = seed_color
                filled_rs.add(r)
    limit_minr = min_r - 1
    limit_maxr = max_r + 1
    temp = set()
    for r in filled_rs:
        for dr in [-1, 1]:
            nr = r + dr
            if limit_minr <= nr <= limit_maxr and 0 <= nr < rows and work[nr][spill_c] == bg:
                work[nr][spill_c] = seed_color
                temp.add(nr)
    filled_rs.update(temp)
    current_c = spill_c
    while current_c - 1 >= 0:
        current_c -= 1
        if not filled_rs:
            break
        intervals = get_intervals(filled_rs)
        widened = []
        for st, en in intervals:
            nst = max(0, st - 1)
            nen = min(rows - 1, en + 1)
            widened.append((nst, nen))
        new_filled_rs = set()
        for st, en in widened:
            for r in range(st, en + 1):
                if work[r][current_c] == bg and r not in shadowed:
                    work[r][current_c] = seed_color
                    new_filled_rs.add(r)
        filled_rs = new_filled_rs

def expand_top(work: List[List[int]], original: List[List[int]], seed_color: int, min_r: int, max_r: int, min_c: int, max_c: int, bg: int, rows: int, cols: int):
    shadowed = set()  # no shadow for top
    gaps = []
    start = None
    for c in range(min_c, max_c + 1):
        if original[min_r][c] == bg:
            if start is None:
                start = c
        else:
            if start is not None:
                gaps.append((start, c - 1))
                start = None
    if start is not None:
        gaps.append((start, max_c))
    spill_r = min_r - 1
    if spill_r < 0:
        return
    filled_cs = set()
    for s, e in gaps:
        for c in range(s, e + 1):
            if work[spill_r][c] == bg:
                work[spill_r][c] = seed_color
                filled_cs.add(c)
    limit_min = min_c - 1
    limit_max = max_c + 1
    temp = set()
    for c in filled_cs:
        for dc in [-1, 1]:
            nc = c + dc
            if limit_min <= nc <= limit_max and 0 <= nc < cols and work[spill_r][nc] == bg:
                work[spill_r][nc] = seed_color
                temp.add(nc)
    filled_cs.update(temp)
    current_r = spill_r
    while current_r - 1 >= 0:
        current_r -= 1
        if not filled_cs:
            break
        intervals = get_intervals(filled_cs)
        widened = []
        for st, en in intervals:
            nst = max(0, st - 1)
            nen = min(cols - 1, en + 1)
            widened.append((nst, nen))
        new_filled_cs = set()
        for st, en in widened:
            for c in range(st, en + 1):
                if work[current_r][c] == bg and c not in shadowed:
                    work[current_r][c] = seed_color
                    new_filled_cs.add(c)
        filled_cs = new_filled_cs

def expand_right(work: List[List[int]], original: List[List[int]], seed_color: int, min_r: int, max_r: int, min_c: int, max_c: int, bg: int, rows: int, cols: int):
    shadowed = set()  # no shadow for right
    gaps = []
    start = None
    for r in range(min_r, max_r + 1):
        if original[r][max_c] == bg:
            if start is None:
                start = r
        else:
            if start is not None:
                gaps.append((start, r - 1))
                start = None
    if start is not None:
        gaps.append((start, max_r))
    spill_c = max_c + 1
    if spill_c >= cols:
        return
    filled_rs = set()
    for s, e in gaps:
        for r in range(s, e + 1):
            if work[r][spill_c] == bg:
                work[r][spill_c] = seed_color
                filled_rs.add(r)
    limit_minr = min_r - 1
    limit_maxr = max_r + 1
    temp = set()
    for r in filled_rs:
        for dr in [-1, 1]:
            nr = r + dr
            if limit_minr <= nr <= limit_maxr and 0 <= nr < rows and work[nr][spill_c] == bg:
                work[nr][spill_c] = seed_color
                temp.add(nr)
    filled_rs.update(temp)
    current_c = spill_c
    while current_c + 1 < cols:
        current_c += 1
        if not filled_rs:
            break
        intervals = get_intervals(filled_rs)
        widened = []
        for st, en in intervals:
            nst = max(0, st - 1)
            nen = min(rows - 1, en + 1)
            widened.append((nst, nen))
        new_filled_rs = set()
        for st, en in widened:
            for r in range(st, en + 1):
                if work[r][current_c] == bg and r not in shadowed:
                    work[r][current_c] = seed_color
                    new_filled_rs.add(r)
        filled_rs = new_filled_rs

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return copy_grid(g)
    bg = get_bg(g)
    components = get_components(g, bg)
    struct_color, union_pos = get_structure_color_and_pos(components, bg)
    if struct_color is None:
        return copy_grid(g)
    min_r, max_r, min_c, max_c = get_bbox(union_pos)
    seed_color = get_seed_color(g, components, struct_color, min_r, max_r, min_c, max_c, bg)
    if seed_color is None:
        return copy_grid(g)
    work = copy_grid(g)
    work = internal_fill(work, seed_color, struct_color, min_r, max_r, min_c, max_c, bg)
    open_side = detect_open_side(g, struct_color, min_r, max_r, min_c, max_c, bg)
    rows = len(g)
    cols = len(g[0])
    if open_side == 'bottom':
        expand_bottom(work, g, seed_color, min_r, max_r, min_c, max_c, bg, rows, cols)
    elif open_side == 'left':
        expand_left(work, g, seed_color, min_r, max_r, min_c, max_c, bg, rows, cols)
    elif open_side == 'top':
        expand_top(work, g, seed_color, min_r, max_r, min_c, max_c, bg, rows, cols)
    elif open_side == 'right':
        expand_right(work, g, seed_color, min_r, max_r, min_c, max_c, bg, rows, cols)
    return work
```