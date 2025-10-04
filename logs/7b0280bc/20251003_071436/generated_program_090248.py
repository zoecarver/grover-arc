```python
from typing import List, Tuple, Dict

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    return [row[:] for row in g]

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def find_components(g: List[List[int]], background: int) -> List[Dict]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = []
    directions: List[Tuple[int, int]] = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(n):
        for j in range(n):
            if not visited[i][j] and g[i][j] != background:
                color = g[i][j]
                component = []
                bbox = [i, i, j, j]
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    bbox[0] = min(bbox[0], x)
                    bbox[1] = max(bbox[1], x)
                    bbox[2] = min(bbox[2], y)
                    bbox[3] = max(bbox[3], y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append({
                    'color': color,
                    'positions': component,
                    'pixels': len(component),
                    'bbox': bbox
                })
    return components

def is_small_tile(comp: Dict) -> bool:
    pixels = comp['pixels']
    bbox = comp['bbox']
    height = bbox[1] - bbox[0] + 1
    width = bbox[3] - bbox[2] + 1
    return pixels <= 4 and height <= 2 and width <= 2

def find_large_frame(components: List[Dict]) -> Dict:
    for comp in components:
        pixels = comp['pixels']
        bbox = comp['bbox']
        height = bbox[1] - bbox[0] + 1
        width = bbox[3] - bbox[2] + 1
        span = max(height, width)
        if 19 <= pixels <= 86 and 10 <= span <= 15:
            return comp
    return None

def bbox_overlap_ratio(small_bbox: List[int], frame_bbox: List[int]) -> float:
    a_min_i, a_max_i, a_min_j, a_max_j = small_bbox
    b_min_i, b_max_i, b_min_j, b_max_j = frame_bbox
    inter_min_i = max(a_min_i, b_min_i)
    inter_max_i = min(a_max_i, b_max_i)
    inter_min_j = max(a_min_j, b_min_j)
    inter_max_j = min(a_max_j, b_max_j)
    if inter_min_i > inter_max_i or inter_min_j > inter_max_j:
        return 0.0
    inter_area = (inter_max_i - inter_min_i + 1) * (inter_max_j - inter_min_j + 1)
    small_area = (a_max_i - a_min_i + 1) * (a_max_j - a_min_j + 1)
    return inter_area / small_area if small_area > 0 else 0.0

def is_lower_position(comp: Dict, n: int) -> bool:
    bbox = comp['bbox']
    center_y = (bbox[0] + bbox[1]) / 2
    return center_y >= n / 2

def is_adjacent_to_background(g: List[List[int]], positions: List[Tuple[int, int]], background: int, n: int) -> bool:
    directions: List[Tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i, j in positions:
        for dx, dy in directions:
            ni = i + dx
            nj = j + dy
            if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == background:
                return True
    return False

def apply_color_change(grid: List[List[int]], comp: Dict, new_color: int):
    for i, j in comp['positions']:
        grid[i][j] = new_color

def rule_orange_from_frame_overlap(grid: List[List[int]], background: int, n: int) -> List[List[int]]:
    components = find_components(grid, background)
    small_tiles = [c for c in components if is_small_tile(c)]
    large_frame = find_large_frame(components)
    if large_frame:
        frame_color = large_frame['color']
        frame_bbox = large_frame['bbox']
        for tile in small_tiles:
            if tile['color'] == frame_color:
                overlap = bbox_overlap_ratio(tile['bbox'], frame_bbox)
                if overlap >= 0.5:
                    apply_color_change(grid, tile, 5)
    return grid

def rule_green_from_lower_position(grid: List[List[int]], background: int, n: int) -> List[List[int]]:
    components = find_components(grid, background)
    small_tiles = [c for c in components if is_small_tile(c)]
    large_frame = find_large_frame(components)
    frame_color = large_frame['color'] if large_frame else -1
    for tile in small_tiles:
        if tile['color'] != frame_color:
            if is_lower_position(tile, n):
                if is_adjacent_to_background(grid, tile['positions'], background, n):
                    apply_color_change(grid, tile, 3)
    return grid

def rule_fill_small_zeros(grid: List[List[int]], background: int, n: int) -> List[List[int]]:
    components = find_components(grid, background)
    zero_tiles = [c for c in components if c['color'] == 0 and is_small_tile(c)]
    for tile in zero_tiles:
        if is_adjacent_to_background(grid, tile['positions'], background, n):
            apply_color_change(grid, tile, 5)
    return grid

def rule_stabilize_large_frame(grid: List[List[int]], background: int) -> List[List[int]]:
    # No change for large frames, already handled by not selecting them as small
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    grid = copy_grid(g)
    grid = rule_orange_from_frame_overlap(grid, background, n)
    grid = rule_green_from_lower_position(grid, background, n)
    grid = rule_fill_small_zeros(grid, background, n)
    grid = rule_stabilize_large_frame(grid, background)
    return grid
```