```python
def get_components(g: List[List[int]], start_row: int = 6) -> list[dict]:
    h, w = 24, 24
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(start_row, h):
        for c in range(w):
            if not visited[r][c] and g[r][c] not in (0, 5):
                color = g[r][c]
                component_cells = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    component_cells.append((cr, cc))
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if start_row <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append({
                    'color': color,
                    'pixels': len(component_cells),
                    'cells': component_cells
                })
    return components

def get_background(g: List[List[int]]) -> int:
    comps = get_components(g)
    if not comps:
        return 3  # default if none
    return max(comps, key=lambda x: x['pixels'])['color']

def get_top_bars(g: List[List[int]]) -> list[int]:
    bars = []
    for c in range(24):
        col_values = [g[r][c] for r in range(1, 5)]
        if all(v == col_values[0] for v in col_values) and col_values[0] not in (0, 5):
            bars.append(c)
    return bars

def get_maroon_bbox(g: List[List[int]]) -> tuple[int, int, int, int]:
    min_r, max_r, min_c, max_c = 24, -1, 24, -1
    for r in range(6, 24):
        for c in range(24):
            if g[r][c] == 8:
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    return min_r, max_r, min_c, max_c

def get_translated_rectangles(g: List[List[int]], bg: int) -> list[dict]:
    comps = get_components(g)
    return [comp for comp in comps if comp['color'] != bg and comp['color'] != 8 and 24 <= comp['pixels'] <= 63]

def get_bottom_component(translated: list[dict]) -> dict:
    if not translated:
        return None
    return max(translated, key=lambda x: max(cell[0] for cell in x['cells']))

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    out = [[bg for _ in range(24)] for _ in range(24)]
    translated = get_translated_rectangles(g, bg)
    for comp in translated:
        color = comp['color']
        for r, c in comp['cells']:
            new_r = r - 6
            if 0 <= new_r < 24:
                out[new_r][c] = color
    min_r, max_r, min_c, max_c = get_maroon_bbox(g)
    shifted_min_r = min_r - 6
    shifted_max_r = max_r - 6
    anchor_width = max_c - min_c + 1
    anchor_slot = min_c // 6
    bars = get_top_bars(g)
    relative3 = bars[2] - 12 if len(bars) == 4 else 1
    # Compute beam_left and beam_right using shifted_min_r as representative anchor row
    r_anchor = shifted_min_r
    # Find left translated right edge left of min_c
    left_trans_right = -1
    for c in range(min_c):
        if out[r_anchor][c] != bg:
            left_trans_right = c
    beam_left = left_trans_right + 1 if left_trans_right >= 0 else 0
    # Find right translated left edge right of max_c
    right_trans_left = 24
    for c in range(max_c + 1, 24):
        if out[r_anchor][c] != bg:
            right_trans_left = c
            break
    beam_right = right_trans_left - 1 if right_trans_left < 24 else 23
    # Fill beam at anchor rows
    for r in range(shifted_min_r, shifted_max_r + 1):
        for c in range(beam_left, beam_right + 1):
            out[r][c] = 8
    # Upper pillars
    if anchor_slot == 2:
        left_upper_start = 8
        right_upper_start = 16
    else:  # 3
        left_upper_start = beam_left
        right_upper_start = beam_right - 1
    pillar_width = 2
    for start_c in [left_upper_start, right_upper_start]:
        for c in range(start_c, start_c + pillar_width):
            for r in range(0, shifted_min_r):
                if 0 <= c < 24:
                    out[r][c] = 8  # place always, as support
    # Lower pillars: left beam end and anchor
    left_lower_start = beam_left
    left_lower_width = 2
    anchor_lower_start = min_c
    anchor_lower_width = anchor_width
    for r in range(shifted_max_r + 1, 24):
        # left lower pillar
        for c in range(left_lower_start, min(left_lower_start + left_lower_width, 24)):
            if out[r][c] == bg:
                out[r][c] = 8
        # anchor lower pillar
        for c in range(anchor_lower_start, min(anchor_lower_start + anchor_lower_width, 24)):
            if out[r][c] == bg:
                out[r][c] = 8
    # Lower beam
    bottom_comp = get_bottom_component(translated)
    if bottom_comp:
        bottom_shifted_min_r = min(cell[0] for cell in bottom_comp['cells']) - 6
        lower_beam_row = bottom_shifted_min_r - 1
        if 0 <= lower_beam_row < 24:
            if anchor_slot == 2:
                start_col = beam_left if relative3 == 1 else min_c
                end_col = 23
            else:
                start_col = beam_left
                end_col = max_c
            for c in range(start_col, end_col + 1):
                if out[lower_beam_row][c] == bg:
                    out[lower_beam_row][c] = 8
    return out
```