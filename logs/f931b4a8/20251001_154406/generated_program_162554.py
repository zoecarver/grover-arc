```python
from typing import List, Tuple, Dict
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

def fill_right(left: List[List[int]], right: List[List[int]]) -> List[List[int]]:
    h = len(left)
    if h == 0:
        return []
    w_r = len(right[0]) if right and right[0] else 0
    filled = [row[:] for row in right]
    for i in range(h):
        for j in range(w_r):
            if filled[i][j] == 0:
                filled[i][j] = left[i][j % len(left[i])]
    return filled

def has_color_in_right(right: List[List[int]], c: int) -> bool:
    for row in right:
        if c in row:
            return True
    return False

def trim_trailing_full_c(filled: List[List[int]], c: int, w: int) -> List[List[int]]:
    trimmed = [row[:] for row in filled]
    while trimmed and all(cell == c for cell in trimmed[-1]):
        trimmed.pop()
    return trimmed

def is_uniform_row(row: List[int]) -> bool:
    if not row:
        return True
    col = row[0]
    return all(cell == col for cell in row)

def get_background_color(right: List[List[int]]) -> int:
    count = Counter(c for row in right for c in row if c != 0)
    return count.most_common(1)[0][0] if count else 0

def get_row_types(left: List[List[int]]) -> List[Tuple[int, ...]]:
    return [tuple(row) for row in left]

def group_types(types_list: List[Tuple[int, ...]]) -> Dict[Tuple[int, ...], List[int]]:
    groups = {}
    for i, t in enumerate(types_list):
        groups.setdefault(t, []).append(i)
    return groups

def get_representative_filled(filled: List[List[int]], indices: List[int], bg: int) -> List[int]:
    if not indices:
        return []
    max_non_bg = -1
    best_row = None
    for i in indices:
        row = filled[i]
        non_bg_count = sum(1 for c in row if c != bg)
        if non_bg_count > max_non_bg:
            max_non_bg = non_bg_count
            best_row = row[:]
    return best_row if best_row is not None else filled[indices[0]][:]

def handle_pure_solid(filled: List[List[int]], n: int, w: int, c: int) -> List[List[int]]:
    trimmed = trim_trailing_full_c(filled, c, w)
    if all(is_uniform_row(row) for row in trimmed):
        return [row[:] for row in trimmed]
    patterned_blocks = []
    i = 0
    h_trim = len(trimmed)
    while i < h_trim:
        if not is_uniform_row(trimmed[i]):
            start = i
            i += 1
            while i < h_trim and not is_uniform_row(trimmed[i]):
                i += 1
            patterned_blocks.append(trimmed[start:i])
        else:
            i += 1
    if len(patterned_blocks) == 1:
        block = [row[:] for row in trimmed]
        output = block * (n // 2)
        return output
    k = w // 4
    total_uniform_h = h_trim - sum(len(pb) for pb in patterned_blocks)
    output = []
    i = 0
    while i < h_trim:
        if not is_uniform_row(trimmed[i]):
            start = i
            i += 1
            while i < h_trim and not is_uniform_row(trimmed[i]):
                i += 1
            pb = trimmed[start:i]
            extended_pb = [r[:] + r[:k] for r in pb]
            output.extend(extended_pb)
        else:
            start = i
            col = trimmed[i][0]
            i += 1
            while i < h_trim and is_uniform_row(trimmed[i]) and trimmed[i][0] == col:
                i += 1
            height = i - start
            extended_ub = [[col] * (w + k) for _ in range(height)]
            output.extend(extended_ub)
    if total_uniform_h > 0 and len(patterned_blocks) > 1:
        first_pb = patterned_blocks[0]
        extended_first = [r[:] + r[:k] for r in first_pb]
        partial = extended_first[:total_uniform_h]
        output.extend(partial)
    return output

def handle_contaminated_solid(trimmed: List[List[int]], w: int) -> List[List[int]]:
    k = w // 4
    return [row[:] + row[:k] for row in trimmed]

def handle_non_solid(left: List[List[int]], filled: List[List[int]], right: List[List[int]], n: int, w: int, h: int) -> List[List[int]]:
    bg = get_background_color(right)
    types_list = get_row_types(left)
    groups = group_types(types_list)
    first_appear_order = []
    seen = set()
    for t in types_list:
        if t not in seen:
            seen.add(t)
            first_appear_order.append(t)
    if not first_appear_order:
        return []
    occ = len(groups[first_appear_order[0]])
    min_occ = min(len(groups[t]) for t in first_appear_order)
    cycles = min_occ if bg > 0 else 1
    band_height = occ  # assume uniform occ
    sep_h = w // 2 if bg > 0 else 0
    target_h = 2 * n if bg > 0 else h
    target_w = 2 * n if bg > 0 else w
    hor_rep = target_w // w
    rep_rows = {}
    for t in first_appear_order:
        indices = groups[t]
        rep = get_representative_filled(filled, indices, bg)
        rep_rows[t] = rep
    bands = []
    for _ in range(cycles):
        for t in first_appear_order:
            rep = rep_rows[t]
            band = [rep * hor_rep for _ in range(band_height)]
            bands.append(band)
    content = []
    for i in range(len(bands)):
        content.extend(bands[i])
        if i < len(bands) - 1 and bg > 0:
            sep = [[bg] * target_w for _ in range(sep_h)]
            content.extend(sep)
    fixed_h = len(content)
    pad_total = target_h - fixed_h
    pad_top = pad_total // 2
    pad_bottom = pad_total - pad_top
    pad_row = [bg] * target_w if bg > 0 else []
    for _ in range(pad_top):
        content.insert(0, pad_row[:])
    for _ in range(pad_bottom):
        content.append(pad_row[:])
    return content

def program(g: List[List[int]]) -> List[List[int]]:
    n = get_n(g)
    h = n // 2
    w = n // 2
    bottom = get_bottom_half(g, n)
    left, right = split_left_right(bottom, w)
    filled = fill_right(left, right)
    if is_solid_left(left):
        c = left[0][0] if left else 0
        has_c_in_right = has_color_in_right(right, c)
        trimmed = trim_trailing_full_c(filled, c, w)
        if not has_c_in_right:
            return handle_pure_solid(filled, n, w, c)
        else:
            return handle_contaminated_solid(trimmed, w)
    else:
        return handle_non_solid(left, filled, right, n, w, h)
```