```python
from collections import deque
from typing import List, Tuple, Dict

def get_size(grid: List[List[int]]) -> Tuple[int, int]:
    if not grid:
        return 0, 0
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    return h, w

def find_connected_components(grid: List[List[int]]) -> Tuple[List[Dict], List[Dict]]:
    h, w = get_size(grid)
    # Non-blue components
    visited = [[False] * w for _ in range(h)]
    components = []
    for i in range(h):
        for j in range(w):
            if not visited[i][j] and grid[i][j] != 1:
                color = grid[i][j]
                positions = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    positions.append((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and grid[nx][ny] == color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                if positions:
                    min_r = min(p[0] for p in positions)
                    max_r = max(p[0] for p in positions)
                    min_c = min(p[1] for p in positions)
                    max_c = max(p[1] for p in positions)
                    components.append({
                        'color': color,
                        'positions': positions,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'size': len(positions)
                    })
    # Blue components
    visited = [[False] * w for _ in range(h)]
    blue_components = []
    for i in range(h):
        for j in range(w):
            if not visited[i][j] and grid[i][j] == 1:
                positions = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    positions.append((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and grid[nx][ny] == 1:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                if positions:
                    min_r = min(p[0] for p in positions)
                    max_r = max(p[0] for p in positions)
                    min_c = min(p[1] for p in positions)
                    max_c = max(p[1] for p in positions)
                    blue_components.append({
                        'color': 1,
                        'positions': positions,
                        'bbox': (min_r, min_c, max_r, max_c),
                        'size': len(positions)
                    })
    return components, blue_components

def bboxes_overlap(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1min, c1min, r1max, c1max = b1
    r2min, c2min, r2max, c2max = b2
    return not (r1max < r2min or r1min > r2max or c1max < c2min or c1min > c2max)

def bboxes_adjacent(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1min, c1min, r1max, c1max = b1
    r2min, c2min, r2max, c2max = b2
    # Check horizontal adjacency
    if (c1max + 1 == c2min or c2max + 1 == c1min) and max(r1min, r2min) <= min(r1max, r2max):
        return True
    # Check vertical adjacency
    if (r1max + 1 == r2min or r2max + 1 == r1min) and max(c1min, c2min) <= min(c1max, c2max):
        return True
    return False

def absorb_small_blues(grid: List[List[int]]) -> List[List[int]]:
    # Rule 1: Absorb small blue components into large regions if bbox overlap/enclosure
    new_grid = [row[:] for row in grid]
    components, blue_components = find_connected_components(grid)
    large_components = [c for c in components if c['size'] > 20 and (c['bbox'][2] - c['bbox'][0] > 5 or c['bbox'][3] - c['bbox'][1] > 5)]
    for blue in [b for b in blue_components if b['size'] <= 4 and (b['bbox'][2] - b['bbox'][0] <= 1 or b['bbox'][3] - b['bbox'][1] <= 1)]:
        for large in sorted(large_components, key=lambda x: x['size'], reverse=True):
            if bboxes_overlap(blue['bbox'], large['bbox']):
                color = large['color']
                for r, c in blue['positions']:
                    new_grid[r][c] = color
                break  # Absorb into the largest overlapping
    return new_grid

def merge_greens(grid: List[List[int]]) -> List[List[int]]:
    # Rule 2: Merge small greens into dominant green, expanding via adjacent/large regions
    new_grid = [row[:] for row in grid]
    components, _ = find_connected_components(grid)
    greens = [c for c in components if c['color'] == 3]
    if not greens:
        return new_grid
    # Union all green bboxes and fill (simple expansion to connect)
    min_r = min(g['bbox'][0] for g in greens)
    max_r = max(g['bbox'][2] for g in greens)
    min_c = min(g['bbox'][1] for g in greens)
    max_c = max(g['bbox'][3] for g in greens)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            new_grid[r][c] = 3
    return new_grid

def merge_pink_darkred(grid: List[List[int]]) -> List[List[int]]:
    # Rule 3: Merge pink (6) and dark red (7) if adjacent/overlap, smaller to larger
    new_grid = [row[:] for row in grid]
    components, _ = find_connected_components(grid)
    pinks = [c for c in components if c['color'] == 6]
    darkreds = [c for c in components if c['color'] == 7]
    for pink in pinks:
        for darkred in darkreds:
            if bboxes_adjacent(pink['bbox'], darkred['bbox']) or bboxes_overlap(pink['bbox'], darkred['bbox']):
                if pink['size'] <= darkred['size']:
                    color = 7
                    positions = pink['positions']
                else:
                    color = 6
                    positions = darkred['positions']
                for r, c in positions:
                    new_grid[r][c] = color
    return new_grid

def expand_maroon(grid: List[List[int]]) -> List[List[int]]:
    # Rule 4: Expand maroon (8) vertically
    h, w = get_size(grid)
    new_grid = [row[:] for row in grid]
    components, _ = find_connected_components(grid)
    maroons = [c for c in components if c['color'] == 8]
    for maroon in maroons:
        min_r, min_c, max_r, max_c = maroon['bbox']
        new_min_r = max(0, min_r - 1)
        new_max_r = min(h - 1, max_r + 1)
        for r in range(new_min_r, new_max_r + 1):
            for c in range(min_c, max_c + 1):
                new_grid[r][c] = 8
    return new_grid

def fill_holes(grid: List[List[int]]) -> List[List[int]]:
    # Rule 5: Fill holes by filling bboxes of large components (ensures no holes)
    new_grid = [row[:] for row in grid]
    components, _ = find_connected_components(grid)
    for comp in sorted(components, key=lambda x: x['size'], reverse=True):
        if comp['size'] > 20:  # Large only
            min_r, min_c, max_r, max_c = comp['bbox']
            color = comp['color']
            h, w = get_size(new_grid)
            for r in range(max(0, min_r), min(h, max_r + 1)):
                for c in range(max(0, min_c), min(w, max_c + 1)):
                    new_grid[r][c] = color
    return new_grid

def transpose_grid(grid: List[List[int]]) -> List[List[int]]:
    # Transpose to swap dimensions
    h, w = get_size(grid)
    new_grid = [[0] * h for _ in range(w)]
    for i in range(w):
        for j in range(h):
            new_grid[i][j] = grid[j][i]
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    # Compose the rules
    grid = absorb_small_blues(grid)
    grid = merge_greens(grid)
    grid = merge_pink_darkred(grid)
    grid = expand_maroon(grid)
    grid = fill_holes(grid)
    # Final transpose
    return transpose_grid(grid)
```