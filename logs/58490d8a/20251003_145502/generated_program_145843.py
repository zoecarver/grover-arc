```python
from typing import List

def count_outside_components(g: List[List[int]], v: int, minr: int, minc: int, maxr: int, maxc: int, N: int, M: int) -> int:
    if v == 0:
        return 0
    visited = [[False] * M for _ in range(N)]
    count = 0
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(N):
        for c in range(M):
            if g[r][c] == v and not visited[r][c] and not (minr <= r <= maxr and minc <= c <= maxc):
                count += 1
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in dirs:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < N and 0 <= nc < M and not visited[nr][nc] and g[nr][nc] == v and not (minr <= nr <= maxr and minc <= nc <= maxc):
                            visited[nr][nc] = True
                            stack.append((nr, nc))
    return count

def get_pattern_colors(g: List[List[int]], minr: int, minc: int, maxr: int, maxc: int) -> List[int]:
    h = maxr - minr + 1
    pattern_colors = []
    for i in range(1, h, 2):
        r = minr + i
        found = 0
        for cc in range(minc, maxc + 1):
            val = g[r][cc]
            if val != 0:
                found = val
                break
        pattern_colors.append(found)
    return pattern_colors

def find_zero_bounds(g: List[List[int]]) -> tuple:
    N = len(g)
    if N == 0:
        return 0, 0, -1, -1
    M = len(g[0])
    min_r = N
    max_r = -1
    min_c = M
    max_c = -1
    for r in range(N):
        for c in range(M):
            if g[r][c] == 0:
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    return min_r, min_c, max_r, max_c

def program(g: List[List[int]]) -> List[List[int]]:
    N = len(g)
    if N == 0:
        return []
    M = len(g[0])
    minr, minc, maxr, maxc = find_zero_bounds(g)
    if maxr < 0:
        return []
    h = maxr - minr + 1
    w = maxc - minc + 1
    pattern_colors = get_pattern_colors(g, minr, minc, maxr, maxc)
    out_grid = [[0] * w for _ in range(h)]
    num_patterns = len(pattern_colors)
    for pi in range(num_patterns):
        c = pattern_colors[pi]
        if c == 0:
            continue
        out_row = 2 * pi + 1
        if out_row >= h:
            break
        k = count_outside_components(g, c, minr, minc, maxr, maxc, N, M)
        max_k = w // 2
        for jj in range(min(k, max_k)):
            col = 2 * jj + 1
            if col < w:
                out_grid[out_row][col] = c
    return out_grid
```