```python
from typing import List, Dict, Tuple
from collections import Counter

def find_top_bottom(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    row_len = len(g[0])
    candidates = [i for i in range(len(g)) if sum(1 for x in g[i] if x == 5) > row_len // 2]
    if not candidates:
        return 0, len(g) - 1
    return min(candidates), max(candidates)

def _find_run(row: List[int], color: int) -> Tuple[int, int]:
    n = len(row)
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
    start_t, end_t = _find_run(row_top, 5)
    start_b, end_b = _find_run(row_bot, 5)
    left = max(start_t, start_b)
    right = min(end_t, end_b)
    return left, right

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

def extract_mappings(g: List[List[int]], top: int, bg: int) -> Dict[int, int]:
    mappings = {}
    for i in range(top + 1):
        row = g[i]
        j = 0
        n = len(row)
        while j < n:
            while j < n and (row[j] == 5 or row[j] == bg):
                j += 1
            if j >= n:
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
            if next_color == 5 or next_color == bg:
                continue
            next_start = j
            while j < n and row[j] == next_color:
                j += 1
            next_len = j - next_start
            if next_len < 2 or next_color == color:
                continue
            mappings[color] = next_color
    return mappings

def transform_row(row: List[int], mappings: Dict[int, int], bg: int) -> List[int]:
    out = []
    j = 0
    m = len(row)
    while j < m:
        val = row[j]
        run_start = j
        while j < m and row[j] == val:
            j += 1
        l = j - run_start
        if val == 5 or val == bg:
            out.extend([val] * l)
            continue
        mapped_c = mappings.get(val, val)
        out.extend([mapped_c] * l)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    top, bottom = find_top_bottom(g)
    left, right = find_left_right(g, top, bottom)
    w = right - left + 1
    bg = find_background(g, top, bottom, left, right)
    mappings = extract_mappings(g, top, bg)
    out = []
    out.append([5] * w)
    inner_height = bottom - top - 1
    for oi in range(inner_height):
        ii = top + 1 + oi
        inner_input = g[ii][left + 1 : right]
        trans = transform_row(inner_input, mappings, bg)
        out_row = [5] + trans + [5]
        out.append(out_row)
    out.append([5] * w)
    return out
```