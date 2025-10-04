```python
from typing import List
from collections import Counter

def identify_background_color(g: List[List[int]]) -> int:
    """Identify the background color as the most frequent color in the grid."""
    if not g:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_connected_components(g: List[List[int]], color: int, n: int, m: int) -> List[dict]:
    """Find all 4-connected components of the given color."""
    visited = [[False] * m for _ in range(n)]
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    components = []
    for i in range(n):
        for j in range(m):
            if g[i][j] == color and not visited[i][j]:
                positions = []
                minr = maxr = i
                minc = maxc = j
                size = 0
                stack = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    if visited[x][y] or g[x][y] != color:
                        continue
                    visited[x][y] = True
                    positions.append((x, y))
                    size += 1
                    minr = min(minr, x)
                    maxr = max(maxr, x)
                    minc = min(minc, y)
                    maxc = max(maxc, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and g[nx][ny] == color:
                            stack.append((nx, ny))
                if size > 0:
                    components.append({
                        'color': color,
                        'positions': positions,
                        'size': size,
                        'bbox': (minr, maxr, minc, maxc)
                    })
    return components

def keep_large_holed_component_unchanged(g: List[List[int]], components: List[dict]) -> List[List[int]]:
    """Keep the large holed component (largest by size) unchanged."""
    # By default, do nothing as we change only small components later
    return [row[:] for row in g]

def change_small_components_based_on_position(g: List[List[int]], components: List[dict], n: int, m: int) -> List[List[int]]:
    """Change color of small components (holes=0 assumed) based on position relative to center."""
    out = [row[:] for row in g]
    if not components:
        return out
    large_size = max(c['size'] for c in components)
    center_r = n / 2.0
    center_c = m / 2.0
    for comp in components:
        if comp['size'] >= large_size / 2 or comp['size'] > 20:
            continue  # Keep large components unchanged
        minr, maxr, minc, maxc = comp['bbox']
        mid_r = (minr + maxr) / 2.0
        mid_c = (minc + maxc) / 2.0
        if comp['color'] == 0:
            # Special rule for empty spaces: fill with orange if small
            new_color = 5
        elif mid_r < center_r:
            # Top position: change to green
            new_color = 3
        elif mid_c < center_c:
            # Left position: change to orange
            new_color = 5
        else:
            continue  # No change
        for i, j in comp['positions']:
            out[i][j] = new_color
    return out

def change_background_color(g: List[List[int]]) -> List[List[int]]:
    """Change background from magenta to yellow if applicable; in examples, numbers stay the same."""
    # No change observed in number representation
    return [row[:] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    bg = identify_background_color(g)
    flat = [cell for row in g for cell in row]
    components = []
    for color in set(flat) - {bg}:
        components.extend(find_connected_components(g, color, n, m))
    out = keep_large_holed_component_unchanged(g, components)
    out = change_small_components_based_on_position(out, components, n, m)
    out = change_background_color(out)
    return out
```