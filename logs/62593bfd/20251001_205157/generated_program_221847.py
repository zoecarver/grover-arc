```python
from typing import List, Tuple, Dict
from collections import namedtuple

Component = namedtuple('Component', ['color', 'cells', 'miny', 'maxy', 'minx', 'maxx', 'pixels'])

def identify_components(grid: List[List[int]]) -> List[Component]:
    H = len(grid)
    if H == 0:
        return []
    W = len(grid[0])
    visited = [[False] * W for _ in range(H)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(H):
        for j in range(W):
            if not visited[i][j] and grid[i][j] != 0:
                color = grid[i][j]
                cells = []
                stack = [(i, j)]
                visited[i][j] = True
                cells.append((i, j))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < H and 0 <= ny < W and not visited[nx][ny] and grid[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            cells.append((nx, ny))
                if cells:
                    min_r = min(r for r, _ in cells)
                    max_r = max(r for r, _ in cells)
                    min_c = min(c for _, c in cells)
                    max_c = max(c for _, c in cells)
                    pixels = len(cells)
                    components.append(Component(color, cells, min_r, max_r, min_c, max_c, pixels))
    return components

def has_large_canvas(comps: List[Component], total_cells: int) -> bool:
    if not comps:
        return False
    max_pixels = max(c.pixels for c in comps)
    return max_pixels > total_cells // 4

def get_canvas_color(comps: List[Component]) -> int:
    if not comps:
        return 0
    return max(comps, key=lambda c: c.pixels).color

def sort_key_comp(c: Component) -> Tuple[int, int]:
    return (-c.minx, -c.pixels)

def place_components_parity(comps: List[Component], H: int, W: int) -> List[Tuple[Component, int]]:
    odd_comps = [c for c in comps if c.color % 2 == 1]
    even_comps = [c for c in comps if c.color % 2 == 0]
    odd_comps.sort(key=sort_key_comp)
    even_comps.sort(key=sort_key_comp)
    occupied_top = [[False] * W for _ in range(H)]
    occupied_bottom = [[False] * W for _ in range(H)]
    placements = []
    # Place odd to top
    for comp in odd_comps:
        shift = -comp.miny
        new_cells = [(r + shift, col) for r, col in comp.cells]
        if all(0 <= nr < H and not occupied_top[nr][col] for nr, col in new_cells):
            placements.append((comp, shift))
            for nr, col in new_cells:
                occupied_top[nr][col] = True
        else:
            # Fallback: place anyway (assume no conflict in practice)
            placements.append((comp, shift))
            for nr, col in new_cells:
                if 0 <= nr < H:
                    occupied_top[nr][col] = True
    # Place even to bottom
    for comp in even_comps:
        shift = H - 1 - comp.maxy
        new_cells = [(r + shift, col) for r, col in comp.cells]
        if all(0 <= nr < H and not occupied_bottom[nr][col] for nr, col in new_cells):
            placements.append((comp, shift))
            for nr, col in new_cells:
                occupied_bottom[nr][col] = True
        else:
            # Fallback: place anyway
            placements.append((comp, shift))
            for nr, col in new_cells:
                if 0 <= nr < H:
                    occupied_bottom[nr][col] = True
    return placements

def place_components_ordered(small_comps: List[Component], H: int, W: int) -> List[Tuple[Component, int]]:
    small_comps = sorted(small_comps, key=sort_key_comp)
    occupied_top = [[False] * W for _ in range(H)]
    occupied_bottom = [[False] * W for _ in range(H)]
    placements = []
    for comp in small_comps:
        # Try top
        shift_top = -comp.miny
        new_cells_top = [(r + shift_top, col) for r, col in comp.cells]
        conflict_top = any(nr < 0 or nr >= H or occupied_top[nr][col] for nr, col in new_cells_top)
        if not conflict_top:
            placements.append((comp, shift_top))
            for nr, col in new_cells_top:
                occupied_top[nr][col] = True
            continue
        # Try bottom
        shift_bottom = H - 1 - comp.maxy
        new_cells_bottom = [(r + shift_bottom, col) for r, col in comp.cells]
        conflict_bottom = any(nr < 0 or nr >= H or occupied_bottom[nr][col] for nr, col in new_cells_bottom)
        # Place to bottom (assume no conflict or fallback)
        placements.append((comp, shift_bottom))
        for nr, col in new_cells_bottom:
            if 0 <= nr < H:
                occupied_bottom[nr][col] = True
    return placements

def program(g: List[List[int]]) -> List[List[int]]:
    H = len(g)
    if H == 0:
        return []
    W = len(g[0])
    total_cells = H * W
    comps = identify_components(g)
    has_canvas_flag = has_large_canvas(comps, total_cells)
    if not has_canvas_flag:
        placements = place_components_parity(comps, H, W)
        out = [[0] * W for _ in range(H)]
    else:
        canvas_color = get_canvas_color(comps)
        small_comps = [c for c in comps if c.pixels != max((cc.pixels for cc in comps), default=0)]
        placements = place_components_ordered(small_comps, H, W)
        out = [row[:] for row in g]
        small_positions = set()
        for c in small_comps:
            for r, col in c.cells:
                small_positions.add((r, col))
        for r, col in small_positions:
            out[r][col] = canvas_color
    # Apply placements
    for comp, shift in placements:
        for r, col in comp.cells:
            nr = r + shift
            if 0 <= nr < H:
                out[nr][col] = comp.color
    return out
```