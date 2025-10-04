```python
from typing import List

def get_row_colors(g: List[List[int]]) -> List[int]:
    return [row[0] for row in g]

def get_blocks(row_colors: List[int]) -> List[tuple]:
    blocks = []
    i = 0
    n = len(row_colors)
    while i < n:
        c = row_colors[i]
        j = i + 1
        while j < n and row_colors[j] == c:
            j += 1
        h = j - i
        blocks.append((h, c))
        i = j
    return blocks

def add_border(inner: List[int], border_w: int, border_c: int) -> List[int]:
    if border_w > 0:
        return [border_c] * border_w + inner + [border_c] * border_w
    return inner

def flatten_segments(segments: List[tuple]) -> List[int]:
    flat = []
    for ww, cc, _ in segments:
        flat += [cc] * ww
    return flat

def program(g: List[List[int]]) -> List[List[int]]:
    row_colors = get_row_colors(g)
    rows = len(row_colors)
    cols = len(g[0])
    blocks = get_blocks(row_colors)
    has_border = len(blocks) > 0 and blocks[0][0] == 2 and blocks[0][1] == 8
    if has_border:
        border_w = 2
        border_c = 8
        eff_cols = cols - 3
        total_w = 2 * eff_cols + 2 * border_w
        inner_w = total_w - 2 * border_w
        inner_row_colors = row_colors[2:]
        inner_blocks = blocks[1:]
    else:
        border_w = 0
        border_c = 0
        eff_cols = cols
        total_w = 2 * eff_cols
        inner_w = total_w
        inner_row_colors = row_colors
        inner_blocks = blocks
    pivot_b = next((b for b in range(len(inner_blocks)) if inner_blocks[b][0] == 1), len(inner_blocks) - 1)
    upper = []
    if has_border:
        for _ in range(border_w):
            upper.append([border_c] * total_w)
    current_sum_h = 0
    for b in range(pivot_b + 1):
        h, c = inner_blocks[b]
        w = current_sum_h
        flank = []
        for pb in range(b):
            ph, pc = inner_blocks[pb]
            flank += [pc] * ph
        is_pivot = (b == pivot_b)
        extra = 0
        if has_border and is_pivot:
            extra = 1
            last_pc = flank[-1] if flank else c
            flank += [last_pc]
        w += extra
        right_flank = list(reversed(flank))
        center_len = 2 * (eff_cols - w)
        center = [c] * center_len
        inner_row = flank + center + right_flank
        for _ in range(h):
            row = add_border(inner_row, border_w, border_c)
            upper.append(row)
        current_sum_h += h
    w_pivot = sum(inner_blocks[k][0] for k in range(pivot_b))
    delta = 1 if has_border else 0
    pivot_center_len = 2 * (eff_cols - w_pivot - delta)
    pivot_h, pivot_c = inner_blocks[pivot_b]
    side_width = pivot_h
    sub_available = pivot_center_len - 2 * side_width
    outer_flank = []
    temp_w = 0
    for pb in range(pivot_b):
        ph, pc = inner_blocks[pb]
        outer_flank += [pc] * ph
        temp_w += ph
    if has_border:
        outer_flank += [outer_flank[-1]]
        temp_w += 1
    right_outer_flank = list(reversed(outer_flank))
    sub_blocks = inner_blocks[pivot_b + 1:]
    sub_configs = []
    side = []
    if sub_blocks:
        h1, c1 = sub_blocks[0]
        sub_row = [c1] * sub_available
        sub_configs.append(sub_row)
        for _ in range(h1):
            inner = outer_flank + [pivot_c] * side_width + sub_row + [pivot_c] * side_width + right_outer_flank
            row = add_border(inner, border_w, border_c)
            side.append(row)
        current_segments = [(sub_available, c1, h1)]
        for sb in range(1, len(sub_blocks)):
            h_new, c_new = sub_blocks[sb]
            num_seg = len(current_segments)
            center_idx = num_seg // 2
            old_width, old_c, old_h = current_segments[center_idx]
            new_width = old_width - 2 * old_h
            if new_width <= 0:
                new_width = 2
            flank_w = (old_width - new_width) // 2
            if flank_w < 0:
                flank_w = 0
                new_width = old_width
            left_flank = (flank_w, old_c, old_h)
            new_seg = (new_width, c_new, h_new)
            right_flank = (flank_w, old_c, old_h)
            current_segments[center_idx:center_idx + 1] = [left_flank, new_seg, right_flank]
            sub_row = flatten_segments(current_segments)
            sub_configs.append(sub_row)
            for _ in range(h_new):
                inner = outer_flank + [pivot_c] * side_width + sub_row + [pivot_c] * side_width + right_outer_flank
                row = add_border(inner, border_w, border_c)
                side.append(row)
        if has_border:
            mirror_sub_blocks = list(reversed(sub_blocks))
        else:
            mirror_sub_blocks = list(reversed(sub_blocks[:-1])) if sub_blocks else []
        for mb in range(len(mirror_sub_blocks) - 1, -1, -1):
            h_m, _ = mirror_sub_blocks[mb]
            sub_row = sub_configs[mb]
            for _ in range(h_m):
                inner = outer_flank + [pivot_c] * side_width + sub_row + [pivot_c] * side_width + right_outer_flank
                row = add_border(inner, border_w, border_c)
                side.append(row)
    upper_mirror = upper[::-1]
    output = upper + side + upper_mirror
    return output
```