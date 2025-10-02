```python
from typing import List, Tuple
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

def extract_pairs(g: List[List[int]], top: int, bg: int) -> List[Tuple[int, int]]:
    pairs = []
    for i in range(top):
        row = g[i]
        j = 0
        n = len(row)
        while j < n:
            while j < n and (row[j] == bg or row[j] == 5):
                j += 1
            if j >= n:
                break
            color = row[j]
            run_start = j
            while j < n and row[j] == color:
                j += 1
            run_len = j - run_start
            if run_len < 2 or color == bg or color == 5:
                continue
            if j >= n:
                break
            next_color = row[j]
            next_start = j
            while j < n and row[j] == next_color:
                j += 1
            next_len = j - next_start
            if next_len < 2 or next_color == bg or next_color == 5 or color == next_color:
                continue
            pairs.append((color, next_color))
    return pairs

def get_mappings(pairs: List[Tuple[int, int]]) -> Dict[int, int]:
    from_set = set(f for f, _ in pairs)
    to_set = set(t for _, t in pairs)
    froms = sorted(from_set)
    tos = sorted(to_set)
    if len(pairs) == 2:
        tos = sorted(to_set, reverse=True)
    return dict(zip(froms, tos))

def transform_row(inner_row: List[int], mappings: Dict[int, int], bg: int) -> List[int]:
    out = []
    j = 0
    m = len(inner_row)
    while j < m:
        val = inner_row[j]
        run_start = j
        while j < m and inner_row[j] == val:
            j += 1
        l = j - run_start
        if val == 5:
            out.extend([5] * l)
            continue
        if val == bg:
            out.extend([bg] * l)
            continue
        mapped_c = mappings.get(val, val)
        if l < 2:
            out.extend([mapped_c] * l)
            continue
        # thin to sides
        out.append(mapped_c)
        out.extend([bg] * (l - 2))
        out.append(mapped_c)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    top, bottom = find_top_bottom(g)
    left, right = find_left_right(g, top, bottom)
    w = right - left + 1
    bg = find_background(g, top, bottom, left, right)
    pairs = extract_pairs(g, top, bg)
    mappings = get_mappings(pairs)
    out = []
    # top full 5
    out.append([5] * w)
    # inner rows from top+1 to bottom-1
    for ii in range(top + 1, bottom):
        inner_row = g[ii][left + 1 : right]
        transformed_inner = transform_row(inner_row, mappings, bg)
        row_out = [5] + transformed_inner + [5]
        out.append(row_out)
    # bottom full 5
    out.append([5] * w)
    return out
```