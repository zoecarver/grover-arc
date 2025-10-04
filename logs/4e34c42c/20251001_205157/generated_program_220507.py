```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    return g[0][0]

def find_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if g[r][c] != bg and not visited[r][c]:
                min_r = max_r = r
                min_c = max_c = c
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] != bg:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append((min_r, max_r, min_c, max_c))
    return components

def trim_subgrid(sub: List[List[int]], bg: int) -> List[List[int]]:
    if not sub or not sub[0]:
        return sub
    rows = len(sub)
    cols = len(sub[0])
    start = 0
    while start < cols:
        if all(sub[r][start] == bg for r in range(rows)):
            start += 1
        else:
            break
    end = cols - 1
    while end >= start:
        if all(sub[r][end] == bg for r in range(rows)):
            end -= 1
        else:
            break
    if start > end:
        return [[bg] for _ in range(rows)]
    new_cols = end - start + 1
    new_sub = [[bg for _ in range(new_cols)] for _ in range(rows)]
    for r in range(rows):
        for j in range(new_cols):
            new_sub[r][j] = sub[r][start + j]
    return new_sub

def max_overlap(left: List[List[int]], right: List[List[int]]) -> int:
    if not left or not right or not left[0] or not right[0]:
        return 0
    w1 = len(left[0])
    w2 = len(right[0])
    max_k = min(w1, w2)
    for k in range(max_k, 0, -1):
        match = True
        for row in range(5):
            for j in range(k):
                if left[row][w1 - k + j] != right[row][j]:
                    match = False
                    break
            if not match:
                break
        if match:
            return k
    return 0

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    components = find_components(g, bg)
    subgrids = []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    for min_r, max_r, min_c, max_c in components:
        orig_min_c = min_c
        if min_r < h and max_r < h and min_c < w and max_c < w and g[min_r][min_c] == 9 and g[max_r][min_c] == 9:
            min_c += 1
        if min_c > max_c:
            continue
        h_comp = max_r - min_r + 1
        if h_comp > 5:
            crop_offset = (h_comp - 5) // 2
            r_start = min_r + crop_offset
            num_content_rows = 5
            pad_top = 0
        else:
            crop_offset = 0
            r_start = min_r
            num_content_rows = h_comp
            pad_top = (5 - h_comp) // 2
        width = max_c - min_c + 1
        sub = [[bg for _ in range(width)] for _ in range(5)]
        for j in range(num_content_rows):
            r = r_start + j
            if r >= h:
                break
            for k in range(width):
                c = min_c + k
                if c < w:
                    sub[pad_top + j][k] = g[r][c]
        sub = trim_subgrid(sub, bg)
        if sub and sub[0]:
            subgrids.append((min_r, orig_min_c, sub))
    if not subgrids:
        return [[bg] for _ in range(5)]
    subgrids.sort(key=lambda x: (-x[0], x[1]))
    strip = subgrids[0][2]
    for _, _, next_sub in subgrids[1:]:
        k = max_overlap(strip, next_sub)
        w_s = len(strip[0])
        w_n = len(next_sub[0])
        for r in range(5):
            for j in range(w_n - k):
                strip[r].append(next_sub[r][k + j])
    return strip
```