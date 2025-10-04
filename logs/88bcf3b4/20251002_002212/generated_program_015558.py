```python
from typing import List, Tuple
from collections import Counter, deque

def get_background(g: List[List[int]]) -> int:
    """Identify the background color as the most frequent value."""
    n = len(g)
    flat = [g[i][j] for i in range(n) for j in range(n)]
    return Counter(flat).most_common(1)[0][0]

def get_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """Find connected components (4-connected) for non-background pixels, grouped by color."""
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = {}  # color -> list of components, each component list of (r, c)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != background and not visited[i][j]:
                color = g[i][j]
                if color not in components:
                    components[color] = []
                component = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                if component:
                    components[color].append(component)
    result = []
    for color, comps in components.items():
        for comp in comps:
            result.append((color, comp))
    return result

def get_bbox(component: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Compute bounding box: min_r, max_r, min_c, max_c."""
    rows = [r for r, c in component]
    cols = [c for r, c in component]
    return min(rows), max(rows), min(cols), max(cols)

def is_fixed(component: List[Tuple[int, int]], n: int) -> bool:
    """Determine if component is fixed based on position (low min_r or high max_c)."""
    min_r, max_r, min_c, max_c = get_bbox(component)
    return min_r <= 2 or max_c >= n - 2

def keep_fixed(color: int, component: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Rule for unchanged components: keep positions as is."""
    return component

def transform_moving(color: int, component: List[Tuple[int, int]], n: int) -> List[Tuple[int, int]]:
    """Rule for moving components: shift up to top, straighten vertically in leftmost column (simplified, may lose pixels if conflict)."""
    k = len(component)
    # Simplified: place vertically from row 0 in col 0, but cap at n pixels, lose if >n (rough approx for loss)
    new_comp = [(i, 0) for i in range(min(k, n))]
    return new_comp

def place_pixels(g: List[List[int]], components: List[Tuple[int, List[Tuple[int, int]]]], background: int) -> List[List[int]]:
    """Compose all components into new grid, filling with background."""
    n = len(g)
    new_g = [[background for _ in range(n)] for _ in range(n)]
    for color, comp in components:
        for r, c in comp:
            if 0 <= r < n and 0 <= c < n:
                new_g[r][c] = color
    return new_g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: infer rules from observations - preserve colors, fix some components, shift/split others."""
    n = len(g)
    background = get_background(g)
    all_components = get_components(g, background)
    transformed_components = []
    for color, comp in all_components:
        if is_fixed(comp, n):
            new_comp = keep_fixed(color, comp)
        else:
            new_comp = transform_moving(color, comp, n)
        transformed_components.append((color, new_comp))
    return place_pixels(g, transformed_components, background)
```