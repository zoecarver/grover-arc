```python
from typing import List
from collections import deque

def touches_top_or_bottom(component: List[tuple[int, int]], n: int) -> bool:
    """
    Rule: A component touches the top or bottom if any cell is in row 0 or row n-1.
    This determines if the component should be preserved (touching) or absorbed (not touching).
    """
    for r, c in component:
        if r == 0 or r == n - 1:
            return True
    return False

def find_non_seven_components(grid: List[List[int]]) -> List[List[tuple[int, int]]]:
    """
    Observation: Non-7 cells (0s and numbers 1-9) form connected components using 4-connectivity.
    This extracts all such blobs for further processing.
    """
    n = len(grid)
    visited = [[False] * n for _ in range(n)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 7 and not visited[i][j]:
                component = []
                q = deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != 7 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            component.append((nx, ny))
                components.append(component)
    return components

def absorb_internal_components(grid: List[List[int]]) -> List[List[int]]:
    """
    Rule: Absorb (set to 7) any connected non-7 component that does not touch the top or bottom row.
    This removes floating internal blobs while preserving those attached to top or bottom.
    """
    n = len(grid)
    result = [row[:] for row in grid]
    components = find_non_seven_components(result)
    for component in components:
        if not touches_top_or_bottom(component, n):
            for r, c in component:
                result[r][c] = 7
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Composes the rules: Extract components and absorb internal ones not touching top or bottom.
    """
    return absorb_internal_components(g)
```