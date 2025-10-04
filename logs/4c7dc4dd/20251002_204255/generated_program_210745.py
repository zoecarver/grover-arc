```python
from typing import List

def find_special_color(g: List[List[int]]) -> int:
    """Find the special color as the maximum value in the grid greater than 4."""
    if not g or not g[0]:
        return 0
    return max(max(row) for row in g)

def find_components(g: List[List[int]], s: int) -> List[List[tuple[int, int]]]:
    """Find 4-connected components of cells with value s, avoiding deep nesting by using iterative BFS."""
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == s and not visited[i][j]:
                component = []
                queue = [(i, j)]
                visited[i][j] = True
                index = 0
                while index < len(queue):
                    x, y = queue[index]
                    index += 1
                    component.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == s and not visited[nx][ny]:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components.append(component)
    return components

def compute_centers(components: List[List[tuple[int, int]]]) -> List[tuple[float, float]]:
    """Compute center (average row, average col) for each component."""
    centers = []
    for comp in components:
        if comp:
            sum_r = sum(r for r, _ in comp)
            sum_c = sum(c for _, c in comp)
            num = len(comp)
            centers.append((sum_r / num, sum_c / num))
        else:
            centers.append((0.0, 0.0))
    return centers

def scale_position(pos: float, min_pos: float, max_pos: float, k: int) -> int:
    """Scale a position to small grid index 0 to k-1 using relative position with shift for rounding."""
    if k <= 1:
        return 0
    span = max_pos - min_pos if max_pos > min_pos else 1.0
    norm = (pos - min_pos) / span * (k - 1)
    shifted = norm + 0.5
    return max(0, min(k - 1, round(shifted)))

def place_components(small: List[List[int]], centers: List[tuple[float, float]], k: int, s: int):
    """Place 2 at scaled positions of centers; use s for the leftmost upper if s==6."""
    if k == 0 or not centers:
        return
    min_r = min(r for r, _ in centers)
    max_r = max(r for r, _ in centers)
    min_c = min(c for _, c in centers)
    max_c = max(c for _, c in centers)
    # Find the upper leftmost for special if applicable
    upper_left_idx = min(range(len(centers)), key=lambda idx: (centers[idx][0], centers[idx][1]))
    for idx, (r, c) in enumerate(centers):
        sr = scale_position(r, min_r, max_r, k)
        sc = scale_position(c, min_c, max_c, k)
        color = s if idx == upper_left_idx and s == 6 else 2
        small[sr][sc] = color

def fill_horizontal_bars(small: List[List[int]], k: int):
    """Fill rows with placements from min to max col with 2's, assuming top bar."""
    for r in range(k):
        cols_with = [j for j in range(k) if small[r][j] != 0]
        if cols_with:
            min_j = min(cols_with)
            max_j = max(cols_with)
            for j in range(min_j, max_j + 1):
                small[r][j] = 2 if small[r][j] == 0 else small[r][j]  # preserve 6

def fill_vertical_attach(small: List[List[int]], k: int):
    """Attach vertical bar from top bar left (col 0, row of first non-zero row) down to bottom with 2's."""
    first_r = next((r for r in range(k) if any(small[r][j] != 0 for j in range(k))), None)
    if first_r is None:
        return
    # Assume top bar at first_r, attach at col 0 down to k-1
    for r in range(first_r, k):
        small[r][0] = 2

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: infer special color, find components, scale and place, fill bars and vertical."""
    s = find_special_color(g)
    if s <= 4:
        return [[]]  # empty if no special
    components = find_components(g, s)
    k = len(components)
    if k == 0:
        return [[]]
    small = [[0] * k for _ in range(k)]
    centers = compute_centers(components)
    place_components(small, centers, k, s)
    fill_horizontal_bars(small, k)
    fill_vertical_attach(small, k)
    return small
```