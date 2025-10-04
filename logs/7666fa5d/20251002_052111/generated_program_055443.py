```python
from typing import List
from collections import deque

def get_grid_size(g: List[List[int]]) -> int:
    """
    Extracts the size n of the square grid.
    """
    return len(g)

def create_visited_matrix(n: int) -> List[List[bool]]:
    """
    Creates a visited matrix initialized to False for tracking exterior 8s.
    """
    return [[False] * n for _ in range(n)]

def get_orthogonal_directions() -> List[tuple[int, int]]:
    """
    Returns the 4 orthogonal directions for flood fill connectivity.
    """
    return [(-1, 0), (1, 0), (0, -1), (0, 1)]

def is_border_cell(r: int, c: int, n: int) -> bool:
    """
    Checks if a cell is on the grid border.
    """
    return r == 0 or r == n - 1 or c == 0 or c == n - 1

def enqueue_border_open_cells(g: List[List[int]], n: int, visited: List[List[bool]], queue: deque) -> None:
    """
    Enqueues all border cells that are 8 (open) and marks them visited.
    """
    for r in range(n):
        for c in range(n):
            if is_border_cell(r, c, n) and g[r][c] == 8 and not visited[r][c]:
                visited[r][c] = True
                queue.append((r, c))

def is_valid_cell(nr: int, nc: int, n: int) -> bool:
    """
    Checks if a cell position is within grid bounds.
    """
    return 0 <= nr < n and 0 <= nc < n

def perform_exterior_flood(g: List[List[int]], n: int, visited: List[List[bool]], queue: deque) -> None:
    """
    Performs BFS flood fill from queued border 8s through adjacent 8s to mark exterior.
    """
    directions = get_orthogonal_directions()
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid_cell(nr, nc, n) and g[nr][nc] == 8 and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc))

def create_result_grid(g: List[List[int]]) -> List[List[int]]:
    """
    Creates a deep copy of the input grid as the result base.
    """
    return [row[:] for row in g]

def fill_enclosed_regions(g: List[List[int]], result: List[List[int]], visited: List[List[bool]], n: int) -> None:
    """
    Fills unvisited 8s (enclosed regions) with 2s in the result grid.
    """
    for r in range(n):
        for c in range(n):
            if g[r][c] == 8 and not visited[r][c]:
                result[r][c] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: identifies enclosed 8s by flooding exterior from borders and fills them with 2s.
    """
    n = get_grid_size(g)
    visited = create_visited_matrix(n)
    queue = deque()
    enqueue_border_open_cells(g, n, visited, queue)
    perform_exterior_flood(g, n, visited, queue)
    result = create_result_grid(g)
    fill_enclosed_regions(g, result, visited, n)
    return result
```