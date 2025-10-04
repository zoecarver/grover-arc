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

def get_clue_color(clue_row: List[int], group_start: int) -> int:
    for p in range(4):
        val = clue_row[group_start + p]
        if val not in [0, 5]:
            return val
    return 0

def compute_seed_pairs(clue_row: List[int], is_lower: bool, max_group: int) -> List[Tuple[int, int]]:
    group_starts = [1, 7, 13, 19]
    seed_pairs = []
    for gi in range(max_group + 1):
        start = group_starts[gi]
        group = clue_row[start:start + 4]
        color_pos = -1
        color = 0
        for p in range(4):
            val = group[p]
            if val not in [0, 5]:
                color_pos = p
                color = val
                break
        activate = False
        if color_pos != -1 and color != 3:
            if color_pos == 0:
                if color in [4, 6] or (is_lower and color == 1):
                    activate = True
            elif color_pos == 3:
                if color in [2, 4, 6]:
                    activate = True
        if not activate:
            continue
        if color_pos == 0:
            if color == 6 or (color == 1 and is_lower):
                pair_start = start + 1
            elif color == 4:
                next_color = 0
                if gi < 3:
                    next_start = group_starts[gi + 1]
                    next_color = get_clue_color(clue_row, next_start)
                if next_color == 2:
                    pair_start = start + 3
                else:
                    pair_start = start + 1
            else:  # color == 1 and is_lower
                pair_start = start + 3
        else:  # color_pos == 3
            if color == 2:
                pair_start = start + 3
                if start == 19:
                    pair_start = 18
            elif color == 4:
                pair_start = start + 2
            elif color == 6:
                pair_start = start + 1
        pair_end = pair_start + 1
        if pair_end < 24:
            seed_pairs.append((pair_start, pair_end))
    return seed_pairs

def get_has_prop_rows(grid: List[List[int]]) -> List[int]:
    has_prop = []
    for i in range(19):
        if any(cell == 8 for cell in grid[6 + i]):
            has_prop.append(i)
    return has_prop

def propagate_has_prop(row: List[int], bkg: int) -> List[int]:
    new_row = row[:]
    eight_cols = [j for j, cell in enumerate(new_row) if cell == 8]
    if not eight_cols:
        return new_row
    min_j = min(eight_cols)
    max_j = max(eight_cols)
    for j in range(min_j, max_j + 1):
        if new_row[j] == bkg:
            new_row[j] = 8
    return new_row

def is_all_bkg_row(row: List[int], bkg: int) -> bool:
    return all(cell == bkg for cell in row)

def program(g: List[List[int]]) -> List[List[int]]:
    if len(g) != 25 or len(g[0]) != 24:
        return []
    output = [row[:] for row in g[6:25]]
    bkg = find_background(output)
    for row in output:
        for j in range(24):
            if row[j] == 5:
                row[j] = bkg
    clue_row = g[1]
    has_prop = get_has_prop_rows(g)
    max_prop_i = max(has_prop) if has_prop else -1
    upper_pairs = compute_seed_pairs(clue_row, False, 3)
    lower_pairs = compute_seed_pairs(clue_row, True, 1)
    # Place upper pairs in rows 0 to max_prop_i
    for i in range(max_prop_i + 1 if max_prop_i >= 0 else 0):
        row = output[i]
        for pair_start, pair_end in upper_pairs:
            for j in range(pair_start, pair_end + 1):
                if row[j] == bkg:
                    row[j] = 8
    # Place lower pairs in rows max_prop_i+1 to 18
    for i in range(max_prop_i + 1 if max_prop_i >= 0 else 0, 19):
        row = output[i]
        for pair_start, pair_end in lower_pairs:
            for j in range(pair_start, pair_end + 1):
                if row[j] == bkg:
                    row[j] = 8
    # Place lower pairs in has_prop rows
    for i in has_prop:
        row = output[i]
        for pair_start, pair_end in lower_pairs:
            for j in range(pair_start, pair_end + 1):
                if row[j] == bkg:
                    row[j] = 8
    # Propagate in has_prop rows
    for i in has_prop:
        output[i] = propagate_has_prop(output[i], bkg)
    # Upper right fill (check before placing pairs, so recompute initial all bkg)
    temp_output = [row[:] for row in output]  # reset for check
    upper_block_start = 0
    while upper_block_start < 19 and not is_all_bkg_row(temp_output[upper_block_start], bkg):
        upper_block_start += 1
    num_fill = min(2, 19 - upper_block_start)
    is_plus1 = False
    if upper_pairs:
        right_start = max(start for start, _ in upper_pairs)
        group_starts = [1, 7, 13, 19]
        for gs in group_starts:
            if right_start == gs + 1:
                is_plus1 = True
                break
    if is_plus1 and upper_pairs:
        right_start = max(start for start, _ in upper_pairs)
        for k in range(num_fill):
            i = upper_block_start + k
            if i >= 19:
                break
            row = output[i]
            for j in range(right_start, 24):
                if row[j] == bkg:
                    row[j] = 8
    # Lower right fill
    first_color = get_clue_color(clue_row, 1)
    if first_color in [1, 2]:
        lower_start = 13 if first_color == 2 else 14
        num = 2
        left_start = min([p[0] for p in lower_pairs] or [0])
        for k in range(num):
            i = lower_start + k
            if i >= 19:
                break
            row = output[i]
            for j in range(left_start, 24):
                if row[j] == bkg:
                    row[j] = 8
    return output
```