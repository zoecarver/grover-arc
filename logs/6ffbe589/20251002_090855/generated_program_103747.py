```python
import math
from typing import List, Tuple, Dict

def find_components(grid: List[List[int]]) -> List[Dict]:
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != 0 and not visited[i][j]:
                color = grid[i][j]
                stack = [(i, j)]
                positions = []
                min_r, max_r = i, i
                min_c, max_c = j, j
                pixel_count = 0
                while stack:
                    x, y = stack.pop()
                    if visited[x][y]:
                        continue
                    visited[x][y] = True
                    positions.append((x, y))
                    pixel_count += 1
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == color:
                            stack.append((nx, ny))
                components.append({
                    'color': color,
                    'positions': positions,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'pixels': pixel_count
                })
    return components

def compute_centroids(components: List[Dict]) -> List[Tuple[float, float]]:
    centroids = []
    for comp in components:
        min_r, min_c, max_r, max_c = comp['bbox']
        cent_r = (min_r + max_r) / 2.0
        cent_c = (min_c + max_c) / 2.0
        centroids.append((cent_r, cent_c))
    return centroids

def build_meta_graph(components: List[Dict], threshold: float = 5.5) -> List[List[int]]:
    n = len(components)
    if n == 0:
        return []
    centroids = compute_centroids(components)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dr = abs(centroids[i][0] - centroids[j][0])
            dc = abs(centroids[i][1] - centroids[j][1])
            dist = math.sqrt(dr * dr + dc * dc)
            if dist < threshold:
                adj[i].append(j)
                adj[j].append(i)
    return adj

def find_meta_components(adj: List[List[int]], n: int) -> List[List[int]]:
    visited = [False] * n
    meta_comps = []
    for i in range(n):
        if not visited[i]:
            group = []
            stack = [i]
            while stack:
                x = stack.pop()
                if visited[x]:
                    continue
                visited[x] = True
                group.append(x)
                for y in adj[x]:
                    if not visited[y]:
                        stack.append(y)
            meta_comps.append(group)
    return meta_comps

def select_largest_meta(meta_comps: List[List[int]], components: List[Dict]) -> List[Dict]:
    max_pixels = 0
    main_indices = []
    for group in meta_comps:
        total = sum(components[k]['pixels'] for k in group)
        if total > max_pixels:
            max_pixels = total
            main_indices = group
    included = [components[i] for i in main_indices]
    return included

def compute_aggregate_bbox(included: List[Dict]) -> Tuple[int, int, int, int]:
    if not included:
        return 0, 0, 0, 0
    min_r = min(comp['bbox'][0] for comp in included)
    max_r = max(comp['bbox'][2] for comp in included)
    min_c = min(comp['bbox'][1] for comp in included)
    max_c = max(comp['bbox'][3] for comp in included)
    return min_r, max_r, min_c, max_c

def get_included_pixels(included: List[Dict]) -> List[Tuple[int, int, int]]:
    pixels = []
    for comp in included:
        v = comp['color']
        for r, c in comp['positions']:
            pixels.append((r, c, v))
    return pixels

def determine_rotation(colors: set) -> str:
    if 5 in colors:
        return 'cw'
    elif 1 in colors:
        return 'ccw'
    else:
        return '180'

def apply_rotation(pixels: List[Tuple[int, int, int]], min_r: int, min_c: int, h: int, w: int, rotation: str) -> List[List[int]]:
    if rotation == 'cw' or rotation == 'ccw':
        new_h = w
        new_w = h
    else:
        new_h = h
        new_w = w
    new_grid = [[0] * new_w for _ in range(new_h)]
    s_r = h  # for 180
    s_c = w
    for old_r, old_c, v in pixels:
        sr = old_r - min_r
        sc = old_c - min_c
        if rotation == 'cw':
            nr = sc
            nc = new_w - 1 - sr
        elif rotation == 'ccw':
            nr = new_h - 1 - sc
            nc = sr
        else:  # 180
            nr = h - 1 - sr
            nc = w - 1 - sc
        if 0 <= nr < new_h and 0 <= nc < new_w:
            new_grid[nr][nc] = v
    return new_grid

def get_colors(included: List[Dict]) -> set:
    return {comp['color'] for comp in included}

def program(g: List[List[int]]) -> List[List[int]]:
    components = find_components(g)
    adj = build_meta_graph(components)
    meta_comps = find_meta_components(adj, len(components))
    included = select_largest_meta(meta_comps, components)
    if not included:
        return [[]]
    min_r, max_r, min_c, max_c = compute_aggregate_bbox(included)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    pixels = get_included_pixels(included)
    colors_set = get_colors(included)
    rotation = determine_rotation(colors_set)
    new_grid = apply_rotation(pixels, min_r, min_c, h, w, rotation)
    return new_grid
```