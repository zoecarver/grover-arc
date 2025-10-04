```python
from typing import List, Dict
from collections import defaultdict, deque

def create_background_grid(h: int, w: int) -> List[List[int]]:
    return [[8] * w for _ in range(h)]

def has_color(g: List[List[int]], c: int) -> bool:
    return any(c in row for row in g)

def remove_yellow_if_pink(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if has_color(new_g, 6):
        h, w = len(new_g), len(new_g[0]) if new_g else 0
        for i in range(h):
            for j in range(w):
                if new_g[i][j] == 4:
                    new_g[i][j] = 8
    return new_g

def remove_small_blue_if_dark_red(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    if has_color(new_g, 7):
        return new_g
    h, w = len(new_g), len(new_g[0]) if new_g else 0
    visited = [[False] * w for _ in range(h)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if new_g[i][j] == 1 and not visited[i][j]:
                component = []
                q = deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and new_g[nx][ny] == 1:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            component.append((nx, ny))
                if len(component) <= 2:
                    for px, py in component:
                        new_g[px][py] = 8
    return new_g

def count_colors(g: List[List[int]]) -> Dict[int, int]:
    counts = defaultdict(int)
    h, w = len(g), len(g[0]) if g else 0
    for i in range(h):
        for j in range(w):
            if g[i][j] != 8:
                counts[g[i][j]] += 1
    return dict(counts)

def compute_avg_col(g: List[List[int]], c: int) -> float:
    total = 0.0
    cnt = 0
    h, w = len(g), len(g[0]) if g else 0
    for i in range(h):
        for j in range(w):
            if g[i][j] == c:
                total += j
                cnt += 1
    return total / cnt if cnt > 0 else float('inf')

def get_widths(n: int, c: int) -> List[int]:
    is_odd = c % 2 == 1
    if n <= 2:
        if is_odd:
            return [0, 0, 0, n]
        else:
            return [n, 0, 0, 0]
    k = 5 if is_odd else 7
    w_mid = (n + k) // 4
    t = max(0, n // 2 - w_mid)
    widths = [t, w_mid, w_mid, t]
    base = sum(widths)
    remaining = n - base
    if remaining > 0:
        widths[1] += remaining // 2
        widths[2] += remaining - (remaining // 2)
    return widths

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    cleaned = remove_yellow_if_pink(g)
    cleaned = remove_small_blue_if_dark_red(cleaned)
    counts = count_colors(cleaned)
    avgs = {c: compute_avg_col(cleaned, c) for c in counts}
    colors = sorted(counts, key=lambda c: (avgs[c], -c))
    out = create_background_grid(h, w)
    has_pink = has_color(g, 6)
    start_row = h // 2 - 2
    if start_row < 0:
        start_row = 0
    current_col = 2
    last_right = current_col - 1
    previous_small = False
    previous_current_col = 0
    for c in colors:
        n = counts.get(c, 0)
        if n == 0:
            continue
        is_odd = c % 2 == 1
        widths = get_widths(n, c)
        box_w = max(widths)
        if is_odd and has_pink:
            box_w += 1
        if n <= 2:
            if previous_small:
                current_col = previous_current_col
            else:
                current_col = last_right + 1
            previous_current_col = current_col
        else:
            current_col = last_right + 1
            previous_small = False
        placed_rights = []
        for r in range(4):
            wi = widths[r]
            if wi == 0:
                continue
            i = start_row + r
            if not (0 <= i < h):
                continue
            if r == 0 or r == 3:
                offset = 0 if is_odd else box_w - wi
            else:
                offset = (box_w - wi) if (is_odd and has_pink) else (0 if is_odd else box_w - wi)
            row_right = current_col + offset + wi - 1
            placed_rights.append(row_right)
            for jj in range(wi):
                j = current_col + offset + jj
                if 0 <= j < w:
                    out[i][j] = c
        if placed_rights:
            last_right = max(placed_rights)
        else:
            last_right = current_col + max(widths) - 1 if max(widths) > 0 else current_col - 1
        previous_small = (n <= 2)
    return out
```