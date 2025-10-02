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

def find_left_right(g: List[List[int]], top: int, bottom: int) -> Tuple[int, int]:
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
    row_top = g[top]
    row_bot = g[bottom]
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
    mappings: Dict[int, int] = {}
    n = len(g[0]) if g else 0
    for i in range(top + 1):
        row = g[i]
        j = 0
        while j < n:
            color = row[j]
            if color == 5 or color == bg:
                while j < n and row[j] == color:
                    j += 1
                continue
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
            if color not in mappings:
                mappings[color] = next_color
    return mappings

def get_outline_mask(l: int) -> List[bool]:
    if l <= 2:
        return [True] * l
    mask = [False] * l
    mask[0] = True
    mask[l - 1] = True
    return mask

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    top, bottom = find_top_bottom(g)
    left, right = find_left_right(g, top, bottom)
    w_frame = right - left + 1
    bg = find_background(g, top, bottom, left, right)
    mappings = extract_mappings(g, top, bg)
    # Get input inner rows
    inner_w = right - left - 1
    inner_g = [g[i][left + 1 : right] for i in range(top + 1, bottom)]
    # Find stacks
    stacks = []
    i = 0
    h_inner = len(inner_g)
    while i < h_inner:
        curr = inner_g[i]
        start = i
        while i < h_inner and inner_g[i] == curr:
            i += 1
        h = i - start
        stacks.append((curr, h))
    # Build output inner rows
    output_inner: List[List[int]] = []
    i_stack = 0
    while i_stack < len(stacks):
        row_pattern, h = stacks[i_stack]
        is_full_bg = all(x == bg for x in row_pattern)
        if is_full_bg:
            output_inner.append([bg] * inner_w)
            i_stack += 1
            continue
        # Pattern stack, compute runs once
        runs = []
        j = 0
        n = inner_w
        while j < n:
            col = row_pattern[j]
            startj = j
            while j < n and row_pattern[j] == col:
                j += 1
            ln = j - startj
            if col == bg:
                runs.append((bg, ln))
            else:
                mapped_c = mappings.get(col, col)
                runs.append((mapped_c, ln, col))  # mapped, ln, orig
        # Generate h rows
        for k in range(h):
            out_row = []
            is_outline = (k == 0 and h > 1)
            for r in runs:
                if len(r) == 2:  # bg
                    c, ln = r
                    out_row.extend([c] * ln)
                else:  # object
                    mapped, ln, orig = r
                    if is_outline:
                        mask = get_outline_mask(ln)
                    else:
                        mask = [True] * ln
                    for fill in mask:
                        out_row.append(mapped if fill else bg)
            output_inner.append(out_row)
        i_stack += 1
        # Insert full bg if next is pattern
        if i_stack < len(stacks):
            next_pattern, _ = stacks[i_stack]
            if not all(x == bg for x in next_pattern):
                output_inner.append([bg] * inner_w)
    # Build full output
    out: List[List[int]] = []
    out.append([5] * w_frame)
    for inner_out in output_inner:
        out.append([5] + inner_out + [5])
    out.append([5] * w_frame)
    return out
```