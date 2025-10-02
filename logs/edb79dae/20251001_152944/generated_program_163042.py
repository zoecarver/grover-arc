```python
from typing import List, Tuple, Dict
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
    inner_h = bottom - top - 1
    inner_w = right - left - 1
    if inner_h <= 0 or inner_w <= 0:
        return 0
    for i in range(top + 1, bottom):
        for j in range(left + 1, right):
            val = g[i][j]
            if val != 5:
                count[val] += 1
    if not count:
        return 0
    return count.most_common(1)[0][0]

def extract_mappings(g: List[List[int]], top: int, bg: int) -> Dict[int, int]:
    mappings: Dict[int, int] = {}
    for i in range(top + 1):
        row = g[i]
        j = 0
        n = len(row)
        while j < n:
            # skip 5 or bg runs
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
            # skip if next is 5 or bg
            if next_color == 5 or next_color == bg:
                while j < n and row[j] == next_color:
                    j += 1
                continue
            next_start = j
            while j < n and row[j] == next_color:
                j += 1
            next_len = j - next_start
            if next_len < 2 or color == next_color:
                continue
            mappings[color] = next_color
            break  # only first pair per row
    return mappings

def build_thinned(mapped: List[int], bg: int) -> List[int]:
    thinned = []
    j = 0
    n = len(mapped)
    while j < n:
        v = mapped[j]
        start = j
        while j < n and mapped[j] == v:
            j += 1
        l = j - start
        if v == bg:
            thinned.extend([bg] * l)
            continue
        if l <= 2:
            thinned.extend([v] * l)
            continue
        thinned.append(v)
        thinned.extend([bg] * (l - 2))
        thinned.append(v)
    return thinned

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    top, bottom = find_top_bottom(g)
    left, right = find_left_right(g, top, bottom)
    width = right - left + 1
    height = bottom - top + 1
    bg = find_background(g, top, bottom, left, right)
    mappings = extract_mappings(g, top, bg)
    # get inner input rows
    inner_len = right - left - 1
    inner_rows = [g[i][left + 1 : right] for i in range(top + 1, bottom)]
    # group into stacks
    stacks = []
    i = 0
    n_inner = len(inner_rows)
    while i < n_inner:
        start_i = i
        current = inner_rows[i]
        is_all_bg = all(v == bg for v in current)
        while i < n_inner and inner_rows[i] == current:
            i += 1
        h = i - start_i
        stacks.append((h, current, is_all_bg))
    # generate out_inner
    out_inner = []
    for h, current, is_all_bg in stacks:
        mapped_row = [mappings.get(v, v) if v != bg else bg for v in current]
        if is_all_bg:
            bg_row = [bg] * inner_len
            for _ in range(h):
                out_inner.append(bg_row)
            continue
        # pattern stack
        for k in range(h):
            if k == 0 or k == h - 1:
                this_row = build_thinned(mapped_row, bg)
            else:
                this_row = mapped_row[:]
            out_inner.append(this_row)
    # build out
    out = [[5] * width for _ in range(height)]
    # top and bottom already full 5
    for kk in range(len(out_inner)):
        row_idx = 1 + kk
        transformed = out_inner[kk]
        out[row_idx][0] = 5
        out[row_idx][width - 1] = 5
        for jj in range(inner_len):
            out[row_idx][1 + jj] = transformed[jj]
    return out
```