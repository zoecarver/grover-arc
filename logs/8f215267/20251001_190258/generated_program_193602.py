```python
from collections import Counter, deque
from typing import List, Set

def find_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def erase_small_components(g: List[List[int]], bg: int, min_size: int, small_colors: Set[int]) -> None:
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
                    g[x][y] = bg

def detect_and_complete_frames(g: List[List[int]], bg: int, small_colors: Set[int]) -> None:
    h = len(g)
    w = len(g[0])
    span = 11
    for i in range(h - 3):
        for start in range(w - span + 1):
            if g[i][start] == bg:
                continue
            c = g[i][start]
            if c not in small_colors:
                continue
            is_bar = all(g[i][start + k] == c for k in range(span))
            if not is_bar:
                continue
            left = start
            right = start + span - 1
            border_left = left == 0 or g[i][left - 1] == bg
            border_right = right == w - 1 or g[i][right + 1] == bg
            if not (border_left and border_right):
                continue
            num_v = 0
            fill_i = -1
            j = i + 1
            while j < h:
                is_v = g[j][left] == c and g[j][right] == c
                inner_bg = all(g[j][k] == bg for k in range(left + 1, right))
                if is_v and inner_bg:
                    num_v += 1
                    if num_v == 2:
                        fill_i = j
                    j += 1
                else:
                    break
            if num_v < 2:
                continue
            if j >= h:
                continue
            is_bottom = all(g[j][left + k] == c for k in range(span))
            bottom_border_left = left == 0 or g[j][left - 1] == bg
            bottom_border_right = right == w - 1 or g[j][right + 1] == bg
            if is_bottom and bottom_border_left and bottom_border_right:
                if fill_i != -1:
                    m = c // 2
                    if c == 1:
                        m = 2 if (start % 2 == 1) else 1
                    for kk in range(1, m + 1):
                        pos = right - 2 * kk
                        if left < pos < right:
                            g[fill_i][pos] = c

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    work_g = [row[:] for row in g]
    small_colors: Set[int] = set()
    erase_small_components(work_g, bg, 12, small_colors)
    detect_and_complete_frames(work_g, bg, small_colors)
    return work_g
```