```python
from typing import List, Dict, Tuple
from collections import defaultdict, deque

def has_color(g: List[List[int]], c: int) -> bool:
    for row in g:
        if any(cell == c for cell in row):
            return True
    return False

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    rows = len(new_g)
    cols = len(new_g[0]) if rows > 0 else 0
    if has_color(g, 6):
        for i in range(rows):
            for j in range(cols):
                if new_g[i][j] == 4:
                    new_g[i][j] = 8
    return new_g

def remove_small_blue_if_dark_red(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    rows = len(new_g)
    cols = len(new_g[0]) if rows > 0 else 0
    if not has_color(g, 7):
        return new_g
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if new_g[i][j] == 1 and not visited[i][j]:
                component = []
                q = deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and new_g[nx][ny] == 1:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            component.append((nx, ny))
                size = len(component)
                if size <= 2:
                    for px, py in component:
                        new_g[px][py] = 8
    return new_g

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    counts = defaultdict(int)
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    for i in range(rows):
        for j in range(cols):
            c = g[i][j]
            if c != 8:
                counts[c] += 1
    return dict(counts)

def compute_avg_col(g: List[List[int]], c: int) -> float:
    total = 0.0
    count = 0
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == c:
                total += j
                count += 1
    return total / count if count > 0 else 0.0

def get_shape_params(n: int, c: int) -> Tuple[List[int], int]:
    if n == 0:
        return [0, 0, 0, 0], 0
    is_odd = c % 2 == 1
    if n <= 2:
        if is_odd:
            return [0, 0, 0, n], n
        else:
            return [n, 0, 0, 0], n
    k = 5 if is_odd else 7
    w = (n + k) // 4
    t = max(0, n // 2 - w)
    widths = [t, w, w, t]
    base = sum(widths)
    remaining = n - base
    if remaining > 0:
        widths[1] += remaining // 2
        widths[2] += remaining - (remaining // 2)
    else:
        diff = base - n
        widths[1] -= diff // 2
        widths[2] -= diff - (diff // 2)
        widths = [max(0, x) for x in widths]
    bw = max(widths) if any(widths) else 0
    return widths, bw

def dry_place(widths: List[int], box_left: int, is_odd: bool) -> Tuple[int, int]:
    bw = max(widths + [0])
    lmin = float('inf')
    rmax = -float('inf')
    for ri in range(4):
        wi = widths[ri]
        if wi == 0:
            continue
        offset = 0 if is_odd else bw - wi
        s = box_left + offset
        e = s + wi - 1
        lmin = min(lmin, s)
        rmax = max(rmax, e)
    return int(lmin), int(rmax)

def place_shape(out: List[List[int]], c: int, widths: List[int], box_left: int, start_r: int, rows: int, cols: int):
    is_odd = c % 2 == 1
    bw = max(widths + [0])
    for ri in range(4):
        wi = widths[ri]
        if wi == 0:
            continue
        row = start_r + ri
        if row < 0 or row >= rows:
            continue
        offset = 0 if is_odd else bw - wi
        col_start = box_left + offset
        for k in range(wi):
            col = col_start + k
            if 0 <= col < cols:
                out[row][col] = c

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        rows, cols = 0, 0
    else:
        rows = len(g)
        cols = len(g[0])
    clean_g = remove_yellow_if_pink(g)
    clean_g = remove_small_blue_if_dark_red(clean_g)
    counts = count_colors(clean_g)
    if not counts:
        return [[8] * cols for _ in range(rows)]
    colors = list(counts.keys())
    colors.sort(key=lambda cc: (compute_avg_col(clean_g, cc), -cc))
    box_lefts: Dict[int, int] = {}
    current_left = 0
    previous_small = False
    previous_box_l = 0
    for c in colors:
        n = counts[c]
        widths, bw = get_shape_params(n, c)
        is_small = n <= 2
        if is_small and previous_small:
            box_l = previous_box_l
            advance = 0
        else:
            box_l = current_left
            advance = bw + 1
        box_lefts[c] = box_l
        current_left += advance
        previous_box_l = box_l
        previous_small = is_small
    # dry run for centering
    min_placed = float('inf')
    max_placed = -float('inf')
    for c in colors:
        box_l = box_lefts[c]
        widths, _ = get_shape_params(counts[c], c)
        is_odd = c % 2 == 1
        lmin, rmax = dry_place(widths, box_l, is_odd)
        min_placed = min(min_placed, lmin)
        max_placed = max(max_placed, rmax)
    total_w = max_placed - min_placed + 1 if min_placed <= max_placed else 0
    margin = (cols - total_w) // 2
    shift = margin - min_placed
    # place
    start_r = (rows - 4) // 2
    out = [[8] * cols for _ in range(rows)]
    for c in colors:
        actual_box_l = box_lefts[c] + shift
        widths, _ = get_shape_params(counts[c], c)
        place_shape(out, c, widths, actual_box_l, start_r, rows, cols)
    return out
```