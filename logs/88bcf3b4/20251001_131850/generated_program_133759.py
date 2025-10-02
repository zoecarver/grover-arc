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

def is_vertical_aligned_component(component: List[Tuple[int, int]]) -> bool:
    if not component:
        return True
    cols = {j for _, j in component}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
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
        components.append(component)
    return components

def find_available_column(out: List[List[int]], n: int, k: int, background: int, target: int) -> int:
    candidates = []
    for col in range(n):
        free = all(out[r][col] == background for r in range(k))
        if free:
            dist = abs(col - target)
            candidates.append((dist, col))
    if candidates:
        candidates.sort(key=lambda x: (x[0], -x[1]))
        return candidates[0][1]
    # fallback to leftmost possible
    for col in range(n):
        free = all(out[r][col] == background for r in range(k))
        if free:
            return col
    return 0

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    out = [[background] * n for _ in range(n)]
    colors = sorted(get_colors(g, background))
    # Preserve all vertical components first
    for color in colors:
        positions = get_positions(g, color)
        components = get_connected_components(g, color, positions, n)
        for component in components:
            if is_vertical_aligned_component(component):
                for i, j in component:
                    out[i][j] = color
    # Collect non-vertical components
    non_vertical = []
    for color in colors:
        positions = get_positions(g, color)
        components = get_connected_components(g, color, positions, n)
        for component in components:
            if not is_vertical_aligned_component(component):
                non_vertical.append((color, component))
    # Sort by decreasing max col, then decreasing size
    non_vertical.sort(key=lambda item: (-max(j for _, j in item[1]), -len(item[1])))
    # Place straightened stacks
    for color, component in non_vertical:
        k = len(component)
        if k == 0:
            continue
        max_col = max(j for _, j in component)
        target = max(0, min(n - 1, max_col))
        chosen_col = find_available_column(out, n, k, background, target)
        for r in range(k):
            if r < n:
                out[r][chosen_col] = color
    return out
```