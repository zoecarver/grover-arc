```python
from typing import List, Tuple
from collections import deque

def identify_background(g: List[List[int]]) -> int:
    """
    Identifies the background color as the color at the top-left corner (0,0).
    """
    return g[0][0]

def extract_objects(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """
    Extracts 8-connected components of same-color non-background cells using BFS.
    Returns list of (color, sorted_positions) where positions are in row-major order.
    """
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    objects = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                positions = []
                q = deque([(r, c)])
                visited[r][c] = True
                positions.append((r, c))
                while q:
                    cr, cc = q.popleft()
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                            positions.append((nr, nc))
                positions.sort(key=lambda p: (p[0], p[1]))
                objects.append((color, positions))
    return objects

def sort_components(objects: List[Tuple[int, List[Tuple[int, int]]]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """
    Sorts components by the row-major position of their first (top-left) cell.
    """
    def key_func(comp: Tuple[int, List[Tuple[int, int]]]) -> Tuple[int, int]:
        if comp[1]:
            first_r, first_c = comp[1][0]
            return (first_r, first_c)
        return (float('inf'), float('inf'))
    return sorted(objects, key=key_func)

def component_to_vertical(comp: Tuple[int, List[Tuple[int, int]]]) -> List[List[int]]:
    """
    Converts a component to vertical output: [[color]] for each cell in sorted positions.
    """
    color, positions = comp
    return [[color] for _ in positions]

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Main program: identifies background, extracts and sorts objects by start position,
    then concatenates their vertical representations.
    """
    bg = identify_background(g)
    objects = extract_objects(g, bg)
    sorted_objects = sort_components(objects)
    output = []
    for comp in sorted_objects:
        output.extend(component_to_vertical(comp))
    return output
```