```python
from typing import List, Tuple, Set
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    c = Counter(flat)
    return c.most_common(1)[0][0]

def get_connected_component(g: List[List[int]], color: int, start_i: int, start_j: int, n: int, background: int) -> List[Tuple[int, int]]:
    visited: Set[Tuple[int, int]] = set()
    component: List[Tuple[int, int]] = []
    stack = [(start_i, start_j)]
    visited.add((start_i, start_j))
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while stack:
        i, j = stack.pop()
        if g[i][j] == color:
            component.append((i, j))
            for di, dj in deltas:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == color and (ni, nj) not in visited:
                    visited.add((ni, nj))
                    stack.append((ni, nj))
    return component

def is_vertical_aligned(component: List[Tuple[int, int]]) -> bool:
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

def get_max_col(component: List[Tuple[int, int]]) -> int:
    if not component:
        return 0
    return max(j for _, j in component)

def place_straightened_stack(out: List[List[int]], color: int, component: List[Tuple[int, int]], n: int, background: int) -> None:
    k = len(component)
    if k == 0:
        return
    target = get_max_col(component)
    current_col = target
    placed = 0
    for r in range(n):
        if placed == k:
            break
        c = current_col
        while 0 <= c < n:
            if out[r][c] == background:
                out[r][c] = color
                placed += 1
                current_col = c
                break
            c -= 1  # shift left

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = get_background(g)
    out = [[background for _ in range(n)] for _ in range(n)]
    all_components = []
    seen: Set[Tuple[int, int]] = set()
    for i in range(n):
        for j in range(n):
            if g[i][j] != background and (i, j) not in seen:
                color = g[i][j]
                component = get_connected_component(g, color, i, j, n, background)
                for p in component:
                    seen.add(p)
                all_components.append((color, component))
    all_components.sort(key=lambda x: min((i for i, _ in x[1]), default=n))
    for color, component in all_components:
        if len(component) <= 3 or is_vertical_aligned(component):
            preserve_group(out, component, color)
    for color, component in all_components:
        if len(component) > 3 and not is_vertical_aligned(component):
            place_straightened_stack(out, color, component, n, background)
    return out
```