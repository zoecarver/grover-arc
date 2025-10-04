```python
from typing import List

def flood_fill_to_find_component(grid: List[List[int]], visited: List[List[bool]], sr: int, sc: int) -> List[tuple[int, int]]:
    """
    Finds the 4-connected component of the same color starting from (sr, sc).
    Marks cells as visited.
    """
    n = len(grid)
    color = grid[sr][sc]
    comp = []
    stack = [(sr, sc)]
    visited[sr][sc] = True
    while stack:
        r, c = stack.pop()
        comp.append((r, c))
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc] and grid[nr][nc] == color:
                visited[nr][nc] = True
                stack.append((nr, nc))
    return comp

def compute_holes(grid: List[List[int]], comp: List[tuple[int, int]]) -> int:
    """
    Computes the number of enclosed hole components within the bounding box of the component.
    Holes are connected components of 0-cells not reachable from the bbox boundary.
    """
    if not comp:
        return 0
    rs = [p[0] for p in comp]
    cs = [p[1] for p in comp]
    min_r = min(rs)
    max_r = max(rs)
    min_c = min(cs)
    max_c = max(cs)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Boundary starts
    starts = set()
    for c in range(min_c, max_c + 1):
        if grid[min_r][c] == 0:
            starts.add((min_r, c))
        if grid[max_r][c] == 0:
            starts.add((max_r, c))
    for r in range(min_r, max_r + 1):
        if grid[r][min_c] == 0:
            starts.add((r, min_c))
        if grid[r][max_c] == 0:
            starts.add((r, max_c))
    # Flood background 0's from starts within bbox
    background = set()
    stack = [pos for pos in starts]
    for sr, sc in starts:
        background.add((sr, sc))
    while stack:
        r, c = stack.pop()
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc
            if min_r <= nr <= max_r and min_c <= nc <= max_c and grid[nr][nc] == 0 and (nr, nc) not in background:
                background.add((nr, nc))
                stack.append((nr, nc))
    # Remaining 0's in bbox
    remaining = [(r, c) for r in range(min_r, max_r + 1) for c in range(min_c, max_c + 1) if grid[r][c] == 0 and (r, c) not in background]
    if not remaining:
        return 0
    # Count CCs in remaining
    hole_visited = set()
    num_holes = 0
    for zr, zc in remaining:
        if (zr, zc) not in hole_visited:
            num_holes += 1
            h_stack = [(zr, zc)]
            hole_visited.add((zr, zc))
            while h_stack:
                hr, hc = h_stack.pop()
                for dr, dc in dirs:
                    nr = hr + dr
                    nc = hc + dc
                    if min_r <= nr <= max_r and min_c <= nc <= max_c and grid[nr][nc] == 0 and (nr, nc) not in background and (nr, nc) not in hole_visited:
                        hole_visited.add((nr, nc))
                        h_stack.append((nr, nc))
    return num_holes

def compute_min_max_r(comp: List[tuple[int, int]]) -> tuple[int, int]:
    """
    Computes min_r and max_r for the component.
    """
    if not comp:
        return 0, 0
    rs = [p[0] for p in comp]
    return min(rs), max(rs)

def identify_and_build_legend(grid: List[List[int]]) -> dict[int, int]:
    """
    Scans the grid to identify legend components: non-5 color components exactly spanning rows 1 to 3 (0-indexed).
    Builds mapping from hole count h to color, sequentially validating h == position index.
    Stops on mismatch.
    """
    n = len(grid)
    visited = [[False] * n for _ in range(n)]
    legend = {}
    expected_h = 0
    stopped = False
    for r in range(n):
        for c in range(n):
            if grid[r][c] != 0 and not visited[r][c]:
                comp = flood_fill_to_find_component(grid, visited, r, c)
                color = grid[comp[0][0]][comp[0][1]]
                if color != 5:
                    min_r, max_r = compute_min_max_r(comp)
                    if min_r == 1 and max_r == 3 and not stopped:
                        h = compute_holes(grid, comp)
                        if h == expected_h:
                            legend[h] = color
                            expected_h += 1
                        else:
                            stopped = True
    return legend

def transform_orange_shapes(grid: List[List[int]], legend: dict[int, int]) -> List[List[int]]:
    """
    Scans the grid to find orange (5) components, computes their hole count h,
    and replaces the component with legend[h] if exists, else with 0 (removal).
    """
    n = len(grid)
    visited = [[False] * n for _ in range(n)]
    new_grid = [row[:] for row in grid]
    for r in range(n):
        for c in range(n):
            if new_grid[r][c] == 5 and not visited[r][c]:
                comp = flood_fill_to_find_component(new_grid, visited, r, c)  # uses new_grid but since 5's still there
                h = compute_holes(new_grid, comp)
                new_color = legend.get(h, 0)
                for pr, pc in comp:
                    new_grid[pr][pc] = new_color
    return new_grid

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: identifies legend from top shapes, transforms orange shapes based on hole counts.
    """
    legend = identify_and_build_legend(g)
    result = transform_orange_shapes(g, legend)
    return result
```