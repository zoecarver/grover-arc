```python
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [[0]]
    rows = len(g)
    cols = len(g[0])
    bg = g[0][0]

    def find_indicator_column_and_rows() -> Tuple[int, List[int]]:
        max_count = 0
        best_c = -1
        best_rows: List[int] = []
        for c in range(cols):
            ind_rs: List[int] = [r for r in range(rows) if g[r][c] != bg and g[r][c] != 0]
            if ind_rs:
                # Check isolation: no two consecutive rows
                isolated = all(ind_rs[i] >= ind_rs[i - 1] + 2 for i in range(1, len(ind_rs)))
                if isolated and len(ind_rs) > max_count:
                    max_count = len(ind_rs)
                    best_c = c
                    best_rows = ind_rs
        return best_c, best_rows

    ind_c, ind_rows = find_indicator_column_and_rows()
    if ind_c == -1 or not ind_rows:
        return [[0]]

    num_ind = len(ind_rows)
    ind_colors = [g[r][ind_c] for r in ind_rows]

    def get_strip_bounds() -> Tuple[int, int, int, int]:
        min_r = min(ind_rows)
        max_r = max(ind_rows)
        s = max(0, min_r - 1)
        e = min(rows - 1, max_r + 1)

        def can_expand_to(candidate_c: int, start_r: int, end_r: int) -> bool:
            if candidate_c < 0 or candidate_c >= cols:
                return False
            has_non_bg_non_zero = False
            has_zero = False
            for rr in range(start_r, end_r + 1):
                val = g[rr][candidate_c]
                if val != bg and val != 0:
                    has_non_bg_non_zero = True
                if val == 0:
                    has_zero = True
            return not has_non_bg_non_zero and has_zero

        strip_left = ind_c
        while strip_left > 0 and can_expand_to(strip_left - 1, s, e):
            strip_left -= 1

        strip_right = ind_c
        while strip_right < cols - 1 and can_expand_to(strip_right + 1, s, e):
            strip_right += 1

        return s, e, strip_left, strip_right

    s, e, strip_l, strip_r = get_strip_bounds()
    out_width = strip_r - strip_l + 1
    out_height = 2 * num_ind + 1

    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def count_components_for_color(color: int, strip_start_r: int, strip_end_r: int, strip_start_c: int, strip_end_c: int) -> int:
        visited = [[False] * cols for _ in range(rows)]
        component_count = 0
        for start_r in range(rows):
            for start_c in range(cols):
                if g[start_r][start_c] == color and not visited[start_r][start_c]:
                    # Explore full component
                    component: List[Tuple[int, int]] = []
                    stack: List[Tuple[int, int]] = [(start_r, start_c)]
                    visited[start_r][start_c] = True
                    component.append((start_r, start_c))
                    while stack:
                        cr, cc = stack.pop()
                        for dr, dc in dirs:
                            nr = cr + dr
                            nc = cc + dc
                            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                                visited[nr][nc] = True
                                stack.append((nr, nc))
                                component.append((nr, nc))
                    # Check if component touches strip
                    touches_strip = any(strip_start_r <= pr <= strip_end_r and strip_start_c <= pc <= strip_end_c for pr, pc in component)
                    if not touches_strip:
                        component_count += 1
        return component_count

    # Build output grid
    output = [[0] * out_width for _ in range(out_height)]
    for k in range(num_ind):
        out_row_idx = 2 * k + 1
        this_color = ind_colors[k]
        this_count = count_components_for_color(this_color, s, e, strip_l, strip_r)
        pos = 1  # Start at odd column 1 (0-based)
        for _ in range(this_count):
            if pos < out_width:
                output[out_row_idx][pos] = this_color
            pos += 2

    # Even rows are already all 0s

    return output
```