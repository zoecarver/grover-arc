```python
from typing import List
from collections import Counter

def get_bottom_half(g: List[List[int]], n: int) -> List[List[int]]:
    h = n // 2
    return [row[:] for row in g[n - h: n]]

def split_left_right(bottom: List[List[int]], w: int) -> tuple[List[List[int]], List[List[int]]]:
    h = len(bottom)
    left = [row[:w] for row in bottom]
    right = [row[w : w + w] for row in bottom]
    return left, right

def is_solid_left(left: List[List[int]]) -> bool:
    if not left or not left[0]:
        return False
    color = left[0][0]
    for row in left:
        for c in row:
            if c != color:
                return False
    return True

def fill_right(left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
    h = len(left)
    if h == 0:
        return []
    w_r = len(right[0])
    filled = [row[:] for row in right]
    for i in range(h):
        for j in range(w_r):
            if filled[i][j] == 0:
                filled[i][j] = left[i][j]
    return filled

def trim_trailing_full(filled: List[List[int]], fill_color: int) -> List[List[int]]:
    trimmed = [row[:] for row in filled]
    while trimmed and all(c == fill_color for c in trimmed[-1]):
        trimmed.pop()
    return trimmed

def handle_solid(left: List[List[int]], right: List[List[int]], n: int, w: int) -> List[List[int]]:
    fill_color = left[0][0]
    filled = fill_right(left, right)
    trimmed = trim_trailing_full(filled, fill_color)
    has_full = any(all(c == fill_color for c in row) for row in trimmed)
    if not has_full:
        return trimmed * w
    else:
        return trimmed

def get_background_color(right: List[List[int]]) -> int:
    count = Counter(c for row in right for c in row if c != 0)
    if not count:
        return 0
    return count.most_common(1)[0][0]

def get_row_types(left: List[List[int]]) -> List[tuple]:
    return [tuple(row) for row in left]

def group_types(types_list: List[tuple]) -> dict[tuple, List[int]]:
    groups = {}
    for i, t in enumerate(types_list):
        groups.setdefault(t, []).append(i)
    return groups

def get_representative_filled(filled: List[List[int]], indices: List[int], bg: int) -> List[int]:
    best_row = None
    max_non_bg = -1
    for i in indices:
        row = filled[i]
        non_bg_count = sum(1 for c in row if c != bg)
        if non_bg_count > max_non_bg:
            max_non_bg = non_bg_count
            best_row = row[:]
    if best_row is None and indices:
        best_row = filled[indices[0]][:]
    return best_row if best_row is not None else []

def handle_non_solid(left: List[List[int]], right: List[List[int]], n: int, w: int) -> List[List[int]]:
    bg = get_background_color(right)
    filled = fill_right(left, right)
    types_list = get_row_types(left)
    groups = group_types(types_list)
    bands = []
    h = len(left)
    for k in range(h):
        t = types_list[k]
        indices = groups.get(t, [])
        count = len(indices)
        rep = get_representative_filled(filled, indices, bg)
        band = [rep[:] for _ in range(count)]
        bands.append(band)
    if bg == 0:
        output = []
        for band in bands:
            output.extend(band)
        return output
    else:
        target_h = n * 2
        target_w = n * 2
        hor_repeat = target_w // w
        sep_h = w // 2
        all_bg_row = [bg] * target_w
        output = []
        num_bands = len(bands)
        total_fixed = sum(len(band) for band in bands) + max(0, num_bands - 1) * sep_h
        remaining = target_h - total_fixed
        pad_start = remaining // 2
        pad_end = remaining - pad_start
        output.extend([all_bg_row[:] for _ in range(pad_start)])
        for bi, band in enumerate(bands):
            extended_band = []
            for r in band:
                long_r = r * hor_repeat
                extended_band.append(long_r)
            output.extend(extended_band)
            if bi < num_bands - 1:
                output.extend([all_bg_row[:] for _ in range(sep_h)])
        output.extend([all_bg_row[:] for _ in range(pad_end)])
        return output

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    n = len(g)
    w = n // 2
    h = n // 2
    bottom = [row[:] for row in g[n - h:]]
    left = [row[:w] for row in bottom]
    right_ = [row[w : w + w] for row in bottom]
    if is_solid_left(left):
        return handle_solid(left, right_, n, w)
    else:
        return handle_non_solid(left, right_, n, w)
```