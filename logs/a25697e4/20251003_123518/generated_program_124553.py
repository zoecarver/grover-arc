```python
from typing import List
from collections import Counter
import copy

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], background: int) -> List[tuple[int, List[tuple[int, int]]]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != background:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def touches_left(component: List[tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in component)

def get_bounding_box(component: List[tuple[int, int]]) -> tuple[int, int, int, int]:
    min_r = min(r for r, _ in component)
    max_r = max(r for r, _ in component)
    min_c = min(c for _, c in component)
    max_c = max(c for _, c in component)
    return min_r, max_r, min_c, max_c

def get_main_components(components: List[tuple[int, List[tuple[int, int]]]]) -> tuple[int, List[tuple[int, int]]]:
    main_color = None
    main_cells = []
    for color, comp in components:
        if touches_left(comp):
            if main_color is None:
                main_color = color
            if color == main_color:
                main_cells.extend(comp)
            else:
                # Assume only one main color
                pass
    return main_color, main_cells

def get_upper_lower_sizes(main_cells: List[tuple[int, int]], background: int, g: List[List[int]]) -> tuple[int, int]:
    # To find upper and lower components of main color
    # Re find components but only for main color cells
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    main_comp_sizes = []
    for r, c in main_cells:
        if not visited[r][c]:
            size = 0
            stack = [(r, c)]
            visited[r][c] = True
            while stack:
                x, y = stack.pop()
                size += 1
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == g[r][c]:
                        visited[nx][ny] = True
                        stack.append((nx, ny))
            main_comp_sizes.append(size)
    main_comp_sizes.sort(key=lambda s: [r for r, _ in main_cells if g[r][0] == g[main_cells[0][1]][0]] ) # Approximate
    if len(main_comp_sizes) >= 2:
        upper = main_comp_sizes[0]
        lower = main_comp_sizes[-1]
    else:
        upper = lower = sum(main_comp_sizes)
    return upper, lower

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    background = get_background(g)
    components = find_components(g, background)
    main_color, main_cells = get_main_components(components)
    if main_color is None:
        # No main, copy for now
        return [row[:] for row in g]
    # Remove noise
    out = [[background for _ in row] for row in g]
    for r, c in main_cells:
        out[r][c] = g[r][c]
    # Noise colors
    noise_colors = set(color for color, comp in components if color != main_color and color != background)
    if len(noise_colors) != 2:
        # Assume 2 for now
        return out
    c1, c2 = sorted(noise_colors)
    # Get upper lower
    upper, lower = get_upper_lower_sizes(main_cells, background, g)
    if upper > lower:
        inner_color = c2
        extension_color = c1
    else:
        inner_color = c1
        extension_color = c2
    # Bounding box for main
    min_r, max_r, min_c, max_c = get_bounding_box(main_cells)
    # Fill inner
    i = 0
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if out[r][c] == background:
                out[r][c] = inner_color
                i += 1
    # For extension, for now, fill next columns full
    h = max_r - min_r + 1
    e = 0
    c = max_c + 1
    while e < 8:  # Approximate E =8
        for r in range(min_r, max_r + 1):
            if c < len(out[0]) and out[r][c] == background:
                out[r][c] = extension_color
                e += 1
                if e >= 8:
                    break
        c += 1
        if c >= len(out[0]):
            break
    return out
```