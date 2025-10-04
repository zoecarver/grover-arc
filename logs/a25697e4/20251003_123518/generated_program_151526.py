```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    if cols == 0:
        return []
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != background:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def touches_left(component: List[Tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in component)

def touches_bottom(component: List[Tuple[int, int]], rows: int) -> bool:
    return any(r == rows - 1 for r, _ in component)

def get_min_row(component: List[Tuple[int, int]]) -> int:
    return min(r for r, _ in component) if component else float('inf')

def get_max_row(component: List[Tuple[int, int]]) -> int:
    return max(r for r, _ in component) if component else -float('inf')

def has_anchored(components: List[Tuple[int, List[Tuple[int, int]]]], background: int) -> bool:
    for color, comp in components:
        if color != background and touches_left(comp):
            return True
    return False

def get_main_color(components: List[Tuple[int, List[Tuple[int, int]]]], background: int) -> int:
    left_colors = set()
    for color, comp in components:
        if color != background and touches_left(comp):
            left_colors.add(color)
    return list(left_colors)[0] if len(left_colors) == 1 else -1

def get_anchored_subs(components: List[Tuple[int, List[Tuple[int, int]]]], main_color: int) -> List[Tuple[List[Tuple[int, int]], int]]:
    subs = []
    for color, comp in components:
        if color == main_color and touches_left(comp):
            min_r = get_min_row(comp)
            subs.append((comp, min_r))
    subs.sort(key=lambda x: x[1])
    return [sub[0] for sub in subs]

def get_noise_colors(components: List[Tuple[int, List[Tuple[int, int]]]], background: int, main_color: int) -> List[int]:
    noise_set = set()
    for color, comp in components:
        if color != background and color != main_color and not touches_left(comp):
            noise_set.add(color)
    noises = sorted(list(noise_set), key=lambda c: min(get_min_row(comp) for colr, comp in components if colr == c))
    return noises if len(noises) == 2 else []

def count_left_main(g: List[List[int]], row: int, main_color: int, cols: int, background: int) -> int:
    left_size = min(4, cols)
    return sum(1 for j in range(left_size) if g[row][j] == main_color and g[row][j] != background)

def detect_structural_rows(g: List[List[int]], main_color: int, background: int, rows: int, cols: int) -> Tuple[List[int], List[int], List[int], int]:
    full_rows = []
    partial_rows = []
    all_counts = [count_left_main(g, r, main_color, cols, background) for r in range(rows)]
    for r in range(rows):
        cnt = all_counts[r]
        if cnt == 4:
            full_rows.append(r)
        elif cnt == 2:
            partial_rows.append(r)
    if len(full_rows) != 2 or len(partial_rows) != 1:
        return [], [], [], -1
    top, bottom = sorted(full_rows)
    if bottom != top + 3:
        return [], [], [], -1
    middle = partial_rows[0]
    if not (top < middle < bottom):
        return [], [], [], -1
    gap_candidates = [r for r in range(top + 1, bottom) if r != middle and all_counts[r] == 0]
    if len(gap_candidates) != 1:
        return [], [], [], -1
    gap = gap_candidates[0]
    return full_rows, partial_rows, [gap], gap

def assign_inner_outer(noises: List[int], gap: int, middle: int) -> Tuple[int, int]:
    upper_noise, lower_noise = noises
    if gap < middle:
        return upper_noise, lower_noise
    else:
        return lower_noise, upper_noise

def build_background_grid(rows: int, cols: int, bg: int) -> List[List[int]]:
    return [[bg] * cols for _ in range(rows)]

def place_component(grid: List[List[int]], color: int, positions: List[Tuple[int, int]]) -> List[List[int]]:
    for r, c in positions:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            grid[r][c] = color
    return grid

def fill_anchored_pattern(grid: List[List[int]], full_rows: List[int], middle: int, gap: int, main_color: int, inner: int, outer: int, cols: int, bg: int) -> List[List[int]]:
    w = len(grid[0])
    left_size = min(4, w)
    ext_size = min(9, w)
    
    # Fill full rows left with main
    for r in full_rows:
        for j in range(left_size):
            grid[r][j] = main_color
    
    # Fill middle: left 2 main, 2-4 inner (cols 2-3), 4-8 outer
    for j in range(2):
        grid[middle][j] = main_color
    for j in range(2, left_size):
        grid[middle][j] = inner
    for j in range(4, min(9, w)):
        grid[middle][j] = outer
    
    # Fill gap: left 4 inner, col 8 outer if possible
    for j in range(left_size):
        grid[gap][j] = inner
    if w > 8:
        grid[gap][8] = outer
    
    # Extensions for adjacent full rows: col 8-9 outer if adjacent to gap has 0 in left? But simplify to always if w>8
    adj_top = full_rows[0]
    adj_bottom = full_rows[1]
    if w > 8:
        if gap == adj_top + 1:
            grid[adj_top][8] = outer
            if w > 9:
                grid[adj_top][9] = outer
        if gap == adj_bottom - 1:
            grid[adj_bottom][8] = outer
            if w > 9:
                grid[adj_bottom][9] = outer
    
    # Place main subs beyond left if they extend
    # But since we rebuild, assume structural only; for now, just pattern
    
    return grid

def can_shift_component(original_pos: List[Tuple[int, int]], delta_r: int, delta_c: int, rows: int, cols: int, grid: List[List[int]], bg: int) -> bool:
    for r, c in original_pos:
        nr, nc = r + delta_r, c + delta_c
        if not (0 <= nr < rows and 0 <= nc < cols):
            return False
        if grid[nr][nc] != bg:
            return False
    return True

def apply_shift(grid: List[List[int]], color: int, original_pos: List[Tuple[int, int]], delta_r: int, delta_c: int, bg: int) -> List[List[int]]:
    rows = len(grid)
    cols = len(grid[0])
    if can_shift_component(original_pos, delta_r, delta_c, rows, cols, grid, bg):
        # Clear original? No, since we build new grid
        new_pos = [(r + delta_r, c + delta_c) for r, c in original_pos]
        return place_component(grid, color, new_pos)
    else:
        return place_component(grid, color, original_pos)

def apply_unanchored(g: List[List[int]], components: List[Tuple[int, List[Tuple[int, int]]]], bg: int, rows: int, cols: int) -> List[List[int]]:
    out = build_background_grid(rows, cols, bg)
    stayers = []
    movables = []
    for color, comp in components:
        if touches_bottom(comp, rows):
            stayers.append((color, comp))
        else:
            movables.append((color, comp))
    
    # Place stayers first
    for color, comp in stayers:
        place_component(out, color, comp)
    
    # Sort movables by descending min row (bottom first)
    movables.sort(key=lambda x: -get_min_row(x[1]))
    
    # Shift each
    delta_r, delta_c = 1, 6
    for color, comp in movables:
        out = apply_shift(out, color, comp, delta_r, delta_c, bg, rows, cols)
    
    return out

def apply_anchored(g: List[List[int]], components: List[Tuple[int, List[Tuple[int, int]]]], main_color: int, noises: List[int], bg: int, rows: int, cols: int) -> List[List[int]]:
    subs = get_anchored_subs(components, main_color)
    if len(subs) != 2:
        # Fallback: place only main subs on bg
        out = build_background_grid(rows, cols, bg)
        for sub in subs:
            place_component(out, main_color, sub)
        return out
    
    if not noises:
        # Fallback
        out = build_background_grid(rows, cols, bg)
        for sub in subs:
            place_component(out, main_color, sub)
        return out
    
    full_rows, partial_rows, gap_rows, gap = detect_structural_rows(g, main_color, bg, rows, cols)
    if not full_rows or gap == -1:
        # Fallback
        out = build_background_grid(rows, cols, bg)
        for sub in subs:
            place_component(out, main_color, sub)
        return out
    
    middle = partial_rows[0]
    inner, outer = assign_inner_outer(noises, gap, middle)
    
    out = build_background_grid(rows, cols, bg)
    # Place main subs
    for sub in subs:
        place_component(out, main_color, sub)
    
    # Apply pattern fills, overwriting bg but not main? But since rebuild, fill as per pattern
    out = fill_anchored_pattern(out, full_rows, middle, gap, main_color, inner, outer, cols, bg)
    
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    components = find_components(g, bg)
    if has_anchored(components, bg):
        main_color = get_main_color(components, bg)
        if main_color == -1:
            return g  # Multiple mains, copy
        noises = get_noise_colors(components, bg, main_color)
        return apply_anchored(g, components, main_color, noises, bg, rows, cols)
    else:
        return apply_unanchored(g, components, bg, rows, cols)
```