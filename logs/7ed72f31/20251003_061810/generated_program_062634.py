```python
from collections import Counter
from typing import List

def get_background_color(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_red_components(g: List[List[int]], n: int, m: int) -> List[List[tuple[int, int]]]:
    visited = [[False] * m for _ in range(n)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(m):
            if g[i][j] == 2 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(component)
    return components

def apply_point_symmetry(g: List[List[int]], output: List[List[int]], r: int, c: int, bg: int, n: int, m: int) -> None:
    for i in range(n):
        for j in range(m):
            if g[i][j] != bg and g[i][j] != 2:
                ir = 2 * r - i
                jr = 2 * c - j
                if 0 <= ir < n and 0 <= jr < m and output[ir][jr] == bg:
                    output[ir][jr] = g[i][j]

def apply_horizontal_symmetry(g: List[List[int]], output: List[List[int]], rr: int, bg: int, n: int, m: int) -> None:
    for i in range(n):
        for j in range(m):
            if g[i][j] != bg and g[i][j] != 2:
                ir = 2 * rr - i
                jr = j
                if 0 <= ir < n and 0 <= jr < m and output[ir][jr] == bg:
                    output[ir][jr] = g[i][j]

def apply_vertical_symmetry(g: List[List[int]], output: List[List[int]], cc: int, bg: int, n: int, m: int) -> None:
    for i in range(n):
        for j in range(m):
            if g[i][j] != bg and g[i][j] != 2:
                ir = i
                jr = 2 * cc - j
                if 0 <= ir < n and 0 <= jr < m and output[ir][jr] == bg:
                    output[ir][jr] = g[i][j]

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    bg = get_background_color(g)
    components = get_red_components(g, n, m)
    output = [row[:] for row in g]
    for comp in components:
        if len(comp) == 1:
            r, c = comp[0]
            apply_point_symmetry(g, output, r, c, bg, n, m)
        else:
            rows_set = {p[0] for p in comp}
            cols_set = {p[1] for p in comp}
            if len(rows_set) == 1 and len(cols_set) > 1:
                rr = next(iter(rows_set))
                c_min = min(cols_set)
                c_max = max(cols_set)
                if c_max - c_min + 1 == len(comp):
                    apply_horizontal_symmetry(g, output, rr, bg, n, m)
            elif len(cols_set) == 1 and len(rows_set) > 1:
                cc = next(iter(cols_set))
                r_min = min(rows_set)
                r_max = max(rows_set)
                if r_max - r_min + 1 == len(comp):
                    apply_vertical_symmetry(g, output, cc, bg, n, m)
    return output
```