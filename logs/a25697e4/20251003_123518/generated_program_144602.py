```python
from typing import List, Tuple
from collections import Counter, defaultdict

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

def touches_bottom(component: List[Tuple[int, int]], h: int) -> bool:
    return any(r == h - 1 for r, c in component)

def has_anchored(g: List[List[int]], bg: int) -> bool:
    return any(row[0] != bg for row in g)

def count_main_left(g: List[List[int]], r: int, main_color: int, w: int) -> int:
    return sum(1 for j in range(min(4, w)) if g[r][j] == main_color)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    if w == 0 or h == 0:
        return g
    if has_anchored(g, bg):
        # Anchored case: reconstruction
        left_colors = {g[r][0] for r in range(h) if g[r][0] != bg}
        if len(left_colors) != 1:
            return [[cell for cell in row] for row in g]
        main_color = next(iter(left_colors))
        all_comps = find_components(g, bg)
        main_subs = [comp for comp in all_comps if comp[0] == main_color and touches_left(comp[1])]
        if len(main_subs) != 2:
            out = [[bg] * w for _ in range(h)]
            for _, pos in main_subs:
                for r, c in pos:
                    out[r][c] = main_color
            return out
        main_subs.sort(key=lambda comp: min(r for r, _ in comp[1]))
        # Noise
        noise_comps = [comp for comp in all_comps if comp[0] != bg and comp[0] != main_color and not touches_left(comp[1])]
        noise_color_set = set(comp[0] for comp in noise_comps)
        if len(noise_color_set) != 2:
            out = [[bg] * w for _ in range(h)]
            for _, pos in main_subs:
                for r, c in pos:
                    out[r][c] = main_color
            return out
        noise_by_color = defaultdict(list)
        for color, pos in noise_comps:
            noise_by_color[color].append(pos)
        noise_colors = list(noise_by_color)
        min_rows = {color: min(min(r for r, _ in poss) for poss in noise_by_color[color]) for color in noise_colors}
        noise_colors.sort(key=lambda c: min_rows[c])
        upper_noise, lower_noise = noise_colors
        # Structural rows
        left_counts = [(r, count_main_left(g, r, main_color, w)) for r in range(h)]
        full_rows = [r for r, cnt in left_counts if cnt == 4]
        partial_rows = [r for r, cnt in left_counts if cnt == 2]
        zero_rows = [r for r, cnt in left_counts if cnt == 0]
        if len(full_rows) != 2 or len(partial_rows) != 1 or len(zero_rows) != 1:
            out = [[bg] * w for _ in range(h)]
            for _, pos in main_subs:
                for r, c in pos:
                    out[r][c] = main_color
            return out
        full_rows.sort()
        top_r, bottom_r = full_rows
        middle_r = partial_rows[0]
        gap_r = zero_rows[0]
        if not (top_r < gap_r < bottom_r and top_r < middle_r < bottom_r and gap_r != middle_r):
            out = [[bg] * w for _ in range(h)]
            for _, pos in main_subs:
                for r, c in pos:
                    out[r][c] = main_color
            return out
        # Assign inner/outer
        if gap_r < middle_r:
            inner = upper_noise
            outer = lower_noise
            adjacent_r = top_r
        else:
            inner = lower_noise
            outer = upper_noise
            adjacent_r = bottom_r
        # Build out
        out = [[bg] * w for _ in range(h)]
        # Place main subs
        for _, pos in main_subs:
            for r, c in pos:
                out[r][c] = main_color
        # Fill inner in left 4 cols for middle and gap where bg
        for rr in [middle_r, gap_r]:
            for j in range(min(4, w)):
                if out[rr][j] == bg:
                    out[rr][j] = inner
        # Fill outer in middle cols 4-8 where bg
        for j in range(4, min(9, w)):
            if out[middle_r][j] == bg:
                out[middle_r][j] = outer
        # Fill outer in gap col 8 where bg
        if w > 8:
            j = 8
            if out[gap_r][j] == bg:
                out[gap_r][j] = outer
        # Fill outer in adjacent cols 8-9 where bg
        for j in [8, 9] if w > 9 else [8]:
            if j < w and out[adjacent_r][j] == bg:
                out[adjacent_r][j] = outer
        return out
    else:
        # Unanchored case: move non-bottom-touching components +1 down +6 right if possible
        all_comps = find_components(g, bg)
        stayers = [comp for comp in all_comps if touches_bottom(comp[1], h)]
        movables = [comp for comp in all_comps if not touches_bottom(comp[1], h)]
        # Sort movables bottom-first
        movables.sort(key=lambda comp: -min(r for r, _ in comp[1]))
        out = [[bg] * w for _ in range(h)]
        # Place stayers
        for color, pos in stayers:
            for r, c in pos:
                out[r][c] = color
        # Place movables
        dr, dc = 1, 6
        for color, pos in movables:
            new_pos_list = [(r + dr, c + dc) for r, c in pos]
            if all(0 <= nr < h and 0 <= nc < w for nr, nc in new_pos_list) and all(out[nr][nc] == bg for nr, nc in new_pos_list):
                # Place at new
                for nr, nc in new_pos_list:
                    out[nr][nc] = color
            else:
                # Place at original
                for r, c in pos:
                    out[r][c] = color
        return out
```