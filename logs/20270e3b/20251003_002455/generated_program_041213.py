```python
from typing import List, Tuple, Optional
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h, w = len(g), len(g[0])
    dark_red = find_dark_red_positions(g)
    yellow_components = find_connected_components(g, 4)
    if not yellow_components:
        # No yellow, return empty or all blue, but assume present
        return [[1 for _ in range(w)] for _ in range(h)]
    main_component = max(yellow_components, key=len)
    main_bbox = get_bbox(main_component)
    expanded_bbox = expand_bbox_for_dark_red(main_bbox, dark_red, h, w)
    minr, maxr, minc, maxc = expanded_bbox
    # Crop the grid
    cropped = [row[minc:maxc+1] for row in g[minr:maxr+1]]
    # Replace 7s with 1s
    for r in range(len(cropped)):
        for c in range(len(cropped[r])):
            if cropped[r][c] == 7:
                cropped[r][c] = 1
    # Compute totals
    total_yellow = count_color(g, 4)
    base_yellow = count_color(cropped, 4)
    s = total_yellow - base_yellow
    # Fill s 1s to 4s using BFS dilation from current 4s, limited to s
    cropped = fill_dilation(cropped, s)
    # Adjust blue by contracting around dark red y positions (simple: remove some blue pixels)
    cropped = contract_blue_simple(cropped, [p[0] + minr for p in dark_red if minc <= p[1] <= maxc])
    # For yellow hole adjustment, assume single, no change
    # Conserve yellow already done by filling
    # Decrease blue in expanded areas by turning some 1s to 4s if needed, but already in s
    return cropped

def find_dark_red_positions(grid: List[List[int]]) -> List[Tuple[int, int]]:
    positions = []
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 7:
                positions.append((r, c))
    return positions

def find_connected_components(grid: List[List[int]], color: int) -> List[List[Tuple[int, int]]]:
    h = len(grid)
    if h == 0:
        return []
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if grid[r][c] == color and not visited[r][c]:
                component = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == color and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(component)
    return components

def get_bbox(component: List[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    if not component:
        return None
    rs = [p[0] for p in component]
    cs = [p[1] for p in component]
    return min(rs), max(rs), min(cs), max(cs)

def expand_bbox_for_dark_red(bbox: Tuple[int, int, int, int], dark_red: List[Tuple[int, int]], h: int, w: int) -> Tuple[int, int, int, int]:
    if bbox is None:
        return 0, h - 1, 0, w - 1
    minr, maxr, minc, maxc = bbox
    for r, c in dark_red:
        if minc <= c <= maxc:
            minr = min(minr, r)
            maxr = max(maxr, r)
    return max(0, minr), min(h - 1, maxr), max(0, minc), min(w - 1, maxc)

def count_color(grid: List[List[int]], color: int) -> int:
    return sum(row.count(color) for row in grid)

def fill_dilation(grid: List[List[int]], s: int) -> List[List[int]]:
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    queue = deque()
    turns = 0
    # Start from all current 4s
    for r in range(h):
        for c in range(w):
            if grid[r][c] == 4:
                queue.append((r, c))
                visited[r][c] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue and turns < s:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == 1 and not visited[nx][ny]:
                grid[nx][ny] = 4
                visited[nx][ny] = True
                queue.append((nx, ny))
                turns += 1
                if turns == s:
                    break
    return grid

def contract_blue_simple(grid: List[List[int]], dark_red_rows: List[int]) -> List[List[int]]:
    h = len(grid)
    if h == 0:
        return grid
    w = len(grid[0])
    # Simple contraction: in rows near dark red rows, turn some 1s to 4s or remove, but to simulate decrease, turn random 1s to 4s
    # For simplicity, turn 1s in those rows to 4s up to some number
    for dr in dark_red_rows:
        if 0 <= dr < h:
            count = 0
            for c in range(w):
                if grid[dr][c] == 1 and count < 2:  # arbitrary small number
                    grid[dr][c] = 4
                    count += 1
    return grid
```