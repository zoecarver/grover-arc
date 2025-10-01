```python
from typing import List, Tuple
from collections import Counter, deque

def find_background(g: List[List[int]]) -> int:
    """
    Identifies the background color as the most frequent value in the grid.
    """
    if not g or not g[0]:
        raise ValueError("Empty grid")
    flat = [cell for row in g for cell in row]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def get_components(g: List[List[int]], background: int) -> List[Tuple[int, int, int, int]]:
    """
    Finds same-color 4-connected components of non-background cells, discovered in row-major order.
    Returns list of (min_row, min_col, color, size) for each component.
    """
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    components = []
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited and g[i][j] != background:
                color = g[i][j]
                queue = deque([(i, j)])
                visited.add((i, j))
                min_row = i
                min_col = j
                size = 1
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and g[nx][ny] == color:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                            size += 1
                            min_row = min(min_row, nx)
                            min_col = min(min_col, ny)
                components.append((min_row, min_col, color, size))
    return components

def order_components(components: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
    """
    Sorts components by increasing min_row, then by increasing min_col.
    """
    return sorted(components, key=lambda t: (t[0], t[1]))

def build_output(ordered_components: List[Tuple[int, int, int, int]]) -> List[List[int]]:
    """
    Builds the output by stacking vertical bars for each component: size rows of [color].
    """
    result = []
    for _, _, color, size in ordered_components:
        result.extend([[color]] * size)
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: finds background, gets components, orders them, and builds the stacked output.
    """
    background = find_background(g)
    components = get_components(g, background)
    ordered = order_components(components)
    return build_output(ordered)
```