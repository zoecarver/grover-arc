```python
from typing import List, Dict, Tuple
from collections import deque

def find_components(g: List[List[int]]) -> List[Dict]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != 0 and not visited[i][j]:
                color = g[i][j]
                pixels = []
                min_r, min_c, max_r, max_c = i, j, i, j
                q = deque([(i, j)])
                visited[i][j] = True
                pixels.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            pixels.append((nx, ny))
                            min_r = min(min_r, nx)
                            min_c = min(min_c, ny)
                            max_r = max(max_r, nx)
                            max_c = max(max_c, ny)
                components.append({
                    'color': color,
                    'pixels': pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return components

def touches_border(bbox: Tuple[int, int, int, int], n: int) -> bool:
    min_r, min_c, max_r, max_c = bbox
    return min_r == 0 or max_r == n - 1 or min_c == 0 or max_c == n - 1

def get_large_color(components: List[Dict]) -> int:
    if not components:
        return 0
    large_comp = max(components, key=lambda comp: len(comp['pixels']))
    return large_comp['color']

def get_growing_colors(components: List[Dict], large_color: int, n: int) -> set:
    growing = set()
    for comp in components:
        if comp['color'] != large_color and touches_border(comp['bbox'], n):
            growing.add(comp['color'])
    return growing

def get_peripheral_pixels(components: List[Dict], growing_colors: set, n: int) -> set:
    peripheral = set()
    for comp in components:
        if comp['color'] in growing_colors and touches_border(comp['bbox'], n):
            peripheral.update(comp['pixels'])
    return peripheral

def get_total_pixels(g: List[List[int]], growing_colors: set) -> Dict[int, int]:
    n = len(g)
    total = {c: 0 for c in growing_colors}
    for i in range(n):
        for j in range(n):
            col = g[i][j]
            if col in total:
                total[col] += 1
    return total

def choose_seed_color(growing_colors: set, total_pixels: Dict[int, int], large_color: int) -> int:
    if not growing_colors:
        return large_color
    return max(growing_colors, key=lambda c: total_pixels.get(c, 0))

def find_remnant_placement(n: int, g: List[List[int]], large_color: int) -> Tuple[int, int]:
    ideal_r = (n - 1) / 2.0
    ideal_c = (n - 1) / 2.0
    best_score = float('inf')
    best_tr = -1
    best_tc = -1
    for tr in range(max(0, n // 2 - 3), min(n - 2, n // 2 + 3)):
        for tc in range(max(0, n // 2 - 3), min(n - 2, n // 2 + 3)):
            positions = [(i, j) for i in range(tr, tr + 3) for j in range(tc, tc + 3)]
            if all(g[i][j] == large_color for i, j in positions):
                score = ((tr + 1 - ideal_r) ** 2 + (tc + 1 - ideal_c) ** 2)
                if score < best_score:
                    best_score = score
                    best_tr = tr
                    best_tc = tc
    return best_tr, best_tc

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    components = find_components(g)
    large_color = get_large_color(components)
    growing_colors = get_growing_colors(components, large_color, n)
    total_pixels = get_total_pixels(g, growing_colors)
    seed_color = choose_seed_color(growing_colors, total_pixels, large_color)
    tr, tc = find_remnant_placement(n, g, large_color)
    protected_set = {(i, j) for i in range(tr, tr + 3) for j in range(tc, tc + 3)}
    center_r = tr + 1
    center_c = tc + 1
    seed_pixels = get_peripheral_pixels(components, growing_colors, n)
    output = [row[:] for row in g]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    q = deque()
    visited = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if (i, j) in protected_set or g[i][j] != large_color:
                visited[i][j] = True
    for i, j in seed_pixels:
        q.append((i, j, g[i][j]))
    while q:
        x, y, col = q.popleft()
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and output[nx][ny] == large_color:
                output[nx][ny] = col
                visited[nx][ny] = True
                q.append((nx, ny, col))
    output[center_r][center_c] = seed_color
    return output
```