```python
from typing import List, Tuple

def find_components(g: List[List[int]]) -> List[List[Tuple[int, int, int]]]:
    n = len(g)
    visited = set()
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] > 0 and (i, j) not in visited:
                component = []
                stack = [(i, j)]
                visited.add((i, j))
                while stack:
                    x, y = stack.pop()
                    component.append((x, y, g[x][y]))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] > 0 and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            stack.append((nx, ny))
                components.append(component)
    return components

def get_rel_shape(component: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    if not component:
        return []
    min_r = min(r for r, _, _ in component)
    min_c = min(c for _, c, _ in component)
    return [(r - min_r, c - min_c, v) for r, c, v in component]

def get_centroid(component: List[Tuple[int, int, int]]) -> float:
    if not component:
        return 0.0
    total_r = sum(r for r, _, _ in component)
    return total_r / len(component)

def get_dimensions(rel_shape: List[Tuple[int, int, int]]) -> Tuple[int, int]:
    if not rel_shape:
        return 0, 0
    max_r = max(r for r, _, _ in rel_shape)
    max_c = max(c for _, c, _ in rel_shape)
    return max_r + 1, max_c + 1

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    components = find_components(g)
    shapes = []
    for comp in components:
        rel = get_rel_shape(comp)
        h, w = get_dimensions(rel)
        centroid = get_centroid(comp)
        shapes.append((centroid, rel, h, w))
    # Sort by decreasing centroid row (bottom first)
    shapes.sort(key=lambda x: -x[0])
    output_g = [[0] * n for _ in range(n)]
    for _, rel_shape, height, width in shapes:
        placed = False
        for sr in range(n - height + 1):
            if placed:
                break
            for sc in range(n - width + 1):
                can_place = True
                for dr, dc, v in rel_shape:
                    nr = sr + dr
                    nc = sc + dc
                    if output_g[nr][nc] != 0 and output_g[nr][nc] != v:
                        can_place = False
                        break
                if can_place:
                    for dr, dc, v in rel_shape:
                        nr = sr + dr
                        nc = sc + dc
                        output_g[nr][nc] = v
                    placed = True
                    break
        # If not placed, skip or place at bottom-left (assume fits)
        if not placed:
            sr = n - height
            sc = 0
            for dr, dc, v in rel_shape:
                nr = sr + dr
                nc = sc + dc
                if 0 <= nr < n and 0 <= nc < n:
                    if output_g[nr][nc] == 0 or output_g[nr][nc] == v:
                        output_g[nr][nc] = v
    return output_g
```