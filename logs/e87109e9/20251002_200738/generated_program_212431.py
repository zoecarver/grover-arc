```python
from typing import List, Tuple
from collections import Counter

def find_background(grid: List[List[int]]) -> int:
    count = Counter()
    for row in grid[6:]:
        for cell in row:
            if cell not in [0, 5, 8]:
                count[cell] += 1
    return max(count, key=count.get) if count else 3

def get_clue_color(clue_row: List[int], group_start: int) -> int:
    for p in range(4):
        val = clue_row[group_start + p]
        if val not in [0, 5]:
            return val
    return 0

def compute_seed_pairs(clue_row: List[int], is_lower: bool, max_gi: int) -> List[Tuple[int, int]]:
    group_starts = [1, 7, 13, 19]
    seed_pairs = []
    for gi in range(max_gi + 1):
        start = group_starts[gi]
        color_pos = -1
        color = 0
        for p in range(4):
            val = clue_row[start + p]
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
        pair_start = 0
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
            else:
                pair_start = start + 3
        else:
            if color == 2:
                pair_start = start + 3
                if start == 19:
                    pair_start = start + 1
            elif color == 4:
                pair_start = start + 2
            elif color == 6:
                pair_start = start + 1
        pair_end = pair_start + 1
        if pair_end <= 23:
            seed_pairs.append((pair_start, pair_end))
    return seed_pairs

def get_first_group_info(clue_row: List[int]) -> Tuple[int, int, int]:
    start = 1
    color_pos = -1
    color = 0
    for p in range(4):
        val = clue_row[start + p]
        if val not in [0, 5]:
            color_pos = p
            color = val
            break
    pair_start = 0
    if color_pos == 0 and color == 1:
        pair_start = start + 3
    elif color_pos == 3:
        if color == 2:
            pair_start = start + 3
        elif color == 4:
            pair_start = start + 2
        elif color == 6:
            pair_start = start + 1
    return color, pair_start, pair_start + 1

def get_original_eight_range(grid: List[List[int]]) -> Tuple[int, int]:
    min_col = 24
    max_col = -1
    for i in range(6, 25):
        row = grid[i]
        for j, cell in enumerate(row):
            if cell == 8:
                min_col = min(min_col, j)
                max_col = max(max_col, j)
    return min_col, max_col if max_col >= 0 else (0, -1)

def find_has_prop_rows(grid: List[List[int]]) -> List[int]:
    has_prop = []
    for i in range(19):
        row = grid[6 + i]
        if any(cell == 8 for cell in row):
            has_prop.append(i)
    return has_prop

def is_all_bkg_row(row: List[int], bkg: int) -> bool:
    return all(cell == bkg for cell in row)

def place_seeds(row: List[int], bkg: int, pairs: List[Tuple[int, int]]) -> List[int]:
    new_row = row[:]
    for start, end in pairs:
        for j in range(start, end + 1):
            if j < 24 and new_row[j] == bkg:
                new_row[j] = 8
    return new_row

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

def propagate_lower_prop_right_fill(row: List[int], bkg: int, left_start: int) -> List[int]:
    new_row = row[:]
    for j in range(left_start, 24):
        if new_row[j] == bkg:
            new_row[j] = 8
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    if len(g) != 25 or len(g[0]) != 24:
        return []
    bkg = find_background(g)
    clue_row = g[1]
    upper_pairs = compute_seed_pairs(clue_row, False, 3)
    first_color, first_start, first_end = get_first_group_info(clue_row)
    original_min, original_max = get_original_eight_range(g)
    has_prop_rows = find_has_prop_rows(g)
    max_prop_i = max(has_prop_rows) if has_prop_rows else -1
    output = [row[:] for row in g[6:25]]
    for row in output:
        for j in range(24):
            if row[j] == 5:
                row[j] = bkg
    # Upper block for right prop
    upper_block_start = 0
    upper_block_end = 0
    for i in range(19):
        if is_all_bkg_row(output[i], bkg):
            upper_block_end = i + 1
        else:
            break
    rightmost_pair = max(upper_pairs, key=lambda p: p[0]) if upper_pairs else (0, 0)
    is_plus1 = False
    for gi in range(4):
        start = [1, 7, 13, 19][gi]
        if rightmost_pair[0] == start + 1:
            is_plus1 = True
            break
    right_fill_start = rightmost_pair[0] if is_plus1 else -1
    for i in range(upper_block_start, min(upper_block_start + 2, upper_block_end)):
        output[i] = place_seeds(output[i], bkg, upper_pairs)
        if right_fill_start >= 0:
            output[i] = propagate_lower_prop_right_fill(output[i], bkg, right_fill_start)
    # Place upper pairs in 0 to max_prop_i
    for i in range(max(0, max_prop_i + 1)):
        output[i] = place_seeds(output[i], bkg, upper_pairs)
    # Has prop propagation
    for i in has_prop_rows:
        output[i] = propagate_has_prop(output[i], bkg)
    # Lower pairs
    lower_pairs = []
    if first_color in [1, 4]:
        lower_pairs.append((first_start, first_end))
    if original_max >= 0:
        lower_pairs.append((original_min, original_max))
    # Place lower pairs in max_prop_i +1 to 18
    for i in range(max_prop_i + 1, 19):
        output[i] = place_seeds(output[i], bkg, lower_pairs)
    # Lower prop rows
    lower_prop_start = 14 if first_color in [1, 4] else 13
    num_lower_prop = 2
    left_fill_start = first_start if first_color in [1, 4] else original_min
    for i in range(lower_prop_start, min(lower_prop_start + num_lower_prop, 19)):
        if first_color in [1, 2]:
            output[i] = propagate_lower_prop_right_fill(output[i], bkg, left_fill_start)
        else:
            output[i] = propagate_has_prop(output[i], bkg)
    return output
```