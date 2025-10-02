```python
from typing import List
import copy

def get_doubled_sequence(row_data: List[int], center: int) -> List[int]:
    blocks = []
    first_non4 = -1
    n_non4 = 0
    i = 0
    while i < center:
        if row_data[i] == 4:
            i += 1
            continue
        if first_non4 == -1:
            first_non4 = i
        val = row_data[i]
        j = i
        while j < center and row_data[j] == val:
            j += 1
        length = j - i
        blocks.append((val, length))
        n_non4 += length
        i = j
    if not blocks:
        return [4] * center
    shift = n_non4 // 2
    start_col = max(0, first_non4 - shift)
    new_row = [4] * center
    pos = start_col
    for val, length in blocks:
        for _ in range(2 * length):
            if pos < center:
                new_row[pos] = val
            pos += 1
    return new_row

def reflect_upper_horizontal(g: List[List[int]]):
    for r in range(13):
        for c in range(13):
            if g[r][c] != 4:
                tc = 26 - c
                if g[r][tc] == 4:
                    g[r][tc] = g[r][c]

def spread_8_up_right(g: List[List[int]]):
    to_set = []
    for r in range(1, 13):
        for c in range(14, 26):
            c2 = c + 1
            if c2 > 26:
                continue
            if g[r][c] == 8 and g[r][c2] == 8 and g[r + 1][c] == 2 and g[r + 1][c2] == 2:
                if g[r - 1][c] == 4 and g[r - 1][c2] == 4:
                    to_set.append((r - 1, c))
                    to_set.append((r - 1, c2))
    for tr, tc in to_set:
        g[tr][tc] = 8

def clear_exception_upper(g: List[List[int]]):
    for r in range(13):
        below_all4 = (r == 12) or all(g[r + 1][c] == 4 for c in range(13))
        if below_all4 and g[r][5:9] == [2, 2, 3, 3]:
            for tc in [18, 19, 20, 21]:
                g[r][tc] = 4

def process_upper(g: List[List[int]]):
    reflect_upper_horizontal(g)
    spread_8_up_right(g)
    clear_exception_upper(g)

def process_lower_no_nine(g: List[List[int]]):
    # Point reflection
    for r in range(13):
        for c in range(13):
            if g[r][c] != 4:
                tr = 26 - r
                tc = 26 - c
                if 14 <= tr < 27 and 14 <= tc < 27 and g[tr][tc] == 4:
                    g[tr][tc] = g[r][c]
    # Isolated 2 to 8 below in left
    for r in range(14, 26):
        for c in range(13):
            is_isolated = g[r][c] == 2 and (c == 0 or g[r][c - 1] != 2) and (c == 12 or g[r][c + 1] != 2)
            if is_isolated and g[r + 1][c] == 4:
                g[r + 1][c] = 8
    # Vertical upward extend 2's in right half (iterative)
    changed = True
    while changed:
        changed = False
        for r in range(15, 27):
            for c in range(14, 27):
                if g[r][c] == 2 and g[r - 1][c] == 4:
                    g[r - 1][c] = 2
                    changed = True
    # Horizontal extend 3's for 2 blocks
    for r in range(14, 27):
        # Left half extend right
        i = 0
        while i < 13:
            if g[r][i] != 2:
                i += 1
                continue
            j = i
            while j < 13 and g[r][j] == 2:
                j += 1
            L = j - i
            for kk in range(1, L + 1):
                cc = j + kk - 1
                if cc >= 13:
                    break
                if g[r][cc] == 4:
                    g[r][cc] = 3
                elif g[r][cc] != 3:
                    break
            i = j
        # Right half extend left
        i = 26
        while i >= 14:
            if g[r][i] != 2:
                i -= 1
                continue
            j = i
            while j >= 14 and g[r][j] == 2:
                j -= 1
            start_block = j + 1
            L = i - start_block + 1
            for kk in range(1, L + 1):
                cc = start_block - kk
                if cc < 14:
                    break
                if g[r][cc] == 4:
                    g[r][cc] = 3
                elif g[r][cc] != 3:
                    break
            i = start_block - 1
    # 8 left extend by 1 in right
    for r in range(14, 27):
        i = 14
        while i < 26:
            if g[r][i] != 8:
                i += 1
                continue
            j = i
            while j < 27 and g[r][j] == 8:
                j += 1
            if i > 14 and g[r][i - 1] == 4:
                g[r][i - 1] = 8
            i = j
    # Spread down 8's in right single layer
    to_set = []
    for r in range(14, 26):
        for c in range(14, 27):
            if g[r][c] == 8 and g[r + 1][c] == 4:
                to_set.append((r + 1, c))
    for tr, tc in to_set:
        g[tr][tc] = 8

def process_lower_has_nine(g: List[List[int]]):
    # Clear lower
    for r in range(14, 27):
        for c in range(27):
            g[r][c] = 1 if c == 13 else 4
    # Collect uniques
    seen = set()
    uniques = []
    num_non4_rows = 0
    for r in range(13):
        row_data = g[r][:13]
        t = tuple(row_data)
        has_non4 = any(v != 4 for v in row_data)
        if has_non4:
            num_non4_rows += 1
        if has_non4 and t not in seen:
            non4_pos = [i for i in range(13) if row_data[i] != 4]
            min_c = min(non4_pos)
            max_c = max(non4_pos)
            seq = [row_data[i] for i in range(min_c, max_c + 1)]
            rev_seq = seq[::-1]
            uniques.append((row_data, min_c, max_c, rev_seq, max_c - min_c + 1))
            seen.add(t)
    num_uniques = len(uniques)
    placement_start_row = 27 - 2 * num_non4_rows
    current_row = 26
    last_pattern = None
    for k in range(num_uniques):
        orig_data, min_c, max_c, rev_seq, length = uniques[k]
        pattern_doubled = get_doubled_sequence(orig_data, 13)
        num = 1 << k
        for j in range(num):
            placed_r = current_row
            # Set left
            for cc in range(13):
                g[placed_r][cc] = pattern_doubled[cc]
            # Set right reflection
            if j == 0 and k >= 2:
                # Bottom: full prev
                prev_k = k - 1
                _, _, prev_max_c, prev_rev_seq, prev_length = uniques[prev_k]
                start_r = 26 - prev_max_c - 1
                for ii in range(prev_length):
                    tc = start_r + ii
                    if 14 <= tc < 27 and g[placed_r][tc] == 4:
                        g[placed_r][tc] = prev_rev_seq[ii]
            elif j > 0:
                if k >= 2:
                    # Non-bottom: full own
                    start_r = 26 - max_c - 1
                    for ii in range(length):
                        tc = start_r + ii
                        if 14 <= tc < 27 and g[placed_r][tc] == 4:
                            g[placed_r][tc] = rev_seq[ii]
                elif k == 1:
                    # Non-bottom: partial own
                    partial_len = 1 << (k - 1)
                    start_r = 26 - max_c - 1
                    for ii in range(partial_len):
                        tc = start_r + ii
                        if 14 <= tc < 27 and g[placed_r][tc] == 4:
                            g[placed_r][tc] = rev_seq[ii]
            current_row -= 1
            last_pattern = pattern_doubled
    # Extra rows
    while current_row >= placement_start_row:
        placed_r = current_row
        for cc in range(13):
            g[placed_r][cc] = last_pattern[cc]
        # No right reflection
        current_row -= 1

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    process_upper(out)
    has_nine = any(9 in row for row in out)
    if has_nine:
        process_lower_has_nine(out)
    else:
        process_lower_no_nine(out)
    # Ensure central cross
    for r in range(27):
        out[r][13] = 1
    for c in range(27):
        out[13][c] = 1
    return out
```