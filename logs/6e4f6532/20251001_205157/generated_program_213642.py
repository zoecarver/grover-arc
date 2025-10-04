```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    """Detect the background color as the most frequent number in the grid."""
    if not g or not g[0]:
        return 0
    flat = [g[i][j] for i in range(len(g)) for j in range(len(g[0]))]
    count = Counter(flat)
    return count.most_common(1)[0][0] if count else 0

def find_connected_components(g: List[List[int]], background: int) -> List[Tuple[List[Tuple[int, int]], int]]:
    """Find connected components of same non-background numbers (4-way adjacent), including singles."""
    if not g or not g[0]:
        return []
    height, width = len(g), len(g[0])
    visited = [[False] * width for _ in range(height)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(height):
        for j in range(width):
            if not visited[i][j] and g[i][j] != background:
                num = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and g[nx][ny] == num:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((component, num))
    return components

def compute_drop_distance(comp_pos: List[Tuple[int, int]], grid: List[List[int]], bg: int, delta: int) -> int:
    """Compute the maximum drop distance for the component in the given direction (delta = -1 for up, 1 for down)."""
    h = len(grid)
    min_d = float('inf')
    for i, j in comp_pos:
        d = 0
        r = i + delta
        while 0 <= r < h and grid[r][j] == bg:
            d += 1
            r += delta
        min_d = min(min_d, d)
    return min_d

def apply_gravity(grid: List[List[int]], bg: int) -> List[List[int]]:
    """Apply gravity upward (to lower row indices) iteratively until stable using connected components."""
    g = [row[:] for row in grid]
    h = len(g)
    if h == 0:
        return g
    w = len(g[0])
    delta = -1  # upward to lower indices
    while True:
        components = find_connected_components(g, bg)
        if not components:
            break
        # Sort to process lower components first: larger max_i first, then larger min_i first
        components.sort(key=lambda c: (-max(p[0] for p in c[0]), -min(p[0] for p in c[0])))
        moved = False
        for comp_pos, num in components:
            # Clear the component
            for i, j in comp_pos:
                g[i][j] = bg
            # Compute min drop distance upward
            min_d = compute_drop_distance(comp_pos, g, bg, delta)
            if min_d > 0:
                moved = True
                # Place at new positions
                for i, j in comp_pos:
                    new_i = i + delta * min_d
                    g[new_i][j] = num
            else:
                # Restore if no drop
                for i, j in comp_pos:
                    g[i][j] = num
        if not moved:
            break
    return g

def remove_large_nines_groups(grid: List[List[int]], bg: int) -> List[List[int]]:
    """Remove connected groups of 9s with size >= 3, setting them to background."""
    g = [row[:] for row in grid]
    components = find_connected_components(g, bg)
    for comp_pos, num in components:
        if num == 9 and len(comp_pos) >= 3:
            for i, j in comp_pos:
                g[i][j] = bg
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: apply upward gravity, remove large 9 groups, then gravity again."""
    if not g:
        return g
    bg = get_background(g)
    grid = apply_gravity(g, bg)
    grid = remove_large_nines_groups(grid, bg)
    grid = apply_gravity(grid, bg)
    return grid
```