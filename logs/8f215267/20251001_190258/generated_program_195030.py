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
    for i in range(h - 4):
        for start in range(w):
            if g[i][start] == bg:
                continue
            c = g[i][start]
            if c not in small_colors:
                continue
            # find end of run
            end = start
            while end + 1 < w and g[i][end + 1] == c:
                end += 1
            span = end - start + 1
            if span < 11:
                continue
            left = start
            right = end
            # now v rows
            num_v = 0
            fill_i = -1
            fill_right = -1
            j = i + 1
            current_right = right
            while j < h:
                possible_sides = [k for k in range(left, current_right + 1) if g[j][k] == c]
                if len(possible_sides) != 2:
                    break
                this_left = min(possible_sides)
                this_right = max(possible_sides)
                if this_left != left or abs(this_right - current_right) > 1:
                    break
                inner_bg = all(g[j][k] == bg for k in range(this_left + 1, this_right))
                if not inner_bg:
                    break
                num_v += 1
                if num_v == 2:
                    fill_i = j
                    fill_right = this_right
                if this_right < current_right:
                    current_right = this_right
                j += 1
            if num_v < 2:
                continue
            if j >= h:
                continue
            # check bottom
            bottom_span_start = left
            bottom_span_end = current_right
            is_bottom = all(g[j][k] == c for k in range(bottom_span_start, bottom_span_end + 1))
            if is_bottom and fill_i != -1:
                m = c // 2
                if c == 1:
                    m = 2 if (left % 2 == 1) else 1
                for kk in range(1, m + 1):
                    pos = fill_right - 2 * kk
                    if left < pos < fill_right:
                        g[fill_i][pos] = c

def program(g: List[List[int]]) -> List[List[int]]:
    bg = find_background(g)
    work_g = [row[:] for row in g]
    small_colors: Set[int] = set()
    erase_small_components(work_g, bg, 12, small_colors)
    detect_and_complete_frames(work_g, bg, small_colors)
    return work_g
```