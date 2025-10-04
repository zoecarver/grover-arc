```python
from typing import List, Tuple
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    if len(g) != 25 or len(g[0]) != 24:
        return []
    output = [row[:] for row in g[6:25]]
    bkg = find_background(g)
    replace_fives(output, bkg)
    clue_row = g[1]
    group_starts = [1, 7, 13, 19]
    upper_pairs = compute_upper_pairs(clue_row, group_starts)
    lower_pairs = compute_lower_pairs(clue_row, group_starts)
    anchor_min, anchor_max = get_original_eight_range(g)
    has_prop = find_has_prop_rows(output)
    max_prop_i = max(has_prop) if has_prop else -1
    first_color, first_pos = get_group_info(clue_row, group_starts[0])
    is_color_one_lower = (first_color == 1 and first_pos == 0)
    left_support_start = 4 if is_color_one_lower else -1
    place_seeds(output, upper_pairs, lower_pairs, anchor_min, anchor_max, max_prop_i, bkg, left_support_start, has_prop)
    propagate_gaps(output, has_prop, bkg)
    if is_color_one_lower:
        apply_lower_right_fill(output, bkg)
    apply_upper_right_fill(output, upper_pairs, bkg, group_starts)
    return output

def find_background(grid: List[List[int]]) -> int:
    count = Counter()
    for row in grid[6:25]:
        for cell in row:
            if cell not in [0, 5, 8]:
                count[cell] += 1
    return count.most_common(1)[0][0] if count else 3

def replace_fives(grid: List[List[int]], bkg: int):
    for row in grid:
        for j in range(len(row)):
            if row[j] == 5:
                row[j] = bkg

def get_group_info(clue_row: List[int], start: int) -> Tuple[int, int]:
    for p in range(4):
        val = clue_row[start + p]
        if val not in [0, 5]:
            return val, p
    return 0, -1

def compute_upper_pairs(clue_row: List[int], group_starts: List[int]) -> List[Tuple[int, int]]:
    pairs = []
    for gi in range(4):
        start = group_starts[gi]
        color, pos = get_group_info(clue_row, start)
        if color == 0 or color == 3:
            continue
        activate = False
        pair_start = -1
        if pos == 0:
            if color in [2, 4, 6]:
                activate = True
                if color == 6:
                    pair_start = start + 1
                elif color == 4:
                    next_color = 0
                    if gi < 3:
                        next_color, _ = get_group_info(clue_row, group_starts[gi + 1])
                    pair_start = start + 3 if next_color == 2 else start + 1
                elif color == 2:
                    pair_start = start + 3
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
        if activate and pair_start != -1 and pair_start + 1 < 24:
            pairs.append((pair_start, pair_start + 1))
            if color == 4 and pos == 0 and gi < 3:
                next_color, _ = get_group_info(clue_row, group_starts[gi + 1])
                if next_color == 2:
                    gi += 1  # skip next
    return pairs

def compute_lower_pairs(clue_row: List[int], group_starts: List[int]) -> List[Tuple[int, int]]:
    color, pos = get_group_info(clue_row, group_starts[0])
    if color == 1 and pos == 0:
        pair_start = group_starts[0] + 3
        if pair_start + 1 < 24:
            return [(pair_start, pair_start + 1)]
    return []

def get_original_eight_range(grid: List[List[int]]) -> Tuple[int, int]:
    min_col = 24
    max_col = -1
    for row in grid[6:25]:
        for j, cell in enumerate(row):
            if cell == 8:
                min_col = min(min_col, j)
                max_col = max(max_col, j)
    return (min_col, max_col) if max_col >= 0 else (24, -1)

def find_has_prop_rows(grid: List[List[int]]) -> List[int]:
    return [i for i, row in enumerate(grid) if any(c == 8 for c in row)]

def place_seeds(grid: List[List[int]], upper_pairs: List[Tuple[int, int]], lower_pairs: List[Tuple[int, int]], anchor_min: int, anchor_max: int, max_prop_i: int, bkg: int, left_support_start: int, has_prop: List[int]):
    for i in range(len(grid)):
        row = grid[i]
        # place anchor
        for j in range(anchor_min, anchor_max + 1):
            if row[j] == bkg:
                row[j] = 8
        # place upper pairs
        if max_prop_i < 0 or i <= max_prop_i:
            for start, end in upper_pairs:
                place_pair(row, start, end, bkg)
        # place lower pairs
        if max_prop_i < 0 or i > max_prop_i:
            for start, end in lower_pairs:
                place_pair(row, start, end, bkg)
    # special left support in upper has_prop for color1 pos0
    if left_support_start >= 0:
        for i in has_prop:
            if i <= max_prop_i:
                row = grid[i]
                place_pair(row, left_support_start, left_support_start + 1, bkg)

def place_pair(row: List[int], start: int, end: int, bkg: int):
    can_place = True
    for j in range(start, end + 1):
        if row[j] != bkg:
            can_place = False
            break
    if can_place:
        for j in range(start, end + 1):
            row[j] = 8

def propagate_gaps(grid: List[List[int]], has_prop: List[int], bkg: int):
    for i in has_prop:
        row = grid[i]
        eight_cols = [j for j in range(24) if row[j] == 8]
        if eight_cols:
            min_j = min(eight_cols)
            max_j = max(eight_cols)
            for j in range(min_j, max_j + 1):
                if row[j] == bkg:
                    row[j] = 8

def apply_lower_right_fill(grid: List[List[int]], bkg: int):
    left_start = 4
    for i in range(14, 16):
        if i < len(grid):
            row = grid[i]
            for j in range(left_start, 24):
                if row[j] == bkg:
                    row[j] = 8

def apply_upper_right_fill(grid: List[List[int]], upper_pairs: List[Tuple[int, int]], bkg: int, group_starts: List[int]):
    if not upper_pairs:
        return
    rightmost_start = upper_pairs[-1][0]
    is_plus1 = False
    for gs in group_starts:
        if abs(rightmost_start - gs) <= 3 and rightmost_start == gs + 1:
            is_plus1 = True
            break
    if not is_plus1:
        return
    # find upper block
    upper_block = []
    for i in range(len(grid)):
        if all(c == bkg for c in grid[i]):
            upper_block.append(i)
        else:
            break
    # fill first 2
    for k in range(min(2, len(upper_block))):
        i = upper_block[k]
        row = grid[i]
        for j in range(rightmost_start, 24):
            if row[j] == bkg:
                row[j] = 8
```