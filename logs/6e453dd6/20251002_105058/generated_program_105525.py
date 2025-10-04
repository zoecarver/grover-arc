```python
from typing import List, Set, Tuple

def find_separator_column(grid: List[List[int]]) -> int:
    return grid[0].index(5)

def find_components(grid: List[List[int]], left_end: int) -> List[Set[Tuple[int, int]]]:
    rows = len(grid)
    visited: Set[Tuple[int, int]] = set()
    components: List[Set[Tuple[int, int]]] = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(left_end + 1):
            if grid[r][c] == 0 and (r, c) not in visited:
                component: Set[Tuple[int, int]] = set()
                stack: List[Tuple[int, int]] = [(r, c)]
                visited.add((r, c))
                component.add((r, c))
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < rows and 0 <= nc <= left_end and grid[nr][nc] == 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            stack.append((nr, nc))
                            component.add((nr, nc))
                components.append(component)
    return components

def compute_shift(component: Set[Tuple[int, int]], left_end: int) -> int:
    if not component:
        return 0
    max_col = max(c for _, c in component)
    return left_end - max_col

def apply_shifts(grid: List[List[int]], components: List[Set[Tuple[int, int]]], left_end: int) -> None:
    for component in components:
        shift = compute_shift(component, left_end)
        if shift > 0:
            for r, c in component:
                grid[r][c] = 6
            for r, c in component:
                new_c = c + shift
                if new_c <= left_end:
                    grid[r][new_c] = 0

def apply_right_side(grid: List[List[int]], s: int) -> None:
    rows = len(grid)
    cols = len(grid[0])
    right_start = s + 1
    left_end = s - 1
    for row in range(rows):
        if grid[row][left_end] != 0:
            continue
        zeros_cols = [c for c in range(s) if grid[row][c] == 0]
        if not zeros_cols:
            continue
        min0 = min(zeros_cols)
        solid = True
        for c in range(min0, s):
            if grid[row][c] != 0:
                solid = False
                break
        if not solid:
            for c in range(right_start, cols):
                grid[row][c] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    s = find_separator_column(g)
    left_end = s - 1
    components = find_components(g, left_end)
    apply_shifts(grid, components, left_end)
    apply_right_side(grid, s)
    return grid
```