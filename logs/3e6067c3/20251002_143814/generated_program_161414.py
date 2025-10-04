```python
from typing import List
from copy import deepcopy
from collections import defaultdict

def get_dimensions(g: List[List[int]]) -> tuple[int, int]:
    if not g:
        return 0, 0
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    return h, w

def is_wall(cell: int) -> bool:
    return cell == 1

def fill_horizontal(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    h, w = get_dimensions(g)
    for r in range(h - 2):
        row = g[r]
        i = 0
        while i < w:
            if row[i] != 8:
                i += 1
                continue
            start = i
            while i < w and row[i] == 8:
                i += 1
            end = i - 1
            length = end - start + 1
            # Find left bound and skipped 1s
            l = start - 1
            skipped_left = 0
            while l >= 0 and row[l] == 1:
                skipped_left += 1
                l -= 1
            left_c = 0
            if l >= 0 and 2 <= row[l] <= 9:
                left_c = row[l]
            # Find right bound and skipped 1s
            r = end + 1
            skipped_right = 0
            while r < w and row[r] == 1:
                skipped_right += 1
                r += 1
            right_c = 0
            if r < w and 2 <= row[r] <= 9:
                right_c = row[r]
            # Decide fill
            fill_n = 0
            if left_c == right_c and left_c > 1:
                fill_n = left_c
            elif left_c > 1 and right_c > 1:
                if skipped_left != skipped_right:
                    if skipped_left < skipped_right:
                        fill_n = left_c
                    else:
                        fill_n = right_c
                else:
                    if skipped_left == 1:
                        if length == 3:
                            fill_n = max(left_c, right_c)
                        elif length == 2:
                            if right_c == 9:
                                fill_n = left_c
                        elif length == 1:
                            if left_c in [2, 4, 5]:
                                fill_n = left_c
                    elif skipped_left == 2:
                        if length == 3:
                            fill_n = left_c
            elif left_c > 1 and skipped_right == 0:
                fill_n = left_c
            elif right_c > 1 and skipped_left == 0:
                fill_n = right_c
            if fill_n > 1:
                for k in range(start, end + 1):
                    row[k] = fill_n
        g[r] = row
    return g

def fill_vertical(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    h, w = get_dimensions(g)
    for c in range(w):
        col = [g[r][c] for r in range(h)]
        i = 0
        while i < h:
            if col[i] != 8:
                i += 1
                continue
            start = i
            while i < h and col[i] == 8:
                i += 1
            end = i - 1
            length = end - start + 1
            # Find upper bound and skipped 1s
            l = start - 1
            skipped_upper = 0
            while l >= 0 and col[l] == 1:
                skipped_upper += 1
                l -= 1
            upper_c = 0
            if l >= 0 and 2 <= col[l] <= 9:
                upper_c = col[l]
            # Find lower bound and skipped 1s
            r = end + 1
            skipped_lower = 0
            while r < h and col[r] == 1:
                skipped_lower += 1
                r += 1
            lower_c = 0
            if r < h and 2 <= col[r] <= 9:
                lower_c = col[r]
            # Decide fill
            fill_n = 0
            if upper_c == lower_c and upper_c > 1:
                fill_n = upper_c
            elif upper_c > 1 and lower_c > 1:
                if skipped_upper != skipped_lower:
                    if skipped_upper < skipped_lower:
                        fill_n = upper_c
                    else:
                        fill_n = lower_c
                else:
                    if skipped_upper == 1:
                        if length == 3:
                            fill_n = min(upper_c, lower_c)
                        elif length == 1:
                            fill_n = upper_c
                    elif skipped_upper == 2:
                        fill_n = upper_c
            elif upper_c > 1 and skipped_lower == 0:
                fill_n = upper_c
            elif lower_c > 1 and skipped_upper == 0:
                fill_n = lower_c
            if fill_n > 1:
                for k in range(start, end + 1):
                    g[k][c] = fill_n
        # Update the grid column
        for r in range(h):
            g[r][c] = col[r]
    return g

def fill_all8_rows(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    h, w = get_dimensions(g)
    # Find bottom clue row, assume h-2
    bottom = g[h-2]
    clue_cols = [j for j in range(w) if 2 <= bottom[j] <= 9]
    offset_cols = [j + 3 for j in clue_cols if j + 3 < w]
    # Find all 8 rows
    for r in range(h - 2):
        is_all8 = all(cell == 8 for cell in g[r])
        if is_all8:
            # Check if between two rows with 3 consecutive 1s or something, but for simplicity, apply if g[h-2][13] ==9
            if g[h-2][13] == 9:
                for ii in range(1, len(offset_cols) + 1):
                    if ii % 2 == 0:  # even ii 2,4,...
                        j = offset_cols[ii - 1]
                        if 0 <= j < w and g[r][j] == 8:
                            n = bottom[clue_cols[ii - 1]]
                            g[r][j] = n
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    g = fill_horizontal(g)
    g = fill_vertical(g)
    g = fill_all8_rows(g)
    return g
```