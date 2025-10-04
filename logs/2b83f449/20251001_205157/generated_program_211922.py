```python
from typing import List, Set
import math

inf = math.inf

def process_content_row(row: List[int]) -> None:
    j = 0
    w = len(row)
    while j < w - 2:
        if row[j] == 7 and row[j + 1] == 7 and row[j + 2] == 7:
            row[j] = 8
            row[j + 1] = 6
            row[j + 2] = 8
            j += 3
        else:
            j += 1

def get_six_positions(row: List[int]) -> Set[int]:
    return {j for j, val in enumerate(row) if val == 6}

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    m = len(g)
    if m == 0:
        return []
    w = len(g[0])
    out = [row[:] for row in g]
    for i in range(1, m, 2):
        if i < m:
            process_content_row(out[i])
    for i in range(0, m, 2):
        if i >= m:
            continue
        orig = g[i]
        above_six = get_six_positions(out[i - 1]) if i > 0 else set()
        below_six = get_six_positions(out[i + 1]) if i < m - 1 else set()
        all_six = above_six.union(below_six)
        new_row = [0 if orig[j] == 0 else 8 for j in range(w)]
        for j in all_six:
            if 0 <= j < w:
                new_row[j] = 6
        is_top = (i == 0)
        is_bottom = (i == m - 1)
        if is_top:
            out[i] = new_row
            continue
        # Handle edge 3s
        if is_bottom:
            # Left edge
            first_zero = w
            for jj in range(w):
                if orig[jj] == 0:
                    first_zero = jj
                    break
            left_six = [jj for jj in all_six if jj < first_zero]
            if left_six:
                seg_min = min(left_six)
                new_row[0] = 3
                if seg_min <= 4 and w > 1 and new_row[1] == 8:
                    new_row[1] = 3
            # Right edge
            last_zero = -1
            for jj in range(w - 1, -1, -1):
                if orig[jj] == 0:
                    last_zero = jj
                    break
            right_six = [jj for jj in all_six if jj > last_zero]
            if right_six:
                seg_max = max(right_six)
                new_row[w - 1] = 3
                if (w - 1 - seg_max) <= 4 and w > 1 and new_row[w - 2] == 8:
                    new_row[w - 2] = 3
        else:
            # Internal non-bottom edge 3s only if both adjacent have 6s
            if above_six and below_six:
                upper_min = min(above_six)
                upper_max = max(above_six)
                lower_min = min(below_six)
                lower_max = max(below_six)
                # Left
                if upper_min < lower_min and new_row[0] == 8:
                    new_row[0] = 3
                    if upper_min <= 4 and w > 1 and new_row[1] == 8:
                        new_row[1] = 3
                # Right
                if upper_max > lower_max and new_row[w - 1] == 8:
                    new_row[w - 1] = 3
                    if (w - 1 - upper_max) <= 4 and w > 1 and new_row[w - 2] == 8:
                        new_row[w - 2] = 3
        # Handle internal gaps for non-top
        # Closing 3s before 0s (only for non-bottom)
        if not is_bottom:
            j = 0
            while j < w:
                if new_row[j] == 0:
                    j += 1
                    continue
                has6 = False
                seg_start = j
                while j < w and new_row[j] != 0:
                    if new_row[j] == 6:
                        has6 = True
                    j += 1
                seg_end = j - 1
                if has6 and j < w and new_row[j] == 0 and new_row[seg_end] == 8:
                    new_row[seg_end] = 3
        # Opening 3s after 0s (for all non-top)
        j = 0
        while j < w - 1:
            if new_row[j] != 0:
                j += 1
                continue
            if new_row[j + 1] == 0:
                j += 1
                continue
            # Start of segment after 0
            seg_start = j + 1
            has6 = False
            k = j + 1
            while k < w and new_row[k] != 0:
                if new_row[k] == 6:
                    has6 = True
                k += 1
            if has6 and new_row[seg_start] == 8:
                new_row[seg_start] = 3
            j = k
        out[i] = new_row
    return out
```