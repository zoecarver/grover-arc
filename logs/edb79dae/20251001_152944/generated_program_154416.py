```python
from typing import List, Dict, Tuple
from collections import Counter

def find_top_bottom(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    row_len = len(g[0])
    candidates = []
    for i in range(len(g)):
        count_5 = sum(1 for x in g[i] if x == 5)
        if count_5 > row_len // 2:
            candidates.append(i)
    if not candidates:
        return 0, len(g) - 1
    return min(candidates), max(candidates)

def _find_run(row: List[int], color: int, n: int) -> Tuple[int, int]:
    max_len = 0
    curr_len = 0
    start = 0
    end = 0
    curr_start = 0
    for j in range(n + 1):
        if j < n and row[j] == color:
            if curr_len == 0:
                curr_start = j
            curr_len += 1
            if curr_len > max_len:
                max_len = curr_len
                start = curr_start
                end = j
        else:
            curr_len = 0
    return start, end

def find_left_right(g: List[List[int]], top: int, bottom: int) -> Tuple[int, int]:
    row_top = g[top]
    row_bot = g[bottom]
    n = len(row_top)
    start_t, end_t = _find_run(row_top, 5, n)
    start_b, end_b = _find_run(row_bot, 5, n)
    left = max(start_t, start_b)
    right = min(end_t, end_b)
    return left, right

def extract_mappings(g: List[List[int]], top: int) -> Dict[int, int]:
    mappings: Dict[int, int] = {}
    for i in range(top + 1):
        row = g[i]
        j = 0
        n = len(row)
        while j < n:
            if row[j] == 5:
                break
            color = row[j]
            run_start = j
            while j < n and row[j] == color:
                j += 1
            run_len = j - run_start
            if run_len < 2:
                continue
            if j >= n:
                break
            next_color = row[j]
            if next_color == 5:
                break
            next_start = j
            while j < n and row[j] == next_color:
                j += 1
            next_len = j - next_start
            if next_len < 2:
                continue
            if color != next_color:
                mappings[color] = next_color
    return mappings

def find_background(g: List[List[int]], top: int, bottom: int, left: int, right: int) -> int:
    count = Counter()
    for i in range(top + 1, bottom):
        for j in range(left + 1, right):
            val = g[i][j]
            if val != 5:
                count[val] += 1
    if not count:
        return 0
    return count.most_common(1)[0][0]

def build_output(g: List[List[int]], top: int, bottom: int, left: int, right: int,
                 mappings: Dict[int, int], bg: int) -> List[List[int]]:
    h = bottom - top + 1
    w = right - left + 1
    out = [[0] * w for _ in range(h)]
    # Set border rows to full 5s
    for j in range(w):
        out[0][j] = 5
        out[h - 1][j] = 5
    # Set side columns for inner rows
    for i in range(1, h - 1):
        out[i][0] = 5
        out[i][w - 1] = 5
    # Fill inner areas
    inner_start_row = top + 1
    num_inner = h - 2
    for k in range(num_inner):
        i_out = 1 + k
        r_in = inner_start_row + k
        inner_input = g[r_in][left + 1 : right]
        inner_w = len(inner_input)
        j = 0
        while j < inner_w:
            val = inner_input[j]
            if val == 5 or val == bg:
                start_j = j
                while j < inner_w and inner_input[j] == val:
                    j += 1
                for p in range(start_j, j):
                    out[i_out][1 + p] = val
            else:
                start_j = j
                while j < inner_w and inner_input[j] == val:
                    j += 1
                l = j - start_j
                m = mappings.get(val, val)
                for p in range(l):
                    out[i_out][1 + start_j + p] = m if p % 2 == 0 else bg
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    top, bottom = find_top_bottom(g)
    left, right = find_left_right(g, top, bottom)
    mappings = extract_mappings(g, top)
    bg = find_background(g, top, bottom, left, right)
    return build_output(g, top, bottom, left, right, mappings, bg)
```