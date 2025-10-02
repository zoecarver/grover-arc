```python
from typing import List, Dict

def find_top_bottom(g: List[List[int]]) -> tuple[int, int]:
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

def find_left_right(g: List[List[int]], top: int, bottom: int) -> tuple[int, int]:
    row = g[top]
    n = len(row)
    max_len = 0
    curr_len = 0
    start = 0
    end = 0
    curr_start = 0
    for j in range(n + 1):
        if j < n and row[j] == 5:
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
                break  # only first pair per row
    return mappings

def find_background(g: List[List[int]], top: int, bottom: int, left: int, right: int) -> int:
    inner_left = left + 1
    inner_right = right - 1
    if inner_left > inner_right:
        return 0
    for i in range(top + 1, bottom):
        row = g[i]
        inner_vals = row[inner_left:inner_right + 1]
        if inner_vals and all(x == inner_vals[0] for x in inner_vals) and inner_vals[0] != 5:
            return inner_vals[0]
    return 0  # default if not found

def build_output(g: List[List[int]], top: int, bottom: int, left: int, right: int,
                 mappings: Dict[int, int], bg: int) -> List[List[int]]:
    h = bottom - top + 1
    w = right - left + 1
    out: List[List[int]] = [[0] * w for _ in range(h)]
    for i in range(h):
        in_row_idx = top + i
        row_in = g[in_row_idx]
        for j in range(w):
            in_col_idx = left + j
            val = row_in[in_col_idx]
            if val == 5:
                out[i][j] = 5
            elif val == bg:
                out[i][j] = bg
            else:
                out[i][j] = mappings.get(val, val)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    top, bottom = find_top_bottom(g)
    left, right = find_left_right(g, top, bottom)
    mappings = extract_mappings(g, top)
    bg = find_background(g, top, bottom, left, right)
    return build_output(g, top, bottom, left, right, mappings, bg)
```