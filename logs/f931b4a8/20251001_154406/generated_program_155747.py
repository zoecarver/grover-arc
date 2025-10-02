```python
from typing import List, Tuple
from collections import Counter

def get_n(g: List[List[int]]) -> int:
    return len(g)

def get_bottom_half(g: List[List[int]], n: int) -> List[List[int]]:
    h = n // 2
    return [row[:] for row in g[n - h:]]

def split_left_right(bottom: List[List[int]], w: int) -> Tuple[List[List[int]], List[List[int]]]:
    h = len(bottom)
    left = [row[:w] for row in bottom]
    right = [row[w:w + w] for row in bottom]
    return left, right

def is_solid_left(left: List[List[int]]) -> bool:
    if not left or not left[0]:
        return False
    c = left[0][0]
    if c == 0:
        return False
    for row in left:
        for cell in row:
            if cell != c:
                return False
    return True

def has_color_in_right(c: int, right: List[List[int]]) -> bool:
    return any(c in row for row in right)

def fill_right(left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
    h = len(left)
    if h == 0:
        return []
    w_r = len(right[0])
    filled = [row[:] for row in right]
    for i in range(h):
        for j in range(w_r):
            if filled[i][j] == 0:
                filled[i][j] = left[i][j % len(left[i])]
    return filled

def trim_trailing_full(filled: List[List[int]], c: int) -> List[List[int]]:
    h = len(filled)
    k = 0
    for i in range(h - 1, -1, -1):
        if all(x == c for x in filled[i]):
            k += 1
        else:
            break
    return filled[:h - k]

def has_any_full_row(filled: List[List[int]], c: int) -> bool:
    return any(all(x == c for x in row) for row in filled)

def get_max_consecutive_full_block(filled: List[List[int]], c: int) -> int:
    max_k = 0
    curr = 0
    for row in filled:
        if all(x == c for x in row):
            curr += 1
            max_k = max(max_k, curr)
        else:
            curr = 0
    return max_k

def extend_wrap(filled: List[List[int]], k: int) -> List[List[int]]:
    h = len(filled)
    for i in range(h):
        filled[i] = filled[i] + filled[i][:k]
    for i in range(k):
        filled.append(filled[i][:])
    return filled

def get_background_color(right: List[List[int]]) -> int:
    count = Counter(c for row in right for c in row if c != 0)
    return count.most_common(1)[0][0] if count else 0

def get_row_types(left: List[List[int]]) -> List[Tuple[int, ...]]:
    return [tuple(row) for row in left]

def group_types(types_list: List[Tuple[int, ...]]) -> dict[Tuple[int, ...], List[int]]:
    groups = {}
    for i, t in enumerate(types_list):
        groups.setdefault(t, []).append(i)
    return groups

def get_representative_filled(filled: List[List[int]], indices: List[int], bg: int) -> List[int]:
    if not indices:
        return []
    best_row = None
    max_non_bg = -1
    for i in indices:
        row = filled[i]
        non_bg_count = sum(1 for c in row if c != bg)
        if non_bg_count > max_non_bg:
            max_non_bg = non_bg_count
            best_row = row[:]
    return best_row if best_row is not None else filled[indices[0]][:]

def get_ordered_types(types_list: List[Tuple[int, ...]], groups: dict) -> List[Tuple[int, ...]]:
    first_appear = {}
    for i, t in enumerate(types_list):
        if t not in first_appear:
            first_appear[t] = i
    return sorted(first_appear, key=first_appear.get)

def build_bands(left: List[List[int]], filled_right: List[List[int]], groups: dict, ordered_types: List[Tuple[int, ...]], bg: int) -> List[List[List[int]]]:
    bands = []
    for t in ordered_types:
        indices = groups[t]
        count = len(indices)
        rep_row = get_representative_filled(filled_right, indices, bg)
        band = [rep_row[:] for _ in range(count)]
        bands.append(band)
    return bands

def build_output_non_solid(bands: List[List[List[int]]], bg: int, n: int, w: int, h: int) -> List[List[int]]:
    if bg == 0:
        output = []
        for band in bands:
            output.extend(band)
        return output
    target_w = 2 * n
    hor_repeat = target_w // w
    sep_h = w // 2
    num_bands = len(bands)
    fixed_h = h + max(0, num_bands - 1) * sep_h
    pad_total = n - fixed_h
    pad_top = pad_total // 2
    pad_bottom = pad_total - pad_top
    bg_row = [bg] * target_w
    block = []
    for _ in range(pad_top):
        block.append(bg_row[:])
    for i, band in enumerate(bands):
        for row in band:
            ext_row = row * hor_repeat
            block.append(ext_row)
        if i < num_bands - 1:
            for _ in range(sep_h):
                block.append(bg_row[:])
    for _ in range(pad_bottom):
        block.append(bg_row[:])
    return block * 2

def program(g: List[List[int]]) -> List[List[int]]:
    n = get_n(g)
    bottom = get_bottom_half(g, n)
    w = n // 2
    h = len(bottom)
    left, right = split_left_right(bottom, w)
    if not left:
        return []
    c = left[0][0]
    is_solid = is_solid_left(left)
    has_c_in_right = has_color_in_right(c, right)
    if is_solid and not has_c_in_right:
        filled_right = fill_right(left, right)
        trimmed = trim_trailing_full(filled_right, c)
        h_prime = len(trimmed)
        has_full = has_any_full_row(trimmed, c)
        if not has_full:
            output = trimmed * w
        else:
            max_k = get_max_consecutive_full_block(trimmed, c)
            if max_k > 1:
                k = max_k
                trimmed = extend_wrap(trimmed, k)
            output = trimmed
        return output
    else:
        filled_right = fill_right(left, right)
        bg = get_background_color(right)
        types_list = get_row_types(left)
        groups = group_types(types_list)
        ordered_types = get_ordered_types(types_list, groups)
        bands = build_bands(left, filled_right, groups, ordered_types, bg)
        output = build_output_non_solid(bands, bg, n, w, h)
        return output
```