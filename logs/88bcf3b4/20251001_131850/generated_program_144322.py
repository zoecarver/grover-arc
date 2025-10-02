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
    rows = sorted(i for i, _ in component)
    if len(rows) != len(component):
        return False
    for idx in range(1, len(rows)):
        if rows[idx] != rows[idx - 1] + 1:
            return False
    return True

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

def get_average_col(component: List[Tuple[int, int]]) -> float:
    if not component:
        return 0.0
    cols = [j for _, j in component]
    return sum(cols) / len(cols)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    out = [[background] * n for _ in range(n)]
    colors = sorted(get_colors(g, background))
    # First preserve all small and vertical components
    for color in colors:
        positions = get_positions(g, color)
        components = get_connected_components(g, color, positions, n)
        for component in components:
            if len(component) <= 3 or is_vertical_aligned_component(component):
                for i, j in component:
                    out[i][j] = color
    # Then straighten large non-vertical components
    for color in colors:
        positions = get_positions(g, color)
        components = get_connected_components(g, color, positions, n)
        for component in components:
            k = len(component)
            if k <= 3 or is_vertical_aligned_component(component):
                continue
            avg_col = get_average_col(component)
            max_j = max(j for _, j in component)
            target = max_j  # Prefer right edge for target
            col = None
            min_dist = float('inf')
            # Prefer closest >= target, smallest dist (which is c - target since >=)
            for c in range(target, n):
                if all(out[r][c] == background for r in range(min(k, n))):
                    dist = c - target
                    if dist < min_dist:
                        min_dist = dist
                        col = c
            if col is None:
                # Fallback to any available, prefer rightmost
                for c in range(n - 1, -1, -1):
                    if all(out[r][c] == background for r in range(min(k, n))):
                        col = c
                        break
            if col is not None:
                for r in range(min(k, n)):
                    out[r][col] = color
    return out
```