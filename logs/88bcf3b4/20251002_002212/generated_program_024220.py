```python
from typing import List
from collections import Counter
import sys

def find_background(g: List[List[int]]) -> int:
    """Rule: Background is the most frequent color in the grid."""
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def is_vertical_component(component: List[tuple[int, int]], n: int) -> bool:
    """Observation: A component is stable if it is a straight vertical line (same column, consecutive rows, no gaps)."""
    if not component:
        return True
    cols = {c for r, c in component}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(r for r, c in component)
    min_r, max_r = rows[0], rows[-1]
    if max_r - min_r + 1 != len(rows):
        return False
    return all(r in rows for r in range(min_r, max_r + 1))

def find_components(g: List[List[int]], background: int, n: int) -> dict[int, List[List[tuple[int, int]]]]:
    """Rule: Find 4-connected components for each non-background color."""
    visited = [[False] * n for _ in range(n)]
    components = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != background and not visited[i][j]:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    r, c = stack.pop()
                    component.append((r, c))
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                if color not in components:
                    components[color] = []
                components[color].append(component)
    return components

def keep_stable_components(g: List[List[int]], background: int, components: dict[int, List[List[tuple[int, int]]]], n: int) -> List[List[int]]:
    """Rule: Keep stable vertical components in their original positions; fill rest with background."""
    out = [[background for _ in range(n)] for _ in range(n)]
    for color, comps in components.items():
        all_vertical = all(is_vertical_component(comp, n) for comp in comps)
        if all_vertical:
            for comp in comps:
                for r, c in comp:
                    out[r][c] = color
    return out

def collect_non_stable_pixels(components: dict[int, List[List[tuple[int, int]]]], background: int, g: List[List[int]], n: int) -> dict[int, List[tuple[int, int]]]:
    """Observation: For colors with any non-vertical component, collect all pixels of that color."""
    non_stable = {}
    for color, comps in components.items():
        if not all(is_vertical_component(comp, n) for comp in comps):
            pixels = []
            for r in range(n):
                for c in range(n):
                    if g[r][c] == color:
                        pixels.append((r, c))
            non_stable[color] = pixels
    return non_stable

def place_non_stable_as_diagonal(out: List[List[int]], non_stable: dict[int, List[tuple[int, int]]], n: int, background: int) -> List[List[int]]:
    """New approach: Place collected pixels of non-stable colors along a diagonal starting from top-left, one per step, overwriting background. Limit to available positions to approximate pixel count."""
    k = 0
    for color, pixels in non_stable.items():
        num = min(len(pixels), n * n)  # Approximate conservation
        for i in range(num):
            r = k // n
            c = k % n
            if r < n and c < n and out[r][c] == background:  # Place only on background
                out[r][c] = color
            k += 1
            if k >= n * n:
                break
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    background = find_background(g)
    components = find_components(g, background, n)
    out = keep_stable_components(g, background, components, n)
    non_stable = collect_non_stable_pixels(components, background, g, n)
    out = place_non_stable_as_diagonal(out, non_stable, n, background)
    return out
```