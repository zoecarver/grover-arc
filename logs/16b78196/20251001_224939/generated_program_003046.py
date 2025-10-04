```python
from typing import List, Tuple

def find_connected_components(grid: List[List[int]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and not visited[r][c]:
                color = grid[r][c]
                component = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    component.append((cr, cc))
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append((color, component))
    return components

def find_large_polyomino(components: List[Tuple[int, List[Tuple[int, int]]]]) -> Tuple[int, List[Tuple[int, int]]]:
    if not components:
        return (0, [])
    max_comp = max(components, key=lambda x: len(x[1]))
    return max_comp

def clear_non_large_pixels(grid: List[List[int]], large: Tuple[int, List[Tuple[int, int]]]) -> None:
    large_positions = set(large[1])
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in large_positions:
                grid[r][c] = 0

def find_small_polyominoes(components: List[Tuple[int, List[Tuple[int, int]]]], large: Tuple[int, List[Tuple[int, int]]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    large_size = len(large[1])
    smalls = [comp for comp in components if comp != large and len(comp[1]) < large_size // 2 and len(comp[1]) >= 2]
    return smalls

def calculate_center(comp: Tuple[int, List[Tuple[int, int]]]) -> Tuple[float, float]:
    positions = comp[1]
    n = len(positions)
    if n == 0:
        return 0.0, 0.0
    sum_r = sum(p[0] for p in positions)
    sum_c = sum(p[1] for p in positions)
    return sum_r / n, sum_c / n

def group_by_x_position(smalls: List[Tuple[int, List[Tuple[int, int]]]]) -> List[List[Tuple[int, List[Tuple[int, int]]]]]:
    left = []
    right = []
    for comp in smalls:
        _, avg_c = calculate_center(comp)
        if avg_c < 15:
            left.append(comp)
        else:
            right.append(comp)
    groups = [left] if left else []
    if right:
        groups.append(right)
    return groups

def sort_by_color(group: List[Tuple[int, List[Tuple[int, int]]]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    return sorted(group, key=lambda comp: (comp[0], calculate_center(comp)[0]))

def get_stack_center_x(group_index: int) -> float:
    return 6.0 if group_index == 0 else 17.5

def get_target_center_y(large_positions: List[Tuple[int, int]], group_index: int, order: int, comp_height: float) -> float:
    min_r = min(p[0] for p in large_positions)
    max_r = max(p[0] for p in large_positions)
    large_center = (min_r + max_r) / 2.0
    offset = 6.0 + order * 4.0
    if group_index == 0:
        return large_center - offset
    return large_center + offset

def translate_component(comp: Tuple[int, List[Tuple[int, int]]], target_r: float, target_c: float) -> List[Tuple[int, int]]:
    positions = comp[1]
    input_r, input_c = calculate_center(comp)
    shift_r = target_r - input_r
    shift_c = target_c - input_c
    new_positions = [(round(p[0] + shift_r), round(p[1] + shift_c)) for p in positions]
    return new_positions

def place_component(grid: List[List[int]], color: int, positions: List[Tuple[int, int]]) -> None:
    rows = len(grid)
    cols = len(grid[0])
    for r, c in positions:
        if 0 <= r < rows and 0 <= c < cols:
            grid[r][c] = color

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    components = find_connected_components(grid)
    large = find_large_polyomino(components)
    clear_non_large_pixels(grid, large)
    smalls = find_small_polyominoes(components, large)
    groups = group_by_x_position(smalls)
    large_positions = large[1]
    for gi, group in enumerate(groups):
        sorted_group = sort_by_color(group)
        stack_center_x = get_stack_center_x(gi)
        for oi, comp in enumerate(sorted_group):
            comp_center_r, _ = calculate_center(comp)
            target_center_r = get_target_center_y(large_positions, gi, oi, comp_center_r - min(p[0] for p in comp[1]))
            new_pos = translate_component(comp, target_center_r, stack_center_x)
            place_component(grid, comp[0], new_pos)
    return grid
```