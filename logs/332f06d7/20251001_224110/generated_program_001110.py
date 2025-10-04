```python
from collections import deque
from typing import List, Tuple

def is_adj_to_one(g: List[List[int]], i: int, j: int, n: int) -> bool:
    """Check if position (i,j) is adjacent to a 1 (blue)."""
    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for di, dj in directions:
        ni: int = i + di
        nj: int = j + dj
        if 0 <= ni < n and 0 <= nj < n and g[ni][nj] == 1:
            return True
    return False

def find_touching_zero_components(g: List[List[int]], n: int) -> List[Tuple[int, int]]:
    """Find all positions in connected components of 0s that touch at least one 1 (blue). Uses BFS."""
    visited: List[List[bool]] = [[False] * n for _ in range(n)]
    fill_positions: List[Tuple[int, int]] = []
    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def bfs(start_i: int, start_j: int) -> List[Tuple[int, int]]:
        q: deque = deque([(start_i, start_j)])
        visited[start_i][start_j] = True
        component: List[Tuple[int, int]] = [(start_i, start_j)]
        while q:
            x, y = q.popleft()
            for di, dj in directions:
                nx: int = x + di
                ny: int = y + dj
                if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 0 and not visited[nx][ny]:
                    visited[nx][ny] = True
                    q.append((nx, ny))
                    component.append((nx, ny))
        return component

    for i in range(n):
        for j in range(n):
            if g[i][j] == 0 and not visited[i][j] and is_adj_to_one(g, i, j, n):
                component: List[Tuple[int, int]] = bfs(i, j)
                fill_positions.extend(component)
    return fill_positions

def set_red_to_empty(out: List[List[int]], n: int) -> None:
    """Set all 2s (red) to 0s. Rule: red is absorbed and contributes pixels to blue when applicable."""
    for i in range(n):
        for j in range(n):
            if out[i][j] == 2:
                out[i][j] = 0

def fill_holes(out: List[List[int]], fill_positions: List[Tuple[int, int]]) -> None:
    """Set positions in fill_positions from 0 to 1 (blue). Observation: holes touching blue are filled."""
    for i, j in fill_positions:
        out[i][j] = 1

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing rules: absorb red to empty, fill touching zero components with blue."""
    n: int = len(g)
    out: List[List[int]] = [row[:] for row in g]
    fill_positions: List[Tuple[int, int]] = find_touching_zero_components(g, n)
    set_red_to_empty(out, n)
    fill_holes(out, fill_positions)
    return out
```