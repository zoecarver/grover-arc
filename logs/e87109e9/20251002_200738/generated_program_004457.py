```python
from typing import List, Tuple
from collections import Counter
import copy

def program(g: List[List[int]]) -> List[List[int]]:
    if len(g) != 25 or len(g[0]) != 24:
        return []
    output = [row[:] for row in g[6:25]]
    bkg = find_background(output)
    replace_fives(output, bkg)
    clue_row = g[1]
    has_prop = get_has_prop_rows(g)
    max_prop_i = max(has_prop) if has_prop else -1
    upper_pairs_with_gi = compute_upper_pairs_with_gi(clue_row)
    lower_pairs = compute_lower_pairs(clue_row)
    orig_cols = get_original_eight_columns(g)
    pillar_cols = set()
    for start, _ in upper_pairs_with_gi:
        pillar_cols.add(start)
        pillar_cols.add(start + 1)
    for start, _ in lower_pairs:
        pillar_cols.add(start)
        pillar_cols.add(start + 1)
    for c in orig_cols:
        pillar_cols.add(c)
    min_pillar = min(pillar_cols) if pillar_cols else 0
    max_pillar = max(pillar_cols) if pillar_cols else 23
    place_upper_pillars(output, upper_pairs_with_gi, max_prop_i, bkg)
    place_lower_pillars(output, lower_pairs, max_prop_i, bkg)
    place_original_pillars(output, orig_cols, bkg)
    propagate_horizontal_in_has_prop(output, has_prop, min_pillar, max_pillar, bkg)
    apply_upper_right_fill(output, upper_pairs_with_gi, max_prop_i, bkg, g)
    apply_lower_bottom_fill(output, clue_row, max_prop_i, orig_cols, pillar_cols, bkg)
    return output

def find_background(grid: List[List[int]]) -> int:
    count = Counter()
    for row in grid:
        for cell in row:
            if cell not in [0, 5, 8]:
                count[cell] += 1
    return count.most_common(1)[0][0] if count else 3

def replace_fives(grid: List[List[int]], bkg: int) -> None:
    for row in grid:
        for j in range(len(row)):
            if row[j] == 5:
                row[j] = bkg

def get_has_prop_rows(g: List[List[int]]) -> List[int]:
    has_prop = []
    for i in range(19):
        if any(cell == 8 for cell in g[6 + i]):
            has_prop.append(i)
    return has_prop

def get_original_eight_columns(g: List[List[int]]) -> set:
    cols = set()
    for i in range(19):
        for j in range(24):
            if g[6 + i][j] == 8:
                cols.add(j)
    return cols

def compute_upper_pairs_with_gi(clue_row: List[int]) -> List[Tuple[int, int]]:
    group_starts = [1, 7, 13, 19]
    pairs = []
    skip_next = False
    for gi in range(4):
        if skip_next:
            skip_next = False
            continue
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
                    next_c = 0
                    if gi < 3:
                        next_c = get_clue_color(clue_row, group_starts[gi + 1])
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
            pairs.append((pair_start, gi))
    return pairs

def compute_lower_pairs(clue_row: List[int]) -> List[Tuple[int, int]]:
    return compute_seed_pairs(clue_row, True, 0)

def compute_seed_pairs(clue_row: List[int], is_lower: bool, max_group: int) -> List[Tuple[int, int]]:
    group_starts = [1, 7, 13, 19]
    pairs = []
    for gi in range(max_group + 1):
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
        pair_start = -1
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
        if pair_start != -1 and pair_start + 1 < 24:
            pairs.append((pair_start, pair_start + 1))
    return pairs

def get_group_info(clue_row: List[int], group_start: int) -> Tuple[int, int]:
    for p in range(4):
        val = clue_row[group_start + p]
        if val not in [0, 5]:
            return val, p
    return 0, -1

def get_clue_color(clue_row: List[int], group_start: int) -> int:
    return get_group_info(clue_row, group_start)[0]

def place_upper_pillars(grid: List[List[int]], pairs_with_gi: List[Tuple[int, int]], max_prop_i: int, bkg: int) -> None:
    num_rows = max_prop_i + 1 if max_prop_i >= 0 else len(grid)
    for pair_start, _ in pairs_with_gi:
        for c in range(pair_start, pair_start + 2):
            for r in range(num_rows):
                if grid[r][c] in (0, bkg):
                    grid[r][c] = 8

def place_lower_pillars(grid: List[List[int]], pairs: List[Tuple[int, int]], max_prop_i: int, bkg: int) -> None:
    start_row = max_prop_i + 1 if max_prop_i >= 0 else 0
    for start, end in pairs:
        for c in range(start, end + 1):
            for r in range(start_row, len(grid)):
                if grid[r][c] in (0, bkg):
                    grid[r][c] = 8

def place_original_pillars(grid: List[List[int]], cols: set, bkg: int) -> None:
    for c in cols:
        for r in range(len(grid)):
            if grid[r][c] in (0, bkg):
                grid[r][c] = 8

def propagate_horizontal_in_has_prop(grid: List[List[int]], has_prop: List[int], min_pillar: int, max_pillar: int, bkg: int) -> None:
    for i in has_prop:
        for j in range(min_pillar, max_pillar + 1):
            if grid[i][j] in (0, bkg):
                grid[i][j] = 8

def apply_upper_right_fill(grid: List[List[int]], pairs_with_gi: List[Tuple[int, int]], max_prop_i: int, bkg: int, original_g: List[List[int]]) -> None:
    if not pairs_with_gi:
        return
    # Find rightmost pair
    rightmost = max(pairs_with_gi, key=lambda x: x[0])
    pair_start, gi = rightmost
    group_starts = [1, 7, 13, 19]
    group_start = group_starts[gi]
    if pair_start != group_start + 1:
        return
    # Temp grid for checking all bkg, copy before placements
    temp = copy.deepcopy(original_g[6:25])
    replace_fives(temp, bkg)
    # Find first all bkg row in 0 to max_prop_i
    first_r = -1
    for r in range(max_prop_i + 1 if max_prop_i >= 0 else len(temp)):
        if all(cell in (0, bkg) for cell in temp[r]):
            first_r = r
            break
    if first_r == -1:
        return
    num_fill = min(2, (max_prop_i + 1 if max_prop_i >= 0 else len(grid)) - first_r)
    for k in range(num_fill):
        rr = first_r + k
        if rr >= len(grid):
            break
        for c in range(pair_start, 24):
            if grid[rr][c] in (0, bkg):
                grid[rr][c] = 8

def apply_lower_bottom_fill(grid: List[List[int]], clue_row: List[int], max_prop_i: int, orig_cols: set, pillar_cols: set, bkg: int) -> None:
    first_color = get_clue_color(clue_row, 1)
    if first_color not in [1, 2]:
        return
    num_rows = 1 if first_color == 1 else 2
    start_col = min(pillar_cols) if first_color == 1 else min(orig_cols) if orig_cols else min(pillar_cols)
    # After all placements, find empty lower rows
    lower_start = max_prop_i + 1 if max_prop_i >= 0 else 0
    empty_lower = []
    for r in range(lower_start, len(grid)):
        is_empty = all(cell in (0, bkg, 8) for cell in grid[r])
        if is_empty:
            empty_lower.append(r)
    # Bottommost (largest r)
    empty_lower.sort(reverse=True)
    fill_rows = empty_lower[:num_rows]
    for r in fill_rows:
        for c in range(start_col, 24):
            if grid[r][c] in (0, bkg):
                grid[r][c] = 8
```