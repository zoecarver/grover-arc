```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
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

def touches_left(component: List[Tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in component)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    components = find_components(g, bg)
    anchored_comps = [comp for comp in components if touches_left(comp[1])]
    if anchored_comps:
        main_color = anchored_comps[0][0]
        main_subs = [comp for comp in components if comp[0] == main_color and touches_left(comp[1])]
        if len(main_subs) != 2:
            return [row[:] for row in g]
        main_subs = sorted(main_subs, key=lambda comp: min(r for r, _ in comp[1]))
        upper_main = main_subs[0]
        lower_main = main_subs[1]
        size_u = len(upper_main[1])
        size_l = len(lower_main[1])
        noise_comps = [comp for comp in components if comp[0] != bg and comp[0] != main_color and not touches_left(comp[1])]
        noise_colors = list(set(comp[0] for comp in noise_comps))
        if len(noise_colors) != 2:
            return [row[:] for row in g]
        min_row_dict = {}
        for nc in noise_colors:
            positions = [p for compp in [comp for comp in noise_comps if comp[0] == nc] for p in compp[1]]
            if positions:
                min_row_dict[nc] = min(r for r, _ in positions)
            else:
                min_row_dict[nc] = rows
        sorted_noises = sorted(noise_colors, key=lambda c: min_row_dict[c])
        upper_noise = sorted_noises[0]
        lower_noise = sorted_noises[1]
        if size_u > size_l:
            inner = lower_noise
            outer = upper_noise
        else:
            inner = upper_noise
            outer = lower_noise
        out = [[bg for _ in range(cols)] for _ in range(rows)]
        all_main_pos = [(r, c) for comp in main_subs for r, c in comp[1]]
        for r, c in all_main_pos:
            out[r][c] = main_color
        left_counts = [sum(1 for j in range(min(4, cols)) if g[i][j] == main_color) for i in range(rows)]
        middle_row_cands = [i for i in range(rows) if left_counts[i] == 2]
        if len(middle_row_cands) != 1:
            return [row[:] for row in g]
        middle_row = middle_row_cands[0]
        top_row_cands = [i for i in range(middle_row) if left_counts[i] == 4]
        if not top_row_cands:
            return [row[:] for row in g]
        top_row = min(top_row_cands)
        bottom_row_cands = [i for i in range(middle_row + 1, rows) if left_counts[i] == 4]
        if not bottom_row_cands:
            return [row[:] for row in g]
        bottom_row = max(bottom_row_cands)
        gap_rows = [i for i in range(top_row + 1, bottom_row) if left_counts[i] == 0]
        if len(gap_rows) != 1:
            return [row[:] for row in g]
        gap_row = gap_rows[0]
        for j in range(min(4, cols)):
            if out[middle_row][j] == bg:
                out[middle_row][j] = inner
        for j in range(min(4, cols)):
            out[gap_row][j] = inner
        for j in range(4, min(9, cols)):
            out[middle_row][j] = outer
        if 8 < cols:
            out[gap_row][8] = outer
        if top_row + 1 < rows and left_counts[top_row + 1] == 0:
            if 8 < cols:
                out[top_row][8] = outer
            if 9 < cols:
                out[top_row][9] = outer
        if bottom_row - 1 >= 0 and left_counts[bottom_row - 1] == 0:
            if 8 < cols:
                out[bottom_row][8] = outer
            if 9 < cols:
                out[bottom_row][9] = outer
        return out
    else:
        out = [[bg for _ in range(cols)] for _ in range(rows)]
        for color, pos_list in components:
            max_r = max(r for r, _ in pos_list)
            max_c = max(c for _, c in pos_list)
            if max_r + 1 < rows and max_c + 6 < cols:
                for r, c in pos_list:
                    out[r + 1][c + 6] = color
            else:
                for r, c in pos_list:
                    out[r][c] = color
        return out
```