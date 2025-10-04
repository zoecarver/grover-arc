```python
from typing import List

def find_label_column(header: List[int]) -> int:
    return header.index(0)

def should_reverse(orig_w: int, label_col: int) -> bool:
    return label_col > (orig_w - 1) / 2

def remove_label_column(content: List[List[int]], label_col: int) -> List[List[int]]:
    return [row[:label_col] + row[label_col + 1:] for row in content]

def reverse_if_needed(content: List[List[int]], reverse: bool) -> List[List[int]]:
    if not reverse:
        return content
    return [row[::-1] for row in content]

def get_grid_width(content: List[List[int]]) -> int:
    return len(content[0]) if content and content[0] else 0

def is_wide_mode(width: int) -> bool:
    return width > 7

def get_max_horizontal_run(grid: List[List[int]]) -> int:
    max_r = 0
    for row in grid:
        j = 0
        n = len(row)
        while j < n:
            if row[j] == 8:
                j += 1
                continue
            c = row[j]
            start = j
            j += 1
            while j < n and row[j] == c:
                j += 1
            max_r = max(max_r, j - start)
    return max_r

def extract_horizontal_runs(row: List[int], min_len: int = 2) -> List[tuple[int, int]]:
    runs = []
    j = 0
    n = len(row)
    while j < n:
        if row[j] == 8:
            j += 1
            continue
        c = row[j]
        start = j
        j += 1
        while j < n and row[j] == c:
            j += 1
        length = j - start
        if length >= min_len:
            runs.append((c, length))
    return runs

def render_bar(c: int, length: int, max_w: int) -> List[int]:
    if length == max_w:
        return [c] * max_w
    pad_l = (max_w - length) // 2
    pad_r = max_w - length - pad_l
    return [8] * pad_l + [c] * length + [8] * pad_r

def process_wide_mode(content: List[List[int]]) -> List[List[int]]:
    max_w = get_max_horizontal_run(content)
    if max_w == 0:
        return []
    out = []
    i = 0
    h = len(content)
    while i < h:
        row = content[i]
        if all(x == 8 for x in row):
            i += 1
            continue
        start = i
        i += 1
        while i < h and content[i] == row:
            i += 1
        group_h = i - start
        runs = extract_horizontal_runs(row)
        for c, length in runs:
            bar = render_bar(c, length, max_w)
            for _ in range(group_h):
                out.append(bar)
    return out

def pad_sequence(seq: List[int], max_w: int) -> List[int]:
    ln = len(seq)
    if ln == max_w:
        return seq[:]
    pad_l = (max_w - ln) // 2
    pad_r = max_w - ln - pad_l
    return [8] * pad_l + seq + [8] * pad_r

def process_band(grid: List[List[int]], l_col: int, r_col: int, max_w: int) -> List[List[int]]:
    out = []
    i = 0
    h = len(grid)
    while i < h:
        if grid[i][l_col] == 8 and grid[i][r_col] == 8:
            i += 1
            continue
        start = i
        i += 1
        while i < h and not (grid[i][l_col] == 8 and grid[i][r_col] == 8):
            i += 1
        group_h = i - start
        seq_r = [grid[start + j][r_col] for j in range(group_h)]
        rendered_r = pad_sequence(seq_r, max_w)
        out.append(rendered_r)
        seq_l = [grid[start + j][l_col] for j in range(group_h)]
        rendered_l = pad_sequence(seq_l, max_w)
        out.append(rendered_l)
    return out

def process_tall_mode(content: List[List[int]]) -> List[List[int]]:
    max_w = 6
    left_out = process_band(content, 1, 2, max_w)
    right_out = process_band(content, 4, 5, max_w)
    return left_out + right_out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    header = g[0]
    label_col = find_label_column(header)
    orig_w = len(header)
    reverse = should_reverse(orig_w, label_col)
    content = [row for row in g[1:]]
    content = remove_label_column(content, label_col)
    content = reverse_if_needed(content, reverse)
    width = get_grid_width(content)
    if is_wide_mode(width):
        return process_wide_mode(content)
    else:
        return process_tall_mode(content)
```