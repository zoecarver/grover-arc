```python
from typing import List, Tuple, Set
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def discover_components_in_order(g: List[List[int]], background: int, n: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    visited: Set[Tuple[int, int]] = set()
    components: List[Tuple[int, List[Tuple[int, int]]]] = []
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(n):
        for j in range(n):
            pos = (i, j)
            if g[i][j] != background and pos not in visited:
                color = g[i][j]
                component: List[Tuple[int, int]] = []
                stack = [pos]
                visited.add(pos)
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in deltas:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == color and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def is_vertical_aligned_component(component: List[Tuple[int, int]]) -> bool:
    if not component:
        return True
    cols = {j for _, j in component}
    if len(cols) != 1:
        return False
    rows = sorted(i for i, _ in component)
    if len(rows) != len(set(rows)):
        return False
    for idx in range(1, len(rows)):
        if rows[idx] != rows[idx - 1] + 1:
            return False
    return True

def find_max_left_shift(out: List[List[int]], background: int, component: List[Tuple[int, int]], n: int) -> int:
    if not component:
        return 0
    max_j = max(j for _, j in component)
    min_dx = -max_j
    for dx in range(min_dx, 1):
        if all(0 <= j + dx < n and out[i][j + dx] == background for i, j in component):
            return dx
    return 0

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    out = [[background for _ in range(n)] for _ in range(n)]
    components = discover_components_in_order(g, background, n)
    for color, component in components:
        if len(component) <= 3 or is_vertical_aligned_component(component):
            dx = 0
        else:
            dx = find_max_left_shift(out, background, component, n)
        for i, j in component:
            new_j = j + dx
            out[i][new_j] = color
    return out
```