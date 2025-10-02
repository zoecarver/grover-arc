```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    rows = len(g)
    cols = len(g[0])
    bg = g[0][0]

    def find_indicator_column() -> int:
        max_count = 0
        best_c = -1
        for c in range(cols):
            ind_rs = [r for r in range(rows) if g[r][c] != 0 and g[r][c] != bg]
            if ind_rs:
                isolated = all(ind_rs[i] != ind_rs[i - 1] + 1 for i in range(1, len(ind_rs)))
                if isolated and len(ind_rs) > max_count:
                    max_count = len(ind_rs)
                    best_c = c
        return best_c

    c_ind = find_indicator_column()
    if c_ind == -1:
        return [[0]]

    ind_rs = [r for r in range(rows) if g[r][c_ind] != 0 and g[r][c_ind] != bg]
    ind_colors = [g[r][c_ind] for r in ind_rs]
    num_ind = len(ind_rs)
    if num_ind == 0:
        return [[0]]

    min_r = min(ind_rs)
    max_r = max(ind_rs)
    s = max(0, min_r - 1)
    e = min(rows - 1, max_r + 1)

    l = c_ind
    r = c_ind

    def can_expand(cand: int, s: int, e: int, bg: int) -> bool:
        if cand < 0 or cand >= cols:
            return False
        segment = [g[row][cand] for row in range(s, e + 1)]
        has_non_bg_nonzero = any(val != bg and val != 0 for val in segment)
        has_zero = any(val == 0 for val in segment)
        return not has_non_bg_nonzero and has_zero

    while l > 0:
        if can_expand(l - 1, s, e, bg):
            l -= 1
        else:
            break

    while r < cols - 1:
        if can_expand(r + 1, s, e, bg):
            r += 1
        else:
            break

    strip_l = l
    strip_r = r
    width = strip_r - strip_l + 1
    height = 2 * num_ind + 1
    output = [[0] * width for _ in range(height)]

    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def count_components(color: int) -> int:
        visited = [[False] * cols for _ in range(rows)]
        count = 0

        def dfs(start_r: int, start_c: int) -> bool:
            stack = [(start_r, start_c)]
            while stack:
                rr, cc = stack.pop()
                if (not (0 <= rr < rows and 0 <= cc < cols) or
                    visited[rr][cc] or g[rr][cc] != color):
                    continue
                if s <= rr <= e and strip_l <= cc <= strip_r:
                    return False
                visited[rr][cc] = True
                for dr, dc in dirs:
                    stack.append((rr + dr, cc + dc))
            return True

        for rr in range(rows):
            for cc in range(cols):
                if (g[rr][cc] == color and not visited[rr][cc] and
                    not (s <= rr <= e and strip_l <= cc <= strip_r)):
                    if dfs(rr, cc):
                        count += 1
        return count

    for i in range(num_ind):
        color = ind_colors[i]
        cnt = count_components(color)
        out_row = 2 * i + 1
        for j in range(cnt):
            pos = 2 * j + 1
            if pos < width:
                output[out_row][pos] = color

    return output
```