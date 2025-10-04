```python
from typing import List

def find_background_color(grid: List[List[int]]) -> int:
    return grid[0][0] if grid else 0

def find_large_shapes(grid: List[List[int]], bg: int) -> List[tuple]:
    larges = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for i in range(rows - 4):
        for j in range(cols - 4):
            c = grid[i][j]
            if c == bg:
                continue
            is_solid = True
            for di in range(5):
                for dj in range(5):
                    if grid[i + di][j + dj] != c:
                        is_solid = False
                        break
                if not is_solid:
                    break
            if is_solid:
                larges.append((i, j, c))
    return larges

def get_min_rc(larges: List[tuple]) -> tuple:
    if not larges:
        return 0, 0
    min_r = min(r for r, _, _ in larges)
    min_c = min(c for _, c, _ in larges)
    return min_r, min_c

def compute_output_dimensions(larges: List[tuple], min_r: int, min_c: int) -> tuple:
    if not larges:
        return 0, 0
    out_rs = [r - min_r + 1 for r, _, _ in larges]
    out_cs = [c - min_c + 1 for _, c, _ in larges]
    max_end_r = max(or_r + 4 for or_r in out_rs)
    max_end_c = max(oc + 4 for oc in out_cs)
    h = max_end_r + 2
    w = max_end_c + 2
    return h, w

def create_empty_grid(h: int, w: int, bg: int) -> List[List[int]]:
    return [[bg] * w for _ in range(h)]

def find_small_components(grid: List[List[int]], color: int, exclude_r: int, exclude_c: int) -> List[List[tuple]]:
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def is_excluded(x: int, y: int) -> bool:
        return exclude_r <= x <= exclude_r + 4 and exclude_c <= y <= exclude_c + 4

    def dfs(start_x: int, start_y: int) -> List[tuple]:
        component = []
        stack = [(start_x, start_y)]
        while stack:
            cx, cy = stack.pop()
            if visited[cx][cy] or grid[cx][cy] != color or is_excluded(cx, cy):
                continue
            visited[cx][cy] = True
            component.append((cx, cy))
            for dx, dy in directions:
                nx = cx + dx
                ny = cy + dy
                if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny]:
                    stack.append((nx, ny))
        return component

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == color and not visited[i][j] and not is_excluded(i, j):
                component = dfs(i, j)
                if component:
                    components.append(component)
    return components

def modify_large_5x5(color: int, components: List[List[tuple]], bg: int) -> List[List[int]]:
    local = [[color] * 5 for _ in range(5)]
    for comp in components:
        if not comp:
            continue
        rs = [r for r, _ in comp]
        cs = [c for _, c in comp]
        min_rx = min(rs)
        max_rx = max(rs)
        min_cx = min(cs)
        max_cx = max(cs)
        h_s = max_rx - min_rx + 1
        w_s = max_cx - min_cx + 1
        start_r = (5 - h_s) // 2
        start_c = (5 - w_s) // 2
        for r, c in comp:
            lrow = r - min_rx
            lcol = c - min_cx
            hr = start_r + lrow
            hc = start_c + lcol
            if 0 <= hr < 5 and 0 <= hc < 5:
                local[hr][hc] = bg
    return local

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    bg = find_background_color(g)
    larges = find_large_shapes(g, bg)
    if not larges:
        return []
    min_r, min_c = get_min_rc(larges)
    h_out, w_out = compute_output_dimensions(larges, min_r, min_c)
    out_grid = create_empty_grid(h_out, w_out, bg)
    for large_r, large_c, color in larges:
        out_r = large_r - min_r + 1
        out_c = large_c - min_c + 1
        components = find_small_components(g, color, large_r, large_c)
        local_5x5 = modify_large_5x5(color, components, bg)
        for di in range(5):
            for dj in range(5):
                out_grid[out_r + di][out_c + dj] = local_5x5[di][dj]
    return out_grid
```