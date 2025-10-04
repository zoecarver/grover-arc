```python
from typing import List, Optional, Tuple

def get_colors(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int) -> set:
    colors = set()
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if g[r][c] not in (1, 4):
                colors.add(g[r][c])
    return colors

def get_bbox(g: List[List[int]], color: int, min_r: int, max_r: int, min_c: int, max_c: int) -> Optional[Tuple[int, int, int, int]]:
    positions = [(r, c) for r in range(min_r, max_r + 1) for c in range(min_c, max_c + 1) if g[r][c] == color]
    if not positions:
        return None
    minr = min(r for r, _ in positions)
    maxr = max(r for r, _ in positions)
    minc = min(c for _, c in positions)
    maxc = max(c for _, c in positions)
    return minr, maxr, minc, maxc

def fill(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, color: int):
    for r in range(max(0, min_r), min(len(g) - 1, max_r) + 1):
        for c in range(max(0, min_c), min(len(g[0]) - 1, max_c) + 1):
            g[r][c] = color

def has_overlap(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, color: int) -> bool:
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if 0 <= r < len(g) and 0 <= c < len(g[0]) and g[r][c] not in (1, 4) and g[r][c] != color:
                return True
    return False

def reflect_quadrant(g: List[List[int]], source_min_r: int, source_max_r: int, source_min_c: int, source_max_c: int,
                     target_min_r: int, target_max_r: int, target_min_c: int, target_max_c: int,
                     flip_x: bool, flip_y: bool, is_bottom: bool) -> List[List[int]]:
    out = [row[:] for row in g]
    colors = get_colors(out, source_min_r, source_max_r, source_min_c, source_max_c)
    red = 2
    red_source = get_bbox(out, red, source_min_r, source_max_r, source_min_c, source_max_c)
    red_target = get_bbox(out, red, target_min_r, target_max_r, target_min_c, target_max_c)
    has_red_target = red_target is not None
    orig_red_h = (red_source[1] - red_source[0] + 1) if red_source else 0
    orig_red_w = (red_source[3] - red_source[2] + 1) if red_source else 0
    if not has_red_target and red_source:
        minr, maxr, minc, maxc = red_source
        if flip_x:
            minc_new = 26 - maxc
            maxc_new = 26 - minc
        else:
            minc_new = minc
            maxc_new = maxc
        if flip_y:
            minr_new = 26 - maxr
            maxr_new = 26 - minr
        else:
            minr_new = minr
            maxr_new = maxr
        fill(out, minr_new, maxr_new, minc_new, maxc_new, red)
    for col in colors:
        if col == red:
            continue
        block_source = get_bbox(out, col, source_min_r, source_max_r, source_min_c, source_max_c)
        if not block_source:
            continue
        minr, maxr, minc, maxc = block_source
        h = maxr - minr + 1
        w = maxc - minc + 1
        if not has_red_target:
            if flip_x:
                minc_new = 26 - maxc
                maxc_new = 26 - minc
            else:
                minc_new = minc
                maxc_new = maxc
            if flip_y:
                minr_new = 26 - maxr
                maxr_new = 26 - minr
            else:
                minr_new = minr
                maxr_new = maxr
        else:
            minr_t, maxr_t, minc_t, maxc_t = red_target
            h_t = maxr_t - minr_t + 1
            w_t = maxc_t - minc_t + 1
            if not red_source:
                if flip_x:
                    minc_new = 26 - maxc
                    maxc_new = 26 - minc
                else:
                    minc_new = minc
                    maxc_new = maxc
                if flip_y:
                    minr_new = 26 - maxr
                    maxr_new = 26 - minr
                else:
                    minr_new = minr
                    maxr_new = maxr
            else:
                minr_s, maxr_s, minc_s, maxc_s = red_source
                y_overlap = max(minr, minr_s) <= min(maxr, maxr_s)
                x_overlap = max(minc, minc_s) <= min(maxc, maxc_s)
                left_attach = (maxc + 1 == minc_s) and y_overlap
                right_attach = (minc - 1 == maxc_s) and y_overlap
                above_attach = (maxr + 1 == minr_s) and x_overlap
                below_attach = (minr - 1 == maxr_s) and x_overlap
                if not (left_attach or right_attach or above_attach or below_attach):
                    if flip_x:
                        minc_new = 26 - maxc
                        maxc_new = 26 - minc
                    else:
                        minc_new = minc
                        maxc_new = maxc
                    if flip_y:
                        minr_new = 26 - maxr
                        maxr_new = 26 - minr
                    else:
                        minr_new = minr
                        maxr_new = maxr
                else:
                    h_new = max(1, h_t - h + orig_red_h)
                    w_new = max(1, w_t - w + orig_red_w)
                    if left_attach or right_attach:
                        minr_new = minr_t
                        maxr_new = maxr_t + h_new - h  # adjust for new h
                        if left_attach:
                            # no flip for horizontal in bottom
                            minc_new = minc_t - w_new
                            maxc_new = minc_t - 1
                        else:
                            minc_new = maxc_t + 1
                            maxc_new = minc_new + w_new - 1
                    else:
                        minc_new = minc_t
                        maxc_new = maxc_t + w_new - w
                        if above_attach:
                            # flip to below for bottom
                            minr_new = maxr_t + 1
                            maxr_new = minr_new + h_new - 1
                        elif below_attach:
                            # flip to above for bottom
                            maxr_new = minr_t - 1
                            minr_new = maxr_new - h_new + 1
        fill(out, minr_new, maxr_new, minc_new, maxc_new, col)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    # Reflect top: flip_x = True, flip_y = False
    out = reflect_quadrant(out, 0, 12, 0, 12, 0, 12, 14, 26, True, False, False)
    # Reflect bottom left: flip_x = False, flip_y = True
    out = reflect_quadrant(out, 0, 12, 0, 12, 14, 26, 0, 12, False, True, True)
    # Reflect bottom right: flip_x = False, flip_y = True
    out = reflect_quadrant(out, 0, 12, 14, 26, 14, 26, 14, 26, False, True, True)
    return out
```