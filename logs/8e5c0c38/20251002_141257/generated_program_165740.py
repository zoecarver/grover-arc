```python
from typing import List, Tuple
from collections import Counter, deque

def get_background(g: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent value in the grid.
    """
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_and_remove_small_components(g: List[List[int]], bg: int, threshold: int = 3) -> List[List[int]]:
    """
    Finds connected components using 4-connectivity and removes those smaller than threshold by setting to background.
    Rule: Small isolated groups (noise) are removed to clean the image while preserving larger structures.
    """
    h, w = len(g), len(g[0])
    out = [row[:] for row in g]
    visited = [[False] * w for _ in range(h)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if not visited[i][j] and g[i][j] != bg:
                color = g[i][j]
                component = []
                queue = deque([(i, j)])
                visited[i][j] = True
                component.append((i, j))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                            component.append((nx, ny))
                if len(component) < threshold:
                    for x, y in component:
                        out[x][y] = bg
    return out

def fill_gaps_with_majority_neighbor(g: List[List[int]], bg: int) -> List[List[int]]:
    """
    Fills background pixels that have at least 2 neighbors of the same non-background color in 8-connectivity.
    Rule: Fill small gaps or indentations in larger shapes based on surrounding color majority.
    """
    h, w = len(g), len(g[0])
    out = [row[:] for row in g]
    directions8 = [(di, dj) for di in [-1, 0, 1] for dj in [-1, 0, 1] if not (di == 0 and dj == 0)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == bg:
                neighbor_counts = Counter()
                for di, dj in directions8:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < h and 0 <= nj < w:
                        c = g[ni][nj]
                        if c != bg:
                            neighbor_counts[c] += 1
                if neighbor_counts:
                    max_c, max_count = neighbor_counts.most_common(1)[0]
                    if max_count >= 2:
                        out[i][j] = max_c
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: Compose removal of small components followed by gap filling to clean the grid.
    Applies rules sequentially to handle noise removal and shape completion.
    """
    h, w = len(g), len(g[0])
    bg = get_background(g)
    out = find_and_remove_small_components(g, bg)
    out = fill_gaps_with_majority_neighbor(out, bg)
    return out
```