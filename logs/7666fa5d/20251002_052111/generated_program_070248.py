```python
from typing import List
from collections import deque

def get_special_color(g: List[List[int]]) -> int:
    # Rule: Identify the boundary color as the maximum non-background color present (assuming single primary boundary color per grid).
    colors = {cell for row in g for cell in row if cell != 8}
    return max(colors) if colors else 8

def create_binary(g: List[List[int]], special: int, n: int) -> List[List[int]]:
    # Rule: Create binary grid where boundary cells (special color) are walls (1), background (8) are spaces (0).
    return [[1 if g[r][c] == special else 0 for c in range(n)] for r in range(n)]

def dilate(b: List[List[int]], n: int, iterations: int = 2) -> List[List[int]]:
    # Rule: Close small gaps in boundary walls using morphological dilation with 8-connectivity; 2 iterations handle gaps up to ~3 cells wide by thickening walls.
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    current = [row[:] for row in b]
    for _ in range(iterations):
        new_b = [row[:] for row in current]
        for r in range(n):
            for c in range(n):
                if current[r][c] == 0:
                    for dr, dc in dirs:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and current[nr][nc] == 1:
                            new_b[r][c] = 1
                            break
        current = new_b
    return current

def flood_exterior(b: List[List[int]], n: int) -> List[List[bool]]:
    # Rule: Mark exterior spaces (0s) reachable from grid borders using BFS with 8-connectivity to detect enclosed regions post-dilation.
    visited = [[False] * n for _ in range(n)]
    q = deque()
    # Enqueue border spaces
    for r in range(n):
        for c in (0, n - 1):
            if b[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in range(1, n - 1):  # Avoid double-enqueue corners
        for r in (0, n - 1):
            if b[r][c] == 0 and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while q:
        r, c = q.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and b[nr][nc] == 0 and not visited[nr][nc]:
                visited[nr][nc] = True
                q.append((nr, nc))
    return visited

def is_interior_space(b: List[List[int]], visited: List[List[bool]], r: int, c: int) -> bool:
    # Rule: An original space (8) remaining as space (0) post-dilation is interior if not reachable from borders (unvisited).
    return b[r][c] == 0 and not visited[r][c]

def has_interior_neighbor(b: List[List[int]], visited: List[List[bool]], r: int, c: int, n: int) -> bool:
    # Rule: An original space (8) dilated into wall (1) is interior if 8-adjacent to an interior space (unvisited 0), ensuring gap fillers inside shapes are filled but exterior ones are not.
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n and is_interior_space(b, visited, nr, nc):
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    # Compose rules: Detect boundary color, binarize, dilate to close gaps, flood exterior spaces, fill original 8s that are interior spaces or interior gap fillers with 2 (red), preserving boundaries and exterior.
    n = len(g)
    out = [row[:] for row in g]
    special = get_special_color(g)
    if special == 8:
        return out
    binary = create_binary(g, special, n)
    dilated = dilate(binary, n, iterations=2)
    visited = flood_exterior(dilated, n)
    for r in range(n):
        for c in range(n):
            if g[r][c] == 8:
                if is_interior_space(dilated, visited, r, c) or (dilated[r][c] == 1 and has_interior_neighbor(dilated, visited, r, c, n)):
                    out[r][c] = 2
    return out
```