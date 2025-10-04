```python
from typing import List, Tuple
from collections import Counter

def find_background(grid: List[List[int]]) -> int:
    count = Counter()
    for row in grid[6:25]:
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

def compute_upper_pairs(clue_row: List[int]) -> List[Tuple[int, int]]:
    group_starts = [1, 7, 13, 19]
    pairs = []
    for gi in range(4):
        start = group_starts[gi]
        color, pos = get_group_info(clue_row, start)
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
                    next_color = 0
                    if gi < 3:
                        next_color, _ = get_group_info(clue_row, group_starts[gi + 1])
                    pair_start = start + 3 if next_color == 2 else start + 1
        elif pos == 3:
            if color in [2, 4, 6]:
                activate = True
                if color == 2:
                    pair_start = start + 3
                    if start == 19:
                        pair_start = 18
                elif color == 4:
                    pair_start = start + 2
                elif color == 6:
                    pair_start = start + 1
        if activate and 0 <= pair_start < 23:
            pairs.append((pair_start, pair_start + 1))
    return pairs

def compute_lower_pair(clue_row: List[int]) -> Tuple[int, int]:
    group_start = 1
    color, pos = get_group_info(clue_row, group_start)
    if color == 0 or color == 3:
        return (-1, -1)
    activate = False
    pair_start = -1
    if pos == 0:
        if color in [4, 6, 1]:
            activate = True
            if color == 6:
                pair_start = group_start + 1
            elif color == 1:
                pair_start = group_start + 3
            elif color == 4:
                pair_start = group_start + 1
    elif pos == 3:
        if color in [4, 6]:
            activate = True
            if color == 4:
                pair_start = group_start + 2
            elif color == 6:
                pair_start = group_start + 1
    if activate and 0 <= pair_start < 23:
        return (pair_start, pair_start + 1)
    return (-1, -1)

def get_original_eight_range(grid: List[List[int]]) -> Tuple[int, int]:
    min_col = 24
    max_col = -1
    for row in grid[6:25]:
        for j, cell in enumerate(row):
            if cell == 8:
                min_col = min(min_col, j)
                max_col = max(max_col, j)
    return min_col, max_col if max_col >= 0 else (24, -1)

def get_has_prop_rows(grid: List[List[int]]) -> List[int]:
    has_prop = []
    for i in range(19):
        if any(cell == 8 for cell in grid[6 + i]):
            has_prop.append(i)
    return has_prop

def get_first_color(clue_row: List[int]) -> int:
    return get_group_info(clue_row, 1)[0]

def apply_right_fill_upper(output: List[List[int]], upper_pairs: List[Tuple[int, int]], bkg: int, max_prop_i: int, clue_row: List[int]):
    if not upper_pairs:
        return
    group_starts = [1, 7, 13, 19]
    rightmost_ps, _ = max(upper_pairs, key=lambda p: p[0])
    gi = -1
    for g in range(4):
        start = group_starts[g]
        c, p = get_group_info(clue_row, start)
        if c == 0 or c == 3:
            continue
        computed_ps = -1
        if p == 0:
            if c in [4, 6]:
                if c == 6:
                    computed_ps = start + 1
                elif c == 4:
                    next_c = 0
                    if g < 3:
                        next_c, _ = get_group_info(clue_row, group_starts[g + 1])
                    computed_ps = start + 3 if next_c == 2 else start + 1
        elif p == 3:
            if c in [2, 4, 6]:
                if c == 2:
                    computed_ps = start + 3 if start != 19 else 18
                elif c == 4:
                    computed_ps = start + 2
                elif c == 6:
                    computed_ps = start + 1
        if computed_ps == rightmost_ps:
            gi = g
            break
    if gi != -1 and rightmost_ps == group_starts[gi] + 1:
        for r in range(max_prop_i + 1):
            if all(output[r][j] == bkg for j in range(24)):
                ps = rightmost_ps
                for j in range(ps, 24):
                    output[r][j] = 8
                return  # only first

def program(g: List[List[int]]) -> List[List[int]]:
    if len(g) < 25 or len(g[0]) != 24:
        return []
    bkg = find_background(g)
    output = [row[:] for row in g[6:25]]
    for row in output:
        for j in range(24):
            if row[j] == 5:
                row[j] = bkg
    clue_row = g[1]
    upper_pairs = compute_upper_pairs(clue_row)
    lower_pair = compute_lower_pair(clue_row)
    min_col, max_col = get_original_eight_range(g)
    has_prop_rows = get_has_prop_rows(g)
    max_prop_i = max(has_prop_rows) if has_prop_rows else -1
    first_color = get_first_color(clue_row)
    apply_right_fill_upper(output, upper_pairs, bkg, max_prop_i, clue_row)
    for out_row in range(19):
        row = output[out_row]
        is_upper = out_row <= max_prop_i
        is_lower_special = (14 <= out_row <= 15) and first_color in [1, 2, 4]
        # place seeds
        if is_upper:
            for ps, pe in upper_pairs:
                if all(row[j] == bkg for j in range(ps, pe + 1)):
                    for j in range(ps, pe + 1):
                        row[j] = 8
        else:
            lp_ps, lp_pe = lower_pair
            if lp_ps != -1:
                if all(row[j] == bkg for j in range(lp_ps, lp_pe + 1)):
                    for j in range(lp_ps, lp_pe + 1):
                        row[j] = 8
            if min_col < 24 and not is_lower_special:
                if all(row[j] == bkg for j in range(min_col, max_col + 1)):
                    for j in range(min_col, max_col + 1):
                        row[j] = 8
        # gap fill in has_prop rows
        if out_row in has_prop_rows:
            eight_cols = [j for j in range(24) if row[j] == 8]
            if eight_cols:
                minj = min(eight_cols)
                maxj = max(eight_cols)
                for j in range(minj, maxj + 1):
                    if row[j] == bkg:
                        row[j] = 8
        # special lower fill
        if is_lower_special:
            eight_cols = [j for j in range(24) if row[j] == 8]
            if eight_cols and min_col < 24:
                leftmost = min(eight_cols)
                if first_color == 1:
                    to_col = 23
                elif first_color == 2:
                    leftmost = min_col
                    to_col = 23
                elif first_color == 4:
                    leftmost = min(eight_cols)
                    to_col = min_col
                else:
                    return output
                for j in range(leftmost, to_col + 1):
                    if row[j] == bkg:
                        row[j] = 8
    return output
```