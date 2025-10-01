```python
from typing import List, Tuple
from collections import Counter, deque

def find_background(g: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent value in the grid.
    """
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def get_component_sizes_and_colors(g: List[List[int]], bg: int) -> List[Tuple[int, int]]:
    """
    Finds 4-connected components of same-color non-background cells in row-major discovery order.
    Returns list of (color, size) tuples in the order components are discovered.
    """
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = set()
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if (i, j) in visited or g[i][j] == bg:
                continue
            color = g[i][j]
            size = 0
            queue = deque([(i, j)])
            visited.add((i, j))
            while queue:
                x, y = queue.popleft()
                size += 1
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and g[nx][ny] == color:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            components.append((color, size))
    return components

def build_output(components: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Builds the output by stacking vertical bars: for each component, append size rows of [color].
    """
    result = []
    for color, size in components:
        result.extend([[color]] * size)
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: finds background, gets components in discovery order, and builds the stacked output.
    """
    bg = find_background(g)
    comps = get_component_sizes_and_colors(g, bg)
    return build_output(comps)
```