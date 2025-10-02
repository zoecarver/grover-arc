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

def is_vertical_aligned_comp(component: List[Tuple[int, int]]) -> bool:
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

def preserve_group(out: List[List[int]], component: List[Tuple[int, int]], color: int) -> None:
    for i, j in component:
        out[i][j] = color

def get_median_col(component: List[Tuple[int, int]]) -> int:
    if not component:
        return 0
    cols = sorted(j for _, j in component)
    return cols[len(cols) // 2]

def find_available_column(n: int, k: int, out: List[List[int]], background: int, target: int) -> int:
    possible = [col for col in range(n) if all(out[r][col] == background for r in range(k))]
    if not possible:
        max_free = -1
        best = 0
        for col in range(n):
            free_count = 0
            for r in range(n):
                if out[r][col] == background:
                    free_count += 1
                else:
                    break
            if free_count > max_free:
                max_free = free_count
                best = col
        return best
    possible.sort(key=lambda c: (abs(c - target), -c))
    return possible[0]

def place_vertical_stack(out: List[List[int]], color: int, col: int, k: int, n: int) -> None:
    for r in range(k):
        if r < n:
            out[r][col] = color

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_background(g)
    out = [[bg] * n for _ in range(n)]
    colors = get_colors(g, bg)
    large_components = []
    for color in sorted(colors):
        positions = get_positions(g, color)
        components = get_connected_components(g, color, positions, n)
        for comp in components:
            if len(comp) <= 3 or is_vertical_aligned_comp(comp):
                preserve_group(out, comp, color)
            else:
                min_r = min(i for i, _ in comp)
                large_components.append((min_r, color, comp))
    large_components.sort(key=lambda x: x[0])
    for _, color, comp in large_components:
        k = len(comp)
        target = get_median_col(comp)
        col = find_available_column(n, k, out, bg, target)
        place_vertical_stack(out, color, col, k, n)
    return out
```