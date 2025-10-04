```python
from typing import List, Tuple
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    """Identify background as most common value."""
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_connected_components(g: List[List[int]], background: int) -> List[Tuple[List[Tuple[int, int]], int]]:
    """Find 4-connected components of same non-background value using flood-fill."""
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-connected
    
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != background and not visited[i][j]:
                value = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == value:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if component:
                    components.append((component, value))
    return components

def drop_one_row(g: List[List[int]], component: List[Tuple[int, int]], value: int, background: int, rows: int, cols: int) -> bool:
    """Attempt to drop the component one row down, modifying g if successful, restoring if not."""
    new_positions = [(r + 1, c) for r, c in component]
    if any(nr >= rows for nr, _ in new_positions):
        return False
    
    # Temporarily clear current positions
    cleared = []
    for r, c in component:
        if g[r][c] == value:
            cleared.append((r, c))
            g[r][c] = background
    
    # Check if all new positions are empty
    can_drop = all(0 <= nc < cols and g[nr][nc] == background for nr, nc in new_positions)
    
    if not can_drop:
        # Restore
        for r, c in cleared:
            g[r][c] = value
        return False
    
    # Place in new positions (old are already cleared)
    for nr, nc in new_positions:
        g[nr][nc] = value
    
    return True

def drop_component(g: List[List[int]], component: List[Tuple[int, int]], value: int, background: int, rows: int, cols: int) -> None:
    """Fully drop the component down as far as possible by repeating one-row drops."""
    current = list(component)
    while drop_one_row(g, current, value, background, rows, cols):
        current = [(r + 1, c) for r, c in current]

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: find components, sort by lowest point (max row) descending, drop each fully."""
    if not g or not g[0]:
        return g
    n, m = len(g), len(g[0])
    bg = find_background(g)
    components = find_connected_components(g, bg)
    if not components:
        return [row[:] for row in g]
    
    # Sort components by max row descending (process lowest first)
    components.sort(key=lambda x: max(r for r, _ in x[0]) if x[0] else -1, reverse=True)
    
    # Work on a copy
    grid = [row[:] for row in g]
    
    for comp, val in components:
        drop_component(grid, comp, val, bg, n, m)
    
    return grid
```