```python
from typing import List, Tuple
from collections import Counter

def shift_up(g: List[List[int]]) -> List[List[int]]:
    W = len(g[0])
    H_out = 19
    out = [[0] * W for _ in range(H_out)]
    for r in range(18):
        out[r] = g[r + 6][:]
    out[18] = g[23][:]
    return out

def find_background(g: List[List[int]]) -> int:
    count = Counter()
    W = len(g[0])
    for r in range(6, 24):
        for c in range(W):
            col = g[r][c]
            if col > 0 and col != 5:
                count[col] += 1
    if count:
        return count.most_common(1)[0][0]
    return 0

def find_components(g: List[List[int]], C: int) -> List[Tuple[int, int, int, int, int, int]]:
    W = len(g[0])
    H = len(g)
    visited = [[False] * W for _ in range(H)]
    components = []
    for r in range(H):
        for c in range(W):
            if g[r][c] != C and g[r][c] != 0 and g[r][c] != 5 and not visited[r][c]:
                color = g[r][c]
                max_c = c
                while max_c + 1 < W and g[r][max_c + 1] == color and not visited[r][max_c + 1]:
                    max_c += 1
                max_r = r
                while max_r + 1 < H:
                    can_expand = True
                    for cc in range(c, max_c + 1):
                        if g[max_r + 1][cc] != color or visited[max_r + 1][cc]:
                            can_expand = False
                            break
                    if not can_expand:
                        break
                    max_r += 1
                for rr in range(r, max_r + 1):
                    for cc in range(c, max_c + 1):
                        visited[rr][cc] = True
                size = (max_r - r + 1) * (max_c - c + 1)
                if size >= 4:
                    components.append((color, r, max_r, c, max_c, size))
    return components

def get_left_support_start(components: List[Tuple[int, int, int, int, int, int]]) -> int:
    non_maroon = [comp for comp in components if comp[0] != 8]
    if not non_maroon:
        return 4
    left_comp = min(non_maroon, key=lambda x: x[3])
    return left_comp[4] + 1

def get_maroon_comp(components: List[Tuple[int, int, int, int, int, int]]) -> Tuple[int, int, int, int, int, int]:
    for comp in components:
        if comp[0] == 8:
            return comp
    return (8, 0, 0, 0, 0, 0)  # fallback, but assume exists

def get_bottom_comp(components: List[Tuple[int, int, int, int, int, int]]) -> Tuple[int, int, int, int, int, int]:
    non_maroon = [comp for comp in components if comp[0] != 8]
    if not non_maroon:
        return (0, 24, 24, 0, 0, 0)
    return max(non_maroon, key=lambda x: x[1])

def get_right_support_start(components: List[Tuple[int, int, int, int, int, int]], bottom_minr_input: int) -> int:
    non_maroon = [comp for comp in components if comp[0] != 8]
    upper_comps = [comp for comp in non_maroon if comp[1] < bottom_minr_input]
    if not upper_comps:
        return 20
    rightmost_start = max(upper_comps, key=lambda x: x[3])[3]
    return rightmost_start - 2

def fill_vertical(out: List[List[int]], C: int, start_r: int, end_r: int, start_c: int, end_c: int):
    for r in range(start_r, end_r + 1):
        for c in range(start_c, end_c + 1):
            if out[r][c] == C:
                out[r][c] = 8

def fill_horizontal(out: List[List[int]], C: int, start_r: int, end_r: int, start_c: int, end_c: int):
    for r in range(start_r, end_r + 1):
        for c in range(start_c, end_c + 1):
            if out[r][c] == C:
                out[r][c] = 8

def program(g: List[List[int]]) -> List[List[int]]:
    out = shift_up(g)
    C = find_background(g)
    components = find_components(g, C)
    left_start = get_left_support_start(components)
    left_end = left_start + 1
    maroon_comp = get_maroon_comp(components)
    small_minr, _, small_maxr, small_minc, small_maxc, _ = maroon_comp
    middle_start = small_minc
    middle_end = small_maxc
    bottom_comp = get_bottom_comp(components)
    bottom_minr_input = bottom_comp[1]
    bottom_start = bottom_comp[3]
    right_start = get_right_support_start(components, bottom_minr_input)
    right_end = right_start + 1
    floor1_min = small_minr - 6
    floor1_max = small_maxr - 6
    base_r = (bottom_minr_input - 6) - 2
    is_far = floor1_max + 2 < base_r
    # vertical fills full height for all supports
    supports_list = [(left_start, left_end), (middle_start, middle_end), (right_start, right_end)]
    for s_start, s_end in supports_list:
        fill_vertical(out, C, 0, 18, s_start, s_end)
    # right support only upper to floor1_max
    fill_vertical(out, C, floor1_max + 1, 18, right_start, right_end)  # but only if not already, but since C to 8, but to not fill below, we skip filling below for right
    # wait, to not fill right below, we fill right only 0 to floor1_max
    fill_vertical(out, C, 0, floor1_max, right_start, right_end)
    # left and middle full already done
    # horizontal for floor1
    h_start = left_start
    h_end = right_end
    if is_far:
        fill_horizontal(out, C, floor1_min, floor1_max, h_start, h_end)
        # base horizontal
        supports_pos = [s[0] for s in supports_list]
        base_start_col = min(s for s in supports_pos if s >= bottom_start)
        fill_horizontal(out, C, base_r, base_r + 1, base_start_col, len(out[0]) - 1)
    else:
        fill_horizontal(out, C, floor1_max, floor1_max, h_start, h_end)
    return out
```