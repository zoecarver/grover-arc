```python
from typing import List, Tuple
from collections import Counter, deque

def flatten_grid(g: List[List[int]]) -> List[int]:
    """
    Flattens the 2D grid into a 1D list in row-major order for frequency analysis.
    """
    return [cell for row in g for cell in row]

def find_background(flat: List[int]) -> int:
    """
    Identifies the background color as the most frequent value in the flattened grid.
    """
    if not flat:
        return 0  # Arbitrary for empty, but assumes non-empty
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def find_connected_components(g: List[List[int]], background: int) -> List[List[Tuple[int, int]]]:
    """
    Finds 4-connected components of same-color non-background cells using BFS, discovered in row-major order.
    Returns a list of lists, each containing the (row, col) positions of cells in a component.
    """
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = set()
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-connected
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != background and (i, j) not in visited:
                component = []
                color = g[i][j]
                queue = deque([(i, j)])
                visited.add((i, j))
                while queue:
                    x, y = queue.popleft()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < rows and 0 <= ny < cols and
                            (nx, ny) not in visited and g[nx][ny] == color):
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                components.append(component)
    return components

def compute_top_left(component: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Computes the top-left position for a component: min row, then min col among cells in that min row.
    """
    if not component:
        return (0, 0)  # Arbitrary for empty
    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component if r == min_r)
    return (min_r, min_c)

def get_component_info(components: List[List[Tuple[int, int]]], g: List[List[int]]) -> List[Tuple[Tuple[int, int], int, int]]:
    """
    Extracts info for each component: (top-left, color, size).
    """
    info = []
    for comp in components:
        if comp:
            color = g[comp[0][0]][comp[0][1]]  # All same color
            size = len(comp)
            top_left = compute_top_left(comp)
            info.append((top_left, color, size))
    return info

def sort_components(info: List[Tuple[Tuple[int, int], int, int]]) -> List[Tuple[Tuple[int, int], int, int]]:
    """
    Sorts components by top-left position: first by row, then by column.
    """
    return sorted(info, key=lambda t: t[0])

def build_stacked_output(ordered_info: List[Tuple[Tuple[int, int], int, int]]) -> List[List[int]]:
    """
    Builds the output by stacking vertical bars: for each component, append size rows of [color].
    """
    result = []
    for _, color, size in ordered_info:
        result.extend([[color]] * size)
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: orchestrates background detection, component extraction, sorting, and output building.
    """
    flat = flatten_grid(g)
    background = find_background(flat)
    components = find_connected_components(g, background)
    info = get_component_info(components, g)
    ordered_info = sort_components(info)
    return build_stacked_output(ordered_info)
```