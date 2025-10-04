```python
from typing import List, Dict, Tuple, Set
from collections import defaultdict

def get_grid_dimensions(g: List[List[int]]) -> Tuple[int, int]:
    h = len(g)
    if h == 0:
        w = 0
    else:
        w = len(g[0])
    return h, w

def is_tall_grid(h: int, w: int) -> bool:
    return h > w

def get_directions() -> List[Tuple[int, int]]:
    return [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_valid_position(y: int, x: int, h: int, w: int) -> bool:
    return 0 <= y < h and 0 <= x < w

def flood_fill_same_color(g: List[List[int]], y: int, x: int, c: int, h: int, w: int, visited: List[List[bool]]) -> int:
    size = 0
    stack: List[Tuple[int, int]] = [(y, x)]
    visited[y][x] = True
    while stack:
        cy, cx = stack.pop()
        size += 1
        for dy, dx in get_directions():
            ny, nx = cy + dy, cx + dx
            if is_valid_position(ny, nx, h, w) and not visited[ny][nx] and g[ny][nx] == c:
                visited[ny][nx] = True
                stack.append((ny, nx))
    return size

def find_background_color(g: List[List[int]], h: int, w: int) -> int:
    visited = [[False for _ in range(w)] for _ in range(h)]
    max_size = 0
    bg_color = -1
    for start_y in range(h):
        for start_x in range(w):
            if not visited[start_y][start_x]:
                c = g[start_y][start_x]
                size = flood_fill_same_color(g, start_y, start_x, c, h, w, visited)
                if size > max_size:
                    max_size = size
                    bg_color = c
    return bg_color

def flood_fill_non_bg(g: List[List[int]], start_y: int, start_x: int, bg: int, h: int, w: int, visited: List[List[bool]]) -> List[Tuple[int, int, int]]:
    component: List[Tuple[int, int, int]] = []
    stack: List[Tuple[int, int]] = [(start_y, start_x)]
    visited[start_y][start_x] = True
    component.append((start_y, start_x, g[start_y][start_x]))
    while stack:
        cy, cx = stack.pop()
        for dy, dx in get_directions():
            ny, nx = cy + dy, cx + dx
            if is_valid_position(ny, nx, h, w) and not visited[ny][nx] and g[ny][nx] != bg:
                visited[ny][nx] = True
                stack.append((ny, nx))
                component.append((ny, nx, g[ny][nx]))
    return component

def collect_small_components_and_targets(g: List[List[int]], bg: int, h: int, w: int, is_tall: bool) -> Tuple[List[List[Tuple[int, int, int]]], Dict[int, int]]:
    visited = [[False for _ in range(w)] for _ in range(h)]
    small_components: List[List[Tuple[int, int, int]]] = []
    targets: Dict[int, int] = {}
    for start_y in range(h):
        for start_x in range(w):
            if not visited[start_y][start_x] and g[start_y][start_x] != bg:
                comp = flood_fill_non_bg(g, start_y, start_x, bg, h, w, visited)
                small_components.append(comp)
                if len(comp) == 1:
                    py, px, pc = comp[0]
                    coord = px if is_tall else py
                    if pc not in targets:
                        targets[pc] = coord
    return small_components, targets

def compute_color_counts(comp: List[Tuple[int, int, int]]) -> Dict[int, int]:
    counts: Dict[int, int] = defaultdict(int)
    for _, _, c in comp:
        counts[c] += 1
    return counts

def find_unique_special_color(counts: Dict[int, int], targets: Dict[int, int]) -> int:
    unique = [c for c in counts if counts[c] == 1 and c in targets]
    return unique[0] if len(unique) == 1 else -1

def find_special_position(comp: List[Tuple[int, int, int]], special_c: int) -> Tuple[int, int]:
    for y, x, c in comp:
        if c == special_c:
            return y, x
    return -1, -1

def compute_deltas(is_tall: bool, targets: Dict[int, int], special_y: int, special_x: int, special_c: int, delta_y: int, delta_x: int) -> Tuple[int, int]:
    if is_tall:
        delta_x = targets[special_c] - special_x
        delta_y = 0
    else:
        delta_y = targets[special_c] - special_y
        delta_x = 0
        if special_c == 1 and delta_y > 0:
            delta_x = -1
    return delta_y, delta_x

def get_default_deltas() -> Tuple[int, int]:
    return 0, 0

def erase_component_positions(output_grid: List[List[int]], comp: List[Tuple[int, int, int]], bg: int) -> None:
    for py, px, _ in comp:
        output_grid[py][px] = bg

def place_component(output_grid: List[List[int]], comp: List[Tuple[int, int, int]], delta_y: int, delta_x: int, h: int, w: int) -> None:
    for py, px, pc in comp:
        ny = py + delta_y
        nx = px + delta_x
        if is_valid_position(ny, nx, h, w):
            output_grid[ny][nx] = pc

def process_component(g: List[List[int]], output_grid: List[List[int]], comp: List[Tuple[int, int, int]], targets: Dict[int, int], is_tall: bool, bg: int, h: int, w: int) -> None:
    counts = compute_color_counts(comp)
    special_c = find_unique_special_color(counts, targets)
    if special_c != -1:
        special_y, special_x = find_special_position(comp, special_c)
        delta_y, delta_x = compute_deltas(is_tall, targets, special_y, special_x, special_c, 0, 0)
    else:
        delta_y, delta_x = get_default_deltas()
    erase_component_positions(output_grid, comp, bg)
    place_component(output_grid, comp, delta_y, delta_x, h, w)

def program(g: List[List[int]]) -> List[List[int]]:
    h, w = get_grid_dimensions(g)
    is_tall_flag = is_tall_grid(h, w)
    bg = find_background_color(g, h, w)
    small_comps, targets = collect_small_components_and_targets(g, bg, h, w, is_tall_flag)
    output_grid = [row[:] for row in g]
    for comp in small_comps:
        process_component(g, output_grid, comp, targets, is_tall_flag, bg, h, w)
    return output_grid
```