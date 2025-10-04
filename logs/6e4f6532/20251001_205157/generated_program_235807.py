```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [g[i][j] for i in range(len(g)) for j in range(len(g[0]))]
    count = Counter(flat)
    return count.most_common(1)[0][0] if count else 0

def find_and_fill_small_components(g: List[List[int]], bg: int, min_r: int, max_r: int, min_c: int, max_c: int) -> List[List[int]]:
    height, width = len(g), len(g[0])
    out = [row[:] for row in g]
    visited = [[False] * width for _ in range(height)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(min_r, max_r + 1):
        for j in range(min_c, max_c + 1):
            if not visited[i][j] and out[i][j] != bg:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if min_r <= nx <= max_r and min_c <= ny <= max_c and 0 <= ny < width and not visited[nx][ny] and out[nx][ny] != bg:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(component) < 3:
                    for x, y in component:
                        out[x][y] = bg
    return out

def apply_gravity_up(g: List[List[int]], bg: int, fixed_top: int) -> List[List[int]]:
    height, width = len(g), len(g[0])
    out = [row[:] for row in g]
    changed = True
    passes = 0
    max_passes = height
    while changed and passes < max_passes:
        changed = False
        for r in range(fixed_top + 1, height):
            for c in range(width):
                if out[r][c] != bg and r - 1 >= fixed_top and out[r - 1][c] == bg:
                    out[r - 1][c], out[r][c] = out[r][c], out[r - 1][c]
                    changed = True
        passes += 1
    return out

def apply_gravity_down(g: List[List[int]], bg: int, fixed_bottom: int) -> List[List[int]]:
    height, width = len(g), len(g[0])
    out = [row[:] for row in g]
    changed = True
    passes = 0
    max_passes = height
    while changed and passes < max_passes:
        changed = False
        for r in range(height - 2, fixed_bottom - 1, -1):
            for c in range(width):
                if out[r][c] != bg and r + 1 < height - fixed_bottom + fixed_bottom and out[r + 1][c] == bg:
                    out[r + 1][c], out[r][c] = out[r][c], out[r + 1][c]
                    changed = True
        passes += 1
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    height = len(g)
    width = len(g[0])
    bg = get_background(g)
    fixed_top = 2
    fixed_bottom = 2
    content_min_r = fixed_top
    content_max_r = height - fixed_bottom - 1
    content_min_c = 2
    content_max_c = width - 3
    out = find_and_fill_small_components(g, bg, content_min_r, content_max_r, content_min_c, content_max_c)
    if height <= 16:
        out = apply_gravity_up(out, bg, fixed_top)
    else:
        out = apply_gravity_down(out, bg, fixed_bottom)
    return out
```