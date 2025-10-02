```python
from collections import Counter, deque, defaultdict
from typing import List, Dict

def erase_small(g: List[List[int]], bg: int, min_size: int, small_colors: set, erased: Dict[int, List[tuple]]) -> None:
    h = len(g)
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for si in range(h):
        for sj in range(w):
            if visited[si][sj] or g[si][sj] == bg:
                continue
            q = deque([(si, sj)])
            visited[si][sj] = True
            component = [(si, sj)]
            color = g[si][sj]
            while q:
                ci, cj = q.popleft()
                for di, dj in dirs:
                    ni = ci + di
                    nj = cj + dj
                    if 0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and g[ni][nj] == color:
                        visited[ni][nj] = True
                        q.append((ni, nj))
                        component.append((ni, nj))
            if len(component) < min_size:
                small_colors.add(color)
                for x, y in component:
                    erased[color].append((x, y))
                    g[x][y] = bg

def complete_frames(g: List[List[int]], bg: int, small_colors: set, erased: Dict[int, List[tuple]], h: int, w: int) -> None:
    span = 11
    for i in range(h - 4):
        for start in range(w - span + 1):
            c = g[i][start]
            if c == bg or c not in small_colors:
                continue
            # check above bg row
            above_bg = i > 0 and all(g[i - 1][start + k] == bg for k in range(span))
            if not above_bg:
                continue
            # check full top bar
            is_bar = all(g[i][start + k] == c for k in range(span))
            if not is_bar:
                continue
            left = start
            right = start + span - 1
            # top borders
            border_left = left == 0 or g[i][left - 1] == bg
            border_right = right == w - 1 or g[i][right + 1] == bg
            if not (border_left and border_right):
                continue
            # find consecutive v rows
            num_v = 0
            fill_i = -1
            j = i + 1
            while j < h:
                is_v = g[j][left] == c and g[j][right] == c and all(g[j][k] == bg for k in range(left + 1, right))
                if is_v:
                    num_v += 1
                    if num_v == 2:
                        fill_i = j
                    j += 1
                else:
                    break
            if num_v < 2:
                continue
            # check bottom bar at j
            if j >= h:
                continue
            is_bottom = all(g[j][left + k] == c for k in range(span))
            b_border_left = left == 0 or g[j][left - 1] == bg
            b_border_right = right == w - 1 or g[j][right + 1] == bg
            if not (is_bottom and b_border_left and b_border_right):
                continue
            # check below bg row
            below_bg = j + 1 < h and all(g[j + 1][left + k] == bg for k in range(span))
            if not below_bg:
                continue
            # complete fill in second v row
            if fill_i != -1:
                if c == 1:
                    erased_count = sum(1 for x, y in erased.get(c, []) if x == fill_i and left < y < right)
                    m = 2 - erased_count
                else:
                    m = c // 2
                if m > 0:
                    for kk in range(1, m + 1):
                        pos = right - 2 * kk
                        if left < pos < right:
                            g[fill_i][pos] = c

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0])
    flat = [cell for row in g for cell in row]
    bg = Counter(flat).most_common(1)[0][0]
    work_g = [row[:] for row in g]
    small_colors = set()
    erased = defaultdict(list)
    erase_small(work_g, bg, 12, small_colors, erased)
    complete_frames(work_g, bg, small_colors, erased, h, w)
    return work_g
```