```python
from typing import List, Tuple
from collections import Counter

def get_bottom_half(g: List[List[int]], n: int) -> List[List[int]]:
    h = n // 2
    return [row[:] for row in g[n - h: n]]

def split_left_right(bottom: List[List[int]], w: int) -> Tuple[List[List[int]], List[List[int]]]:
    h = len(bottom)
    left = [row[:w] for row in bottom]
    right = [row[w : w + w] for row in bottom]
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
    w_r = len(right[0])
    filled = [row[:] for row in right]
    for i in range(h):
        for j in range(w_r):
            if filled[i][j] == 0:
                filled[i][j] = left[i][j % len(left[i])]
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
    max_non_bg = -1
    best_row = None
    for i in indices:
        row = filled[i]
        non_bg_count = sum(1 for c in row if c != bg)
        if non_bg_count > max_non_bg:
            max_non_bg = non_bg_count
            best_row = row[:]
    return best_row if best_row is not None else filled[indices[0]][:]

def trim_trailing_full(filled: List[List[int]], c: int, w: int) -> List[List[int]]:
    h = len(filled)
    i = h - 1
    while i >= 0 and all(filled[i][j] == c for j in range(w)):
        i -= 1
    return [row[:] for row in filled[:i + 1]]

def has_full_c_row(filled: List[List[int]], c: int, w: int) -> bool:
    for row in filled:
        if all(cell == c for cell in row):
            return True
    return False

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    w = n // 2
    h = n // 2
    bottom = get_bottom_half(g, n)
    left, right = split_left_right(bottom, w)
    filled = fill_right(left, right)
    if is_solid_left(left):
        c = left[0][0] if left and left[0] else 0
        trimmed = trim_trailing_full(filled, c, w)
        if len(trimmed) == 0:
            return []
        if not has_full_c_row(trimmed, c, w):
            num_rep = 2 * n // len(trimmed)
            out = []
            for _ in range(num_rep):
                out.extend([row[:] for row in trimmed])
            return out
        else:
            remaining_h = len(trimmed)
            blocks = []
            i = 0
            while i < remaining_h:
                row = trimmed[i]
                if all(cell == c for cell in row):
                    start = i
                    while i < remaining_h and all(trimmed[i][j] == c for j in range(w)):
                        i += 1
                    ht = i - start
                    rep_row = [c] * w
                    blocks.append(('full_c', ht, rep_row))
                else:
                    start = i
                    block_rows = []
                    is_m = False
                    while i < remaining_h and not all(trimmed[i][j] == c for j in range(w)):
                        r = trimmed[i]
                        if len(set(r)) > 1:
                            is_m = True
                        block_rows.append(r)
                        i += 1
                    ht = len(block_rows)
                    if is_m:
                        k = w // 4
                        ext_rows = [r + r[:k] for r in block_rows]
                        blocks.append(('mixed', ht, ext_rows))
                    else:
                        blocks.append(('full_other', ht, block_rows))
            has_m = any(b[0] == 'mixed' for b in blocks)
            k = w // 4 if has_m else 0
            extra = []
            if has_m:
                for b in blocks:
                    if b[0] == 'mixed':
                        extra = [r[:] for r in b[2][:k]]
                        break
            out = []
            for btype, ht, cont in blocks:
                if btype == 'full_c':
                    rep = cont[0] + [c] * k if k > 0 else cont[0]
                    for _ in range(ht):
                        out.append(rep[:])
                elif btype == 'mixed':
                    out.extend([r[:] for r in cont])
                elif btype == 'full_other':
                    out.extend([r[:] for r in cont])
            out.extend(extra)
            return out
    else:
        bg = get_background_color(right)
        row_types = get_row_types(left)
        groups = group_types(row_types)
        if not groups:
            return filled
        ordered_types = sorted(groups, key=lambda t: min(groups[t]))
        reps = {}
        occs = {}
        for t in ordered_types:
            indices = groups[t]
            occs[t] = len(indices)
            reps[t] = get_representative_filled(filled, indices, bg)
        min_occ = min(occs.values()) if occs else 0
        num_cycles = min_occ if bg > 0 else 1
        sep_h = w // 2 if bg > 0 else 0
        out = []
        for cyc in range(num_cycles):
            for gi, t in enumerate(ordered_types):
                rep = reps[t]
                occ = occs[t]
                for _ in range(occ):
                    out.append(rep[:])
                if not (cyc == num_cycles - 1 and gi == len(ordered_types) - 1):
                    bg_row = [bg] * w
                    for _ in range(sep_h):
                        out.append(bg_row[:])
        if bg > 0:
            fixed_h = len(out)
            target_h = 2 * n
            remain = target_h - fixed_h
            top_p = remain // 2
            bottom_p = remain - top_p
            bg_row = [bg] * w
            pad_top = [bg_row[:] for _ in range(top_p)]
            pad_bottom = [bg_row[:] for _ in range(bottom_p)]
            out = pad_top + out + pad_bottom
            rep_num = 2 * n // w
            final_out = [row * rep_num for row in out]
            return final_out
        else:
            return out
```