```python
from typing import List, Tuple

def identify_background(g: List[List[int]]) -> int:
    """
    Rule: Background color is always at position (0,0).
    """
    return g[0][0] if g and g[0] else 0

def find_components(g: List[List[int]], bg: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """
    Rule: Extract 8-connected components of same-color non-background cells using iterative DFS.
    Collect positions for each component.
    """
    if not g or not g[0]:
        return []
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    def dfs(start_r: int, start_c: int, color: int) -> List[Tuple[int, int]]:
        stack = [(start_r, start_c)]
        positions = []
        while stack:
            cr, cc = stack.pop()
            if visited[cr][cc]:
                continue
            visited[cr][cc] = True
            positions.append((cr, cc))
            for dr, dc in directions:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                    stack.append((nr, nc))
        return positions
    
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                positions = dfs(r, c, color)
                positions.sort(key=lambda p: (p[0], p[1]))
                components.append((color, positions))
    return components

def get_top_left_key(comp: Tuple[int, List[Tuple[int, int]]]) -> Tuple[int, int]:
    """
    Observation: Sort components by the minimum row, then minimum column in that row (top-left position).
    """
    positions = comp[1]
    if not positions:
        return (float('inf'), float('inf'))
    min_row = min(p[0] for p in positions)
    min_col = min(p[1] for p in positions if p[0] == min_row)
    return (min_row, min_col)

def sort_components(components: List[Tuple[int, List[Tuple[int, int]]]]) -> List[Tuple[int, List[Tuple[int, int]]]]:
    """
    Rule: Sort extracted components by their top-left position in row-major order.
    """
    return sorted(components, key=get_top_left_key)

def component_to_vertical(comp: Tuple[int, List[Tuple[int, int]]]) -> List[List[int]]:
    """
    Rule: For each component, output a vertical stack of [color] for each position in row-major order.
    """
    color, positions = comp
    return [[color] for _ in positions]

def to_vertical_output(components: List[Tuple[int, List[Tuple[int, int]]]]) -> List[List[int]]:
    """
    Transformation: Concatenate vertical representations of all sorted components.
    """
    output = []
    for comp in components:
        output.extend(component_to_vertical(comp))
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """
    Composes all rules: identify background, find components, sort them, and generate vertical output.
    """
    bg = identify_background(g)
    components = find_components(g, bg)
    sorted_components = sort_components(components)
    return to_vertical_output(sorted_components)
```