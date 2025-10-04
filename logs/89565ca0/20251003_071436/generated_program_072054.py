```python
from typing import List, Tuple

def find_non_zero_colors(g: List[List[int]]) -> set:
    """Find all distinct non-zero colors in the grid."""
    colors = set()
    for row in g:
        for cell in row:
            if cell != 0:
                colors.add(cell)
    return colors

def num_connected_components(g: List[List[int]], c: int) -> int:
    """Compute the number of 8-connected components for color c in the grid."""
    if not g:
        return 0
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    count = 0
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == c and not visited[i][j]:
                count += 1
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == c and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
    return count

def select_filler(colors: set, comp: dict) -> int:
    """Select the filler color as the one with the maximum number of components."""
    if not colors:
        return 0
    return max(colors, key=lambda cc: comp[cc])

def sort_other_colors(others: list, comp: dict) -> list:
    """Sort other colors by increasing number of components, then by color value."""
    return sorted(others, key=lambda cc: (comp[cc], cc))

def build_output_row(c: int, w: int, filler: int) -> List[int]:
    """Build a single output row for color c with width w, filled with filler."""
    return [c] * w + [filler] * (4 - w)

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to generate the small grid based on connected components rules."""
    colors = find_non_zero_colors(g)
    if not colors:
        return []
    comp = {c: num_connected_components(g, c) for c in colors}
    filler = select_filler(colors, comp)
    others = [c for c in colors if c != filler]
    sorted_others = sort_other_colors(others, comp)
    result = []
    for c in sorted_others:
        w = comp[c]
        row = build_output_row(c, w, filler)
        result.append(row)
    return result
```