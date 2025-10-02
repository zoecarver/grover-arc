```python
from collections import Counter, deque
from typing import List, Tuple

def find_background_and_special(grid: List[List[int]]) -> tuple[int, int]:
    """Identify background (most common) and special (least common non-bg with >0 count)."""
    if not grid or not grid[0]:
        return 0, 0  # Default for empty
    flat = [grid[i][j] for i in range(len(grid)) for j in range(len(grid[0]))]
    c = Counter(flat)
    background = c.most_common(1)[0][0]
    non_bg = [k for k in c if k != background and c[k] > 0]
    special = min(non_bg, key=lambda k: c[k]) if non_bg else None
    return background, special

def extract_components(grid: List[List[int]], background: int, directions: List[Tuple[int, int]]) -> List[List[Tuple[int, int, int]]]:
    """Extract all connected components (non-bg) using BFS, returning list of [positions with (r, c, value)]."""
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != background and not visited[i][j]:
                component = []
                queue = deque([(i, j)])
                visited[i][j] = True
                component.append((i, j, grid[i][j]))
                while queue:
                    r, c = queue.popleft()
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] != background:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                            component.append((nr, nc, grid[nr][nc]))
                if component:
                    components.append(component)
    return components

def find_all_isolated_special(grid: List[List[int]], special: int, background: int, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Find all isolated special cells (no adjacent non-bg neighbors)."""
    rows, cols = len(grid), len(grid[0])
    isolated = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == special:
                is_isolated = True
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != background:
                        is_isolated = False
                        break
                if is_isolated:
                    isolated.append((r, c))
    return isolated

def program(g: List[List[int]]) -> List[List[int]]:
    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    bg, special = find_background_and_special(g)
    if special is None:
        return [row[:] for row in g]
    rows = len(g)
    if rows == 0:
        return g
    cols = len(g[0])
    isolated = find_all_isolated_special(g, special, bg, directions)
    if isolated:
        avg_c = sum(c for _, c in isolated) / len(isolated)
        ref_c = round(avg_c)
    else:
        special_cells = [(r, c) for r in range(rows) for c in range(cols) if g[r][c] == special]
        if not special_cells:
            return [row[:] for row in g]
        avg_c = sum(c for _, c in special_cells) / len(special_cells)
        ref_c = round(avg_c)
    components = extract_components(g, bg, directions)
    new_grid = [row[:] for row in g]
    for component in components:
        special_pos = [(r, c) for r, c, v in component if v == special]
        if not special_pos:
            continue
        # Check if single isolated
        if len(component) == 1 and len(special_pos) == 1:
            r, c = special_pos[0]
            is_isolated = True
            for dr, dc in directions:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] != bg:
                    is_isolated = False
                    break
            if is_isolated:
                continue
        # Key c from special pos
        key_sum_c = sum(c for _, c in special_pos)
        key_c = key_sum_c / len(special_pos)
        delta_c = round(ref_c - key_c)
        delta_r = 0
        # Erase original
        for r, c, _ in component:
            new_grid[r][c] = bg
        # Place shifted
        for r, c, v in component:
            nr = r + delta_r
            nc = c + delta_c
            if 0 <= nr < rows and 0 <= nc < cols:
                new_grid[nr][nc] = v
    return new_grid
```