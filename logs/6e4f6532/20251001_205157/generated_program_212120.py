```python
from typing import List, Tuple
from collections import Counter, defaultdict

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
                if component:
                    components.append((component, num))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    """Simulate gravity for connected components of same non-background color, dropping rigid units from bottom to top."""
    background = get_background(g)
    components = find_connected_components(g, background)
    # Sort by max row descending (process bottom components first)
    components.sort(key=lambda x: -max(pos[0] for pos in x[0]))
    new_g = [row[:] for row in g]
    height = len(new_g)
    for component, num in components:
        # Clear component positions
        for i, j in component:
            new_g[i][j] = background
        # Compute min drop distance across columns
        col_lowest = defaultdict(lambda: -1)
        for i, j in component:
            col_lowest[j] = max(col_lowest[j], i)
        d = float('inf')
        for j, lowest in col_lowest.items():
            count = 0
            for r in range(lowest + 1, height):
                if new_g[r][j] == background:
                    count += 1
                else:
                    break
            d = min(d, count)
        # Drop the component
        for i, j in component:
            new_i = i + d
            if new_i < height:
                new_g[new_i][j] = num
    return new_g
```