```python
from typing import List, Tuple, Dict
import collections

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Copy the grid."""
    return [row[:] for row in g]

def count_non_zero_colors(g: List[List[int]]) -> int:
    """Identify the most frequent non-zero color as fill."""
    counts = collections.Counter(c for row in g for c in row if c > 0)
    return counts.most_common(1)[0][0] if counts else 0

def get_size_map(g: List[List[int]]) -> Dict[Tuple[int, int], int]:
    """Compute initial component size for each position using 4-connectivity."""
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    size_map: Dict[Tuple[int, int], int] = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and g[r][c] > 0:
                value = g[r][c]
                component = []
                queue = collections.deque([(r, c)])
                visited[r][c] = True
                component.append((r, c))
                while queue:
                    cr, cc = queue.popleft()
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == value:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                            component.append((nr, nc))
                component_size = len(component)
                for pr, pc in component:
                    size_map[(pr, pc)] = component_size
    return size_map

def get_adjacent_positions(r: int, c: int, rows: int, cols: int) -> List[Tuple[int, int]]:
    """Get 4-connected adjacent positions."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    positions = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            positions.append((nr, nc))
    return positions

def perform_update_step(g: List[List[int]], fill: int, size_map: Dict[Tuple[int, int], int], rows: int, cols: int) -> Tuple[List[List[int]], bool]:
    """Perform one update step: replace fill cells adjacent to unique or max influencing color from qualified neighbors."""
    temp = copy_grid(g)
    changed = False
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == fill:
                influencing_colors = set()
                color_counts = collections.Counter()
                for nr, nc in get_adjacent_positions(r, c, rows, cols):
                    nval = g[nr][nc]
                    npos = (nr, nc)
                    nsize = size_map.get(npos, 0)
                    if nval != fill and nval > 0 and nsize >= 2:
                        color_counts[nval] += 1
                        influencing_colors.add(nval)
                if influencing_colors:
                    if len(influencing_colors) == 1:
                        new_color = next(iter(influencing_colors))
                    else:
                        new_color = max(influencing_colors)
                    temp[r][c] = new_color
                    changed = True
    return temp, changed

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: iteratively update the grid until stable."""
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    fill = count_non_zero_colors(g)
    if fill == 0:
        return copy_grid(g)
    size_map = get_size_map(g)
    current = copy_grid(g)
    max_iters = rows * cols  # Prevent infinite loop
    for _ in range(max_iters):
        temp, changed = perform_update_step(current, fill, size_map, rows, cols)
        current = temp
        if not changed:
            break
    return current
```