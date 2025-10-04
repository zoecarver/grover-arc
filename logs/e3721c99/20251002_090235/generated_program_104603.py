```python
from typing import List

def find_components(grid: List[List[int]]) -> List[tuple[int, List[tuple[int, int]]]]:
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0 and not visited[i][j]:
                color = grid[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def compute_holes(grid: List[List[int]], positions: List[tuple[int, int]]) -> int:
    if not positions:
        return 0
    minr = min(r for r, c in positions)
    maxr = max(r for r, c in positions)
    minc = min(c for r, c in positions)
    maxc = max(c for r, c in positions)
    sub_rows = maxr - minr + 3
    sub_cols = maxc - minc + 3
    offset_r = 1
    offset_c = 1
    sub_grid = [[0] * sub_cols for _ in range(sub_rows)]
    comp_set = set(positions)
    for sr in range(1, sub_rows - 1):
        for sc in range(1, sub_cols - 1):
            gr = minr + sr - offset_r
            gc = minc + sc - offset_c
            if 0 <= gr < len(grid) and 0 <= gc < len(grid[0]):
                if (gr, gc) in comp_set:
                    sub_grid[sr][sc] = 1
                elif grid[gr][gc] != 0:
                    sub_grid[sr][sc] = 2
    visited = [[False] * sub_cols for _ in range(sub_rows)]
    queue = []
    for i in range(sub_rows):
        for j in range(sub_cols):
            if (i == 0 or i == sub_rows - 1 or j == 0 or j == sub_cols - 1) and sub_grid[i][j] == 0 and not visited[i][j]:
                queue.append((i, j))
                visited[i][j] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        x, y = queue.pop(0)
        for dx, dy in dirs:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < sub_rows and 0 <= ny < sub_cols and not visited[nx][ny] and sub_grid[nx][ny] == 0:
                visited[nx][ny] = True
                queue.append((nx, ny))
    hole_count = 0
    for sr in range(1, sub_rows - 1):
        for sc in range(1, sub_cols - 1):
            if sub_grid[sr][sc] == 0 and not visited[sr][sc]:
                gr = minr + sr - offset_r
                gc = minc + sc - offset_c
                if 0 <= gr < len(grid) and 0 <= gc < len(grid[0]) and grid[gr][gc] == 0:
                    hole_count += 1
    return hole_count

def get_header_mapping(grid: List[List[int]]) -> dict[int, int]:
    components = find_components(grid)
    candidates = [(colr, pos) for colr, pos in components if colr != 5 and len(pos) >= 5 and min(r for r, _ in pos) <= 4]
    def min_col_key(comp: tuple[int, List[tuple[int, int]]]) -> int:
        _, pos = comp
        return min(c for _, c in pos)
    sorted_candidates = sorted(candidates, key=min_col_key)
    mapping = {}
    idx = 0
    for colr, pos in sorted_candidates:
        h = compute_holes(grid, pos)
        if h == idx:
            mapping[idx] = colr
            idx += 1
    return mapping

def transform_orange_components(grid: List[List[int]], mapping: dict[int, int]) -> List[List[int]]:
    components = find_components(grid)
    output = [row[:] for row in grid]
    for colr, pos in components:
        if colr == 5:
            h = compute_holes(grid, pos)
            if h in mapping:
                new_color = mapping[h]
                for r, c in pos:
                    output[r][c] = new_color
            else:
                for r, c in pos:
                    output[r][c] = 0
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    mapping = get_header_mapping(g)
    return transform_orange_components(g, mapping)
```