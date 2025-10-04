```python
from typing import List, Tuple, Dict
import math

def find_components(grid: List[List[int]]) -> List[Dict]:
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
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
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
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
                            visited[nx][ny] = True
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

def build_meta_graph(components: List[Dict], threshold: float = 6.0) -> List[List[int]]:
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
    if not meta_comps:
        return []
    max_pixels = 0
    main_indices = []
    for group in meta_comps:
        total = sum(components[k]['pixels'] for k in group)
        if total > max_pixels:
            max_pixels = total
            main_indices = group
    return [components[i] for i in main_indices]

def determine_rotation(colors: set) -> str:
    if 5 in colors:
        return 'cw'
    elif 1 in colors:
        return 'ccw'
    else:
        return 'none'

def apply_rotation(pixels: List[Tuple[int, int, int]], min_r: int, min_c: int, h: int, w: int, rotation: str) -> List[List[int]]:
    if h <= 0 or w <= 0:
        return []
    if rotation in ('cw', 'ccw'):
        new_h = w
        new_w = h
    else:
        new_h = h
        new_w = w
    new_grid = [[0] * new_w for _ in range(new_h)]
    for old_r, old_c, v in pixels:
        sr = old_r - min_r
        sc = old_c - min_c
        if rotation == 'none':
            nr = sr
            nc = sc
        elif rotation == 'cw':
            nr = sc
            nc = new_w - 1 - sr
        elif rotation == 'ccw':
            nr = new_h - 1 - sc
            nc = sr
        else:  # Fallback, though not used
            nr = sr
            nc = sc
        if 0 <= nr < new_h and 0 <= nc < new_w:
            new_grid[nr][nc] = v
    return new_grid

def pad_to_square(grid: List[List[int]]) -> List[List[int]]:
    if not grid or not grid[0]:
        return [[0]]
    rh = len(grid)
    rw = len(grid[0])
    n = max(rh, rw)
    if n == 0:
        return [[0]]
    padded = [[0] * n for _ in range(n)]
    pad_r = (n - rh) // 2
    pad_c = (n - rw) // 2
    for i in range(rh):
        for j in range(rw):
            if pad_r + i < n and pad_c + j < n:
                padded[pad_r + i][pad_c + j] = grid[i][j]
    return padded

def program(g: List[List[int]]) -> List[List[int]]:
    components = find_components(g)
    if not components:
        return [[0]]
    adj = build_meta_graph(components)
    n = len(components)
    meta_comps = find_meta_components(adj, n)
    included = select_largest_meta(meta_comps, components)
    pixels = []
    for comp in included:
        for r, c in comp['positions']:
            pixels.append((r, c, g[r][c]))
    if not pixels:
        return [[0]]
    min_r = min(r for r, _, _ in pixels)
    max_r = max(r for r, _, _ in pixels)
    min_c = min(c for _, c, _ in pixels)
    max_c = max(c for _, c, _ in pixels)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    colors = set(v for _, _, v in pixels)
    rotation = determine_rotation(colors)
    rotated = apply_rotation(pixels, min_r, min_c, h, w, rotation)
    return pad_to_square(rotated)
```