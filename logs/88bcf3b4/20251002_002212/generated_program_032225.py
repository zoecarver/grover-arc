```python
from typing import List, Tuple, Dict
from collections import Counter, deque

def find_background(g: List[List[int]]) -> int:
    """Identify the background as the most common value."""
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_non_background_colors(g: List[List[int]], bg: int) -> set:
    """Get set of non-background colors."""
    return {cell for row in g for cell in row if cell != bg}

def is_vertical_bar(positions: List[Tuple[int, int]]) -> bool:
    """Check if positions form a straight vertical bar."""
    if not positions:
        return False
    cols = {c for r, c in positions}
    if len(cols) != 1:
        return False
    col = next(iter(cols))
    rows = sorted(r for r, c in positions)
    if len(rows) != len(positions):
        return False
    for i in range(1, len(rows)):
        if rows[i] != rows[i - 1] + 1:
            return False
    return True

def is_horizontal_bar(positions: List[Tuple[int, int]]) -> bool:
    """Check if positions form a straight horizontal bar."""
    if not positions:
        return False
    rows = {r for r, c in positions}
    if len(rows) != 1:
        return False
    row = next(iter(rows))
    cols = sorted(c for r, c in positions)
    if len(cols) != len(positions):
        return False
    for i in range(1, len(cols)):
        if cols[i] != cols[i - 1] + 1:
            return False
    return True

def is_bar(positions: List[Tuple[int, int]]) -> bool:
    """Check if positions form a bar (horizontal or vertical)."""
    return is_vertical_bar(positions) or is_horizontal_bar(positions)

def get_connected_components_per_color(g: List[List[int]], bg: int) -> Dict[int, List[List[Tuple[int, int]]]]:
    """Find 8-connected components per non-background color."""
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components: Dict[int, List[List[Tuple[int, int]]]] = {}
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != bg and not visited[i][j]:
                color = g[i][j]
                if color not in components:
                    components[color] = []
                comp = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components[color].append(comp)
    return components

def get_all_positions(g: List[List[int]], color: int) -> List[Tuple[int, int]]:
    """Get all positions of a specific color."""
    n = len(g)
    positions = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == color:
                positions.append((i, j))
    return positions

def find_fixed_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int]]]:
    """Find 8-connected components of remaining non-background cells (color-blind)."""
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != bg and not visited[i][j]:
                comp = []
                queue = deque([(i, j)])
                visited[i][j] = True
                while queue:
                    x, y = queue.popleft()
                    comp.append((x, y))
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] != bg:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                components.append(comp)
    return components

def get_component_min_c(comp: List[Tuple[int, int]]) -> int:
    """Get minimum column of component."""
    return min(c for r, c in comp)

def place_bridge(g: List[List[int]], upper_comp: List[Tuple[int, int]], lower_comp: List[Tuple[int, int]], color: int, N: int, bg: int, n: int) -> None:
    """Place bridge pixels using linear interpolation, shifting left if occupied."""
    upper_min_c = get_component_min_c(upper_comp)
    lower_min_c = get_component_min_c(lower_comp)
    start_col = upper_min_c - 1
    end_col = lower_min_c - 1
    delta_c = end_col - start_col
    upper_max_r = max(r for r, c in upper_comp)
    lower_min_r = min(r for r, c in lower_comp)
    end_row = lower_min_r - 1
    start_row = max(0, lower_min_r - N)
    num_possible = end_row - start_row + 1
    placed = 0
    for k in range(min(N, num_possible)):
        row = start_row + k
        fraction = k / max(1, num_possible - 1)
        col = round(start_col + fraction * delta_c)
        placed_pos = False
        for shift in range(0, n):
            test_col = col - shift
            if 0 <= test_col < n and g[row][test_col] == bg:
                g[row][test_col] = color
                placed += 1
                placed_pos = True
                break
        if not placed_pos:
            # place at original col if possible
            if 0 <= col < n and g[row][col] == bg:
                g[row][col] = color
                placed += 1
    # place remaining below end_row if any
    current_row = end_row + 1
    for k in range(placed, N):
        if current_row >= n:
            break
        col = end_col
        if 0 <= col < n and g[current_row][col] == bg:
            g[current_row][col] = color
        current_row += 1

def place_fallback(g: List[List[int]], fixed_comp: List[Tuple[int, int]], color: int, N: int, bg: int, n: int) -> None:
    """Place pixels vertically below the fixed component in center column."""
    if not fixed_comp:
        return
    center_c = round(sum(c for r, c in fixed_comp) / len(fixed_comp))
    max_r = max(r for r, c in fixed_comp)
    current_row = max_r + 1
    placed = 0
    while placed < N and current_row < n:
        col = center_c
        if 0 <= col < n and g[current_row][col] == bg:
            g[current_row][col] = color
            placed += 1
        current_row += 1

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program composing rules for puzzle solving."""
    n = len(g)
    if n == 0:
        return g
    out = [row[:] for row in g]
    bg = find_background(g)
    components = get_connected_components_per_color(g, bg)
    erased_colors = []
    for color in sorted(components):
        comp_list = components[color]
        has_non_bar_large = any(len(comp) > 3 and not is_bar(comp) for comp in comp_list)
        if has_non_bar_large:
            positions = get_all_positions(g, color)
            total_n = len(positions)
            for r, c in positions:
                out[r][c] = bg
            erased_colors.append((color, total_n))
    fixed_comps = find_fixed_components(out, bg)
    fixed_comps.sort(key=lambda comp: min((r for r, c in comp), default=n))
    erased_idx = 0
    num_gaps = len(fixed_comps) - 1
    for i in range(num_gaps):
        if erased_idx >= len(erased_colors):
            break
        upper = fixed_comps[i]
        lower = fixed_comps[i + 1]
        color, n_pixels = erased_colors[erased_idx]
        place_bridge(out, upper, lower, color, n_pixels, bg, n)
        erased_idx += 1
    # place remaining erased below the last fixed component
    if fixed_comps:
        last_comp = fixed_comps[-1]
        for j in range(erased_idx, len(erased_colors)):
            color, n_pixels = erased_colors[j]
            place_fallback(out, last_comp, color, n_pixels, bg, n)
    else:
        # no fixed components, place erased at top in row-major order
        idx = 0
        for color, n_pixels in erased_colors:
            for k in range(n_pixels):
                row = idx // n
                col = idx % n
                if row < n:
                    out[row][col] = color
                idx += 1
    return out
```