```python
from typing import List, Tuple
from collections import Counter

def get_bottom_half(g: List[List[int]], n: int) -> List[List[int]]:
    h = n // 2
    return [row[:] for row in g[n - h:]]

def split_left_right(bottom: List[List[int]], w: int) -> Tuple[List[List[int]], List[List[int]]]:
    h = len(bottom)
    left = [row[:w] for row in bottom]
    right = [row[w:2 * w] for row in bottom]
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
        left_row_len = len(left[i])
        for j in range(w_r):
            if filled[i][j] == 0:
                filled[i][j] = left[i][j % left_row_len]
    return filled

def get_background_color(right: List[List[int]]) -> int:
    if not right:
        return 0
    count = Counter(c for row in right for c in row if c != 0)
    return count.most_common(1)[0][0] if count else 0

def get_row_types(left: List[List[int]]) -> List[Tuple[int, ...]]:
    return [tuple(row) for row in left]

def group_types(types_list: List[Tuple[int, ...]]) -> dict[Tuple[int, ...], List[int]]:
    groups = {}
    for i, t in enumerate(types_list):
        groups.setdefault(t, []).append(i)
    return groups

def trim_trailing_full(filled: List[List[int]], c: int, w: int) -> List[List[int]]:
    h = len(filled)
    if h == 0:
        return []
    i = h - 1
    while i >= 0 and all(filled[i][j] == c for j in range(w)):
        i -= 1
    return [row[:] for row in filled[:i + 1]]

def get_max_consecutive_full(filled: List[List[int]], c: int, w: int) -> int:
    h = len(filled)
    if h == 0:
        return 0
    max_k = 0
    curr = 0
    for i in range(h):
        if all(filled[i][j] == c for j in range(w)):
            curr += 1
            max_k = max(max_k, curr)
        else:
            curr = 0
    return max_k

def parse_blocks(filled: List[List[int]], c: int, w: int) -> List[Tuple[str, int, int]]:
    h = len(filled)
    blocks = []
    i = 0
    while i < h:
        if all(filled[i][j] == c for j in range(w)):
            typ = 'full'
            start = i
            i += 1
            while i < h and all(filled[i][j] == c for j in range(w)):
                i += 1
            blocks.append((typ, start, i - start))
        else:
            typ = 'nonfull'
            start = i
            i += 1
            while i < h and not all(filled[i][j] == c for j in range(w)):
                i += 1
            blocks.append((typ, start, i - start))
    return blocks

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    w = n // 2
    h = n // 2
    bottom = get_bottom_half(g, n)
    left, right = split_left_right(bottom, w)
    if is_solid_left(left):
        c = left[0][0] if left else 0
        filled = fill_right(left, right)
        trimmed = trim_trailing_full(filled, c, w)
        h_trim = len(trimmed)
        if h_trim == 0:
            return []
        max_k = get_max_consecutive_full(trimmed, c, w)
        if max_k == 0:
            block = [row[:] for row in trimmed]
            output = block * h
            return output
        elif max_k <= 1:
            return [row[:] for row in trimmed]
        else:
            k = max_k
            new_w = w + k
            blocks = parse_blocks(trimmed, c, w)
            output = []
            prev_nonfull_extended = None
            for typ, start, blen in blocks:
                if typ == 'nonfull':
                    this_ext = []
                    for rr in range(blen):
                        row = trimmed[start + rr][:]
                        ext_row = row + row[:k]
                        this_ext.append(ext_row)
                        output.append(ext_row)
                    prev_nonfull_extended = this_ext
                else:
                    full_row = [c] * new_w
                    for _ in range(blen):
                        output.append(full_row)
                    if blen > 1 and prev_nonfull_extended is not None:
                        for ii in range(blen):
                            output.append(prev_nonfull_extended[ii])
            return output
    else:
        filled = fill_right(left, right)
        bg = get_background_color(right)
        row_types = get_row_types(left)
        groups = group_types(row_types)
        ordered_groups = []
        seen = set()
        for i in range(h):
            t = row_types[i]
            if t not in seen:
                seen.add(t)
                ordered_groups.append(groups[t])
        num_bands = len(ordered_groups)
        bands = []
        for indices in ordered_groups:
            if not indices:
                continue
            max_non = max(sum(1 for cc in filled[i] if cc != bg) for i in indices) if indices else 0
            achieving = [i for i in indices if sum(1 for cc in filled[i] if cc != bg) == max_non]
            achieving.sort()
            stack = [filled[i][:] for i in achieving]
            stack_h = len(stack)
            occ = len(indices)
            full_r = occ // stack_h if stack_h > 0 else 0
            rem = occ % stack_h
            band = stack * full_r + stack[:rem] if stack_h > 0 else []
            bands.append(band)
        if not bands:
            return []
        if bg == 0:
            output = []
            for band in bands:
                for r in band:
                    output.append(r[:])
            return output
        else:
            target_h = 2 * n
            target_w = 2 * n
            hor_rep = target_w // w
            sep_h = w // 2
            bg_row = [bg] * target_w
            if num_bands == 1:
                band = bands[0]
                band_h = len(band)
                if band_h == 0:
                    return [bg_row[:] for _ in range(target_h)]
                num_cyc = target_h // band_h
                output = []
                for _ in range(num_cyc):
                    for r in band:
                        output.append(r * hor_rep)
                return output
            else:
                occs = [len(idx_list) for idx_list in ordered_groups]
                num_cycles = min(occs) if occs else 1
                full_band_sequence = [band for _ in range(num_cycles) for band in bands]
                total_instances = len(full_band_sequence)
                if total_instances == 0:
                    return [bg_row[:] for _ in range(target_h)]
                total_band_h = sum(len(b) for b in full_band_sequence)
                num_seps = total_instances - 1
                total_sep_h = num_seps * sep_h
                fixed_h = total_band_h + total_sep_h
                pad_total = target_h - fixed_h
                top_pad = pad_total // 2
                bottom_pad = pad_total - top_pad
                output = [bg_row[:] for _ in range(top_pad)]
                for ii in range(total_instances):
                    band = full_band_sequence[ii]
                    for r in band:
                        output.append(r * hor_rep)
                    if ii < total_instances - 1:
                        output += [bg_row[:] for _ in range(sep_h)]
                output += [bg_row[:] for _ in range(bottom_pad)]
                return output
```