```python
from typing import List, Tuple
from collections import Counter, defaultdict

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

def get_rep(filled: List[List[int]], indices: List[int], bg: int) -> List[int]:
    if not indices:
        return []
    max_non = -1
    best_row = None
    best_idx = float('inf')
    for idx in indices:
        row = filled[idx]
        non = sum(1 for c in row if c != bg)
        if non > max_non or (non == max_non and idx < best_idx):
            max_non = non
            best_row = row[:]
            best_idx = idx
    return best_row

def trim_trailing_full(filled: List[List[int]], c: int, w: int) -> List[List[int]]:
    h = len(filled)
    i = h - 1
    while i >= 0:
        if all(filled[i][j] == c for j in range(w)):
            i -= 1
        else:
            break
    return [row[:] for row in filled[:i + 1]]

def get_max_consecutive_full(filled: List[List[int]], c: int, w: int) -> int:
    max_k = 0
    curr = 0
    for row in filled:
        if all(cell == c for cell in row):
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
            start = i
            i += 1
            while i < h and all(filled[i][j] == c for j in range(w)):
                i += 1
            blocks.append(('full', start, i - start))
        else:
            start = i
            i += 1
            while i < h and not all(filled[i][j] == c for j in range(w)):
                i += 1
            blocks.append(('nonfull', start, i - start))
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
        trimmed_filled = trim_trailing_full(filled, c, w)
        k_max = get_max_consecutive_full(trimmed_filled, c, w)
        if k_max == 0:
            return [row[:] for row in trimmed_filled * (n // 2)]
        else:
            blocks = parse_blocks(trimmed_filled, c, w)
            extend = k_max > 1
            ext_w = w + (k_max if extend else 0)
            out = []
            first_nonfull_rows = None
            for typ, start, bh in blocks:
                if typ == 'nonfull':
                    block_rows = [trimmed_filled[start + j][:] for j in range(bh)]
                    if first_nonfull_rows is None:
                        first_nonfull_rows = [r[:] for r in block_rows]
                    for r in block_rows:
                        if extend:
                            out.append(r + r[:k_max])
                        else:
                            out.append(r)
                else:
                    full_r = [c] * ext_w
                    for _ in range(bh):
                        out.append(full_r)
            if k_max > 1 and first_nonfull_rows is not None:
                for j in range(k_max):
                    if j < len(first_nonfull_rows):
                        r = first_nonfull_rows[j][:]
                        if extend:
                            out.append(r + r[:k_max])
                        else:
                            out.append(r)
            return out
    else:
        types_list = get_row_types(left)
        groups = defaultdict(list)
        for i, t in enumerate(types_list):
            groups[t].append(i)
        first_appear = {t: min(groups[t]) for t in groups}
        ordered_types = sorted(groups, key=lambda t: first_appear[t])
        filled = fill_right(left, right)
        bg = get_background_color(right)
        stacked = []
        for ii, t in enumerate(ordered_types):
            indices = groups[t]
            rep = get_rep(filled, indices, bg)
            count = len(indices)
            for _ in range(count):
                stacked.append(rep[:])
            if ii < len(ordered_types) - 1 and bg != 0:
                sep_h = w // 2
                full_bg = [bg] * w
                for _ in range(sep_h):
                    stacked.append(full_bg)
        if bg == 0:
            return [row[:] for row in stacked]
        else:
            total_fixed = len(stacked)
            pad_total = n - total_fixed
            top_pad = pad_total // 2
            bottom_pad = pad_total - top_pad
            full_bg = [bg] * w
            block = [full_bg[:] for _ in range(top_pad)] + [row[:] for row in stacked] + [full_bg[:] for _ in range(bottom_pad)]
            hor_rep_num = 2 * n // w
            wide_block = [row * hor_rep_num for row in block]
            return [row[:] for row in wide_block * 2]
```