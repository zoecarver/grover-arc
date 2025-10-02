```python
from typing import List, Tuple, Set
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_colors(g: List[List[int]], background: int) -> set:
    colors = set()
    for row in g:
        for cell in row:
            if cell != background:
                colors.add(cell)
    return colors

def get_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    n = len(g)
    return [(i, j) for i in range(n) for j in range(n) if g[i][j] == color]

def get_connected_components(g: List[List[int]], color: int, all_positions: List[Tuple[int, int]], n: int) -> List[List[Tuple[int, int]]]:
    visited: Set[Tuple[int, int]] = set()
    components: List[List[Tuple[int, int]]] = []
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for start_pos in all_positions:
        if start_pos in visited:
            continue
        component = []
        stack = [start_pos]
        visited.add(start_pos)
        while stack:
            x, y = stack.pop()
            component.append((x, y))
            for dx, dy in deltas:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == color and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append((nx, ny))
        if component:
            components.append(component)
    return components

def is_vertical_aligned_component(component: List[Tuple[int, int]]) -> bool:
    if not component:
        return True
    cols = {j for _, j in component}
    if len(cols) != 1:
        return False
    rows = sorted(i for i, _ in component)
    if len(rows) != len(component):
        return False
    for idx in range(1, len(rows)):
        if rows[idx] != rows[idx - 1] + 1:
            return False
    return True

def get_average_col(component: List[Tuple[int, int]]) -> float:
    if not component:
        return 0.0
    cols = [j for _, j in component]
    return sum(cols) / len(cols)

def preserve_positions(out: List[List[int]], component: List[Tuple[int, int]], color: int) -> None:
    for i, j in component:
        out[i][j] = color

def place_vertical_stack(out: List[List[int]], color: int, col: int, k: int, n: int) -> None:
    for r in range(k):
        if r < n:
            out[r][col] = color

def find_available_column(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    best_dist = float('inf')
    best_col = -1
    for c in range(n):
        if all(out[r][c] == background for r in range(min(k, n))):
            dist = abs(c - target)
            if dist < best_dist or (dist == best_dist and (best_col == -1 or c < best_col)):
                best_dist = dist
                best_col = c
    if best_col == -1:
        best_dist = float('inf')
        best_col = -1
        max_free = -1
        for c in range(n):
            free = 0
            for r in range(n):
                if out[r][c] == background:
                    free += 1
                else:
                    break
            dist = abs(c - target)
            if free >= max_free or (free > 0 and max_free == -1):
                if dist < best_dist or (dist == best_dist and c < best_col):
                    best_dist = dist
                    max_free = free
                    best_col = c
    return best_col if best_col != -1 else (target % n)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    out = [[background for _ in range(n)] for _ in range(n)]
    colors = sorted(get_colors(g, background))
    for color in colors:
        positions = get_positions(g, color)
        components = get_connected_components(g, color, positions, n)
        for comp in components:
            if len(comp) <= 3 or is_vertical_aligned_component(comp):
                preserve_positions(out, comp, color)
    large_components = []
    for color in colors:
        positions = get_positions(g, color)
        components = get_connected_components(g, color, positions, n)
        for comp in components:
            if len(comp) > 3 and not is_vertical_aligned_component(comp):
                min_r = min(i for i, _ in comp)
                large_components.append((min_r, color, comp))
    large_components.sort(key=lambda x: x[0])
    for min_r, color, comp in large_components:
        k = len(comp)
        avg = get_average_col(comp)
        target = round(avg)
        col = find_available_column(n, k, out, background, target)
        place_vertical_stack(out, color, col, k, n)
    return out
```