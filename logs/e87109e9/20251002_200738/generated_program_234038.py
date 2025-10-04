```python
from typing import List, Tuple
from collections import Counter

def find_background(grid: List[List[int]]) -> int:
    count = Counter()
    for row in grid:
        for cell in row:
            if cell not in [0, 5, 8]:
                count[cell] += 1
    return count.most_common(1)[0][0] if count else 3

def get_group_info(clue_row: List[int], group_start: int) -> Tuple[int, int]:
    for p in range(4):
        val = clue_row[group_start + p]
        if val not in [0, 5]:
            return val, p
    return 0, -1

def get_clue_color(clue_row: List[int], group_start: int) -> int:
    return get_group_info(clue_row, group_start)[0]

def get_has_prop_rows(grid: List[List[int]]) -> List[int]:
    has_prop = []
    for i in range(19):
        if any(cell == 8 for cell in grid[6 + i]):
            has_prop.append(i)
    return has_prop

def compute_upper_pairs_with_skip(clue: List[int]) -> List[Tuple[int, int]]:
    group_starts = [1, 7, 13, 19]
    pairs = []
    skip_next = False
    for gi in range(4):
        if skip_next:
            skip_next = False
            continue
        start = group_starts[gi]
        color, pos = get_group_info(clue, start)
        if color == 0 or color == 3:
            continue
        activate = False
        pair_start = -1
        if pos == 0:
            if color in [4, 6]:
                activate = True
                if color == 6:
                    pair_start = start + 1
                elif color == 4:
                    next_c = 0
                    if gi < 3:
                        next_c = get_clue_color(clue, group_starts[gi + 1])
                    if next_c == 2:
                        pair_start = start + 3
                        skip_next = True
                    else:
                        pair_start = start + 1
        elif pos == 3:
            if color in [2, 4, 6]:
                activate = True
                if color == 2:
                    pair_start = start + 3
                    if start == 19:
                        pair_start = 18
                elif color == 4:
                    pair_start = start + 2
                    skip_next = True
                elif color == 6:
                    pair_start = start + 1
        if activate and pair_start != -1 and pair_start + 1 < 24:
            pairs.append((pair_start, pair_start + 1))
    return pairs

def compute_lower_pairs(clue: List[int]) -> List[Tuple[int, int]]:
    start = 1
    color, pos = get_group_info(clue, start)
    if color == 0 or color == 3:
        return []
    activate = False
    pair_start = -1
    if pos == 0 and color == 1:
        activate = True
        pair_start = start + 3
    elif pos == 3 and color == 4:
        activate = True
        pair_start = start + 2
    if activate and pair_start + 1 < 24:
        return [(pair_start, pair_start + 1)]
    return []

def program(g: List[List[int]]) -> List[List[int]]:
    if len(g) != 25 or len(g[0]) != 24:
        return []
    output = [row[:] for row in g[6:25]]
    bkg = find_background(output)
    for row in output:
        for j in range(24):
            if row[j] == 5:
                row[j] = bkg
    clue = g[1]
    has_prop = get_has_prop_rows(g)
    max_prop_i = max(has_prop) if has_prop else -1
    upper_pairs = compute_upper_pairs_with_skip(clue)
    for i in range(max_prop_i + 1 if max_prop_i >= 0 else 0):
        row = output[i]
        for ps, pe in upper_pairs:
            if all(row[k] == bkg for k in range(ps, pe + 1)):
                for k in range(ps, pe + 1):
                    row[k] = 8
    first_color, first_pos = get_group_info(clue, 1)
    lower_pair_for_special = None
    if first_color == 1 and first_pos == 0:
        pair_start = 1 + 3
        lower_pair_for_special = (pair_start, pair_start + 1)
        for i in has_prop:
            row = output[i]
            if all(row[k] == bkg for k in range(pair_start, pair_start + 2)):
                for k in range(pair_start, pair_start + 2):
                    row[k] = 8
    lower_pairs = compute_lower_pairs(clue)
    for i in range(max_prop_i + 1 if max_prop_i >= 0 else 16, 16):
        row = output[i]
        for ps, pe in lower_pairs:
            if all(row[k] == bkg for k in range(ps, pe + 1)):
                for k in range(ps, pe + 1):
                    row[k] = 8
    orig_min_row = {j: 19 for j in range(24)}
    orig_max_row = {j: -1 for j in range(24)}
    for i in range(19):
        for j in range(24):
            if g[6 + i][j] == 8:
                orig_min_row[j] = min(orig_min_row[j], i)
                orig_max_row[j] = max(orig_max_row[j], i)
    for j in range(24):
        if orig_max_row[j] >= 0:
            min_i = orig_min_row[j]
            for k in range(min_i - 1, -1, -1):
                if output[k][j] == bkg:
                    output[k][j] = 8
                else:
                    break
            max_i = orig_max_row[j]
            for k in range(max_i + 1, 19):
                if output[k][j] == bkg:
                    output[k][j] = 8
                else:
                    break
    for i in has_prop:
        row = output[i]
        eight_cols = [jj for jj in range(24) if row[jj] == 8]
        if eight_cols:
            minj = min(eight_cols)
            maxj = max(eight_cols)
            for jj in range(minj, maxj + 1):
                if row[jj] == bkg:
                    row[jj] = 8
    if upper_pairs:
        rightmost_pair = max(upper_pairs, key=lambda p: p[0])
        right_start = rightmost_pair[0]
        group_starts = [1, 7, 13, 19]
        gi = 0
        for gg in range(4):
            gs = group_starts[gg]
            if (gs <= right_start <= gs + 3) or (gg == 3 and right_start >= 19):
                gi = gg
                break
        group_start = group_starts[gi]
        if right_start == group_start + 1:
            upper_block_start = -1
            for ii in range(max_prop_i + 1 if max_prop_i >= 0 else 0):
                if all(output[ii][kk] == bkg for kk in range(24)):
                    upper_block_start = ii
                    break
            if upper_block_start != -1:
                num_rows = min(2, (max_prop_i - upper_block_start + 1 if max_prop_i >= 0 else 19 - upper_block_start))
                for ii in range(upper_block_start, upper_block_start + num_rows):
                    if ii > 18:
                        break
                    row = output[ii]
                    for jj in range(right_start, 24):
                        if row[jj] == bkg:
                            row[jj] = 8
    for ii in [14, 15]:
        if ii < 19:
            row = output[ii]
            eight_cols = [j for j in range(24) if row[j] == 8]
            if eight_cols:
                minj = min(eight_cols)
                maxj = max(eight_cols)
                for j in range(minj, maxj + 1):
                    if row[j] == bkg:
                        row[j] = 8
    first_color = get_clue_color(clue, 1)
    if first_color in [1, 2]:
        left_fill_start = 24
        if lower_pairs:
            left_fill_start = min(left_fill_start, min(p[0] for p in lower_pairs))
        orig_min_col = min((j for j in range(24) if orig_max_row[j] >= 0), default=24)
        left_fill_start = min(left_fill_start, orig_min_col)
        if left_fill_start < 24:
            for ii in [14, 15]:
                if ii < 19:
                    row = output[ii]
                    for j in range(left_fill_start, 24):
                        if row[j] == bkg:
                            row[j] = 8
    return output
```