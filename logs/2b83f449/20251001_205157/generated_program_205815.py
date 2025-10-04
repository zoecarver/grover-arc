```python
from typing import List
from math import inf

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

def get_six_positions(row: List[int]) -> set:
    return {j for j in range(len(row)) if row[j] == 6}

def place_sixes(row: List[int], six_pos: set) -> None:
    w = len(row)
    for j in six_pos:
        if 0 <= j < w and row[j] != 0:
            row[j] = 6

def handle_upper_frame_borders(out: List[List[int]], i: int, six_pos_above_first: int, six_pos_above_last: int, has_zero: bool) -> None:
    row = out[i]
    w = len(row)
    end = w - 1
    if six_pos_above_first < w:
        # Left border
        if six_pos_above_first <= 4 or has_zero:
            row[0] = 3
        if six_pos_above_first <= 4 and w > 1:
            row[1] = 3
        # Right border
        if six_pos_above_last >= end - 4 or has_zero:
            row[end] = 3
        if six_pos_above_last >= end - 4 and w > 1:
            row[end - 1] = 3

def handle_closing_threes(row: List[int], six_pos: set, max_six: int) -> None:
    w = len(row)
    for j in range(w):
        if row[j] == 0 and max_six <= j and j > 0:
            row[j - 1] = 3

def handle_bottom_frame(out: List[int], i: int, six_pos: set) -> None:
    row = out[i]
    w = len(row)
    zeros = [j for j in range(w) if row[j] == 0]
    if not zeros:
        # Single segment 0 to w-1
        has_six = any(0 <= j < w for j in six_pos)
        if has_six:
            row[0] = 3
        row[w - 1] = 3
        return
    # Segments
    seg_starts = [0] + [zeros[k] + 1 for k in range(len(zeros))]
    k = 0
    for start in seg_starts:
        if start >= w:
            break
        end = w - 1 if k >= len(zeros) else zeros[k] - 1
        k += 1
        if start > end:
            continue
        # Check has six
        has_six = False
        for j in six_pos:
            if start <= j <= end:
                has_six = True
                break
        if has_six:
            row[start] = 3
        # Last segment end
        if end == w - 1:
            row[w - 1] = 3

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h = len(out)
    if h == 0:
        return out
    w = len(out[0])
    # Process content rows (odd indices)
    for i in range(1, h, 2):
        process_content_row(out[i])
    # Process frame rows (even indices)
    for i in range(0, h, 2):
        row = out[i]
        # Get six_pos
        six_pos = set()
        if i > 0:
            six_pos |= get_six_positions(out[i - 1])
        if i < h - 1:
            six_pos |= get_six_positions(out[i + 1])
        # Place sixes
        place_sixes(row, six_pos)
        # Compute max_six for closing
        max_six = max(six_pos) if six_pos else -1
        # Has zero
        has_zero = any(row[j] == 0 for j in range(w))
        if i == h - 1:
            # Bottom special
            handle_bottom_frame(out, i, six_pos)
        else:
            # Upper frame
            if i > 0:
                above = out[i - 1]
                first_six = inf
                last_six = -inf
                for j in range(w):
                    if above[j] == 6:
                        first_six = min(first_six, j)
                        last_six = max(last_six, j)
                if first_six < inf:
                    handle_upper_frame_borders(out, i, first_six, last_six, has_zero)
            # Closing threes (for all non-bottom frame)
            handle_closing_threes(row, six_pos, max_six)
    return out
```