```python
from typing import List, Set, Tuple

def get_colors(g: List[List[int]]) -> Set[int]:
    """Extract all unique non-zero colors from the grid."""
    colors: Set[int] = set()
    for row in g:
        for val in row:
            if val != 0:
                colors.add(val)
    return colors

def find_components(g: List[List[int]], c: int) -> List[List[Tuple[int, int]]]:
    """Find all 4-connected components for a specific color c."""
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == c and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == c and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(comp)
    return components

def is_h_shape(comp: List[Tuple[int, int]], c: int, g: List[List[int]], rows: int, cols: int) -> bool:
    """Check if a component forms a valid H shape of width 3 with alternating full and split rows."""
    if not comp:
        return False
    min_j = min(j for i, j in comp)
    max_j = max(j for i, j in comp)
    if max_j - min_j + 1 != 3:
        return False
    min_i = min(i for i, j in comp)
    max_i = max(i for i, j in comp)
    height = max_i - min_i + 1
    if height % 2 == 0:
        return False
    for rel_r in range(height):
        abs_r = min_i + rel_r
        js = sorted(j for ii, jj in comp if ii == abs_r)
        if rel_r % 2 == 0:  # full row
            if len(js) != 3 or js != [min_j, min_j + 1, min_j + 2]:
                return False
            if any(g[abs_r][j] != c for j in js):
                return False
        else:  # split row
            if len(js) != 2 or js != [min_j, min_j + 2]:
                return False
            if g[abs_r][min_j + 1] != 0:
                return False
    return True

def find_main_h_color(g: List[List[int]]) -> int:
    """Find the color for H type: the color of the leftmost valid H component."""
    rows = len(g)
    cols = len(g[0])
    min_left = cols
    best_c = 0
    for c in get_colors(g):
        components = find_components(g, c)
        h_comps = [comp for comp in components if is_h_shape(comp, c, g, rows, cols)]
        if h_comps:
            left_min = min(min(j for i, j in comp) for comp in h_comps)
            if left_min < min_left:
                min_left = left_min
                best_c = c
    return best_c

def generate_h_output(g: List[List[int]], c: int) -> List[List[int]]:
    """Generate the stacked H pattern output for the given color."""
    rows = len(g)
    cols = len(g[0])
    components = find_components(g, c)
    h_comps = [comp for comp in components if is_h_shape(comp, c, g, rows, cols)]
    if len(h_comps) < 2:
        return []
    h_comps.sort(key=lambda comp: min(j for i, j in comp))
    patterns = []
    for comp in h_comps:
        min_i = min(i for i, j in comp)
        max_i = max(i for i, j in comp)
        min_j = min(j for i, j in comp)
        comp_pat = []
        valid = True
        for r in range(min_i, max_i + 1):
            js = sorted(j for ii, jj in comp if ii == r)
            if len(js) == 3 and js == [min_j, min_j + 1, min_j + 2]:
                comp_pat.append([c, c, c])
            elif len(js) == 2 and js == [min_j, min_j + 2]:
                comp_pat.append([c, 0, c])
            else:
                valid = False
                break
        if valid and len(comp_pat) == max_i - min_i + 1:
            patterns.append(comp_pat)
        else:
            return []
    total = patterns[0]
    for p in patterns[1:]:
        total.append([c, 0, c])
        total.extend(p)
    return total

def is_u_shape(comp: List[Tuple[int, int]]) -> bool:
    """Check if a component forms the exact U shape with 9 cells over 5 rows and 3 columns."""
    if len(comp) != 9:
        return False
    min_i = min(i for i, j in comp)
    max_i = max(i for i, j in comp)
    if max_i - min_i + 1 != 5:
        return False
    min_j = min(j for i, j in comp)
    max_j = max(j for i, j in comp)
    if max_j - min_j + 1 != 3:
        return False
    positions = {(i - min_i, j - min_j) for i, j in comp}
    expected = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 0), (4, 0), (4, 1), (4, 2)}
    return positions == expected

def find_u_color(g: List[List[int]]) -> int:
    """Find the color with a U-shaped component."""
    for c in get_colors(g):
        components = find_components(g, c)
        for comp in components:
            if is_u_shape(comp):
                return c
    return 0

def generate_u_output(c: int) -> List[List[int]]:
    """Generate the 6x3 U pattern filled with color c."""
    top = [c] * 6
    middle = [c] + [0] * 5
    bottom = [c] * 6
    return [top, middle, bottom]

def find_components_non_zero(g: List[List[int]]) -> List[List[Tuple[int, int]]]:
    """Find all 4-connected components of any non-zero cells."""
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != 0 and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] != 0 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(comp)
    return components

def generate_pair_output(g: List[List[int]]) -> List[List[int]]:
    """Generate the 2xN pair output from bottom to top using left and right edge colors of the main component."""
    all_comps = find_components_non_zero(g)
    if not all_comps:
        return []
    main_comp = max(all_comps, key=len)
    row_set = set(i for i, j in main_comp)
    non_empty_rows = sorted(list(row_set), reverse=True)  # bottom to top
    output = []
    for r in non_empty_rows:
        js = [j for i, j in main_comp if i == r]
        if js:
            min_j = min(js)
            max_j = max(js)
            left_c = g[r][min_j]
            right_c = g[r][max_j]
            output.append([left_c, right_c])
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: detect type and generate output using composed rules."""
    # Rule 1: Check for U type
    u_c = find_u_color(g)
    if u_c != 0:
        return generate_u_output(u_c)
    # Rule 2: Check for H type
    h_c = find_main_h_color(g)
    if h_c != 0:
        return generate_h_output(g, h_c)
    # Rule 3: Default to pair type
    return generate_pair_output(g)
```