```python
from typing import List
import collections

def find_three_border(g: List[List[int]]) -> tuple:
    n = len(g)
    if n == 0:
        return -1, -1, -1, 0
    m = len(g[0])
    max_h = 0
    best_l = best_r = best_start = -1
    for l in range(m):
        for r in range(l + 2, m):
            current_h = 0
            curr_start = -1
            for row in range(n):
                if g[row][l] == 3 and g[row][r] == 3:
                    if current_h == 0:
                        curr_start = row
                    current_h += 1
                    if current_h > max_h:
                        max_h = current_h
                        best_l = l
                        best_r = r
                        best_start = curr_start
                else:
                    current_h = 0
    if max_h < 3:
        return -1, -1, -1, 0
    return best_l, best_r, best_start, max_h

def compute_fill(g: List[List[int]], l: int, r: int, start: int, h: int) -> int:
    counter = collections.Counter()
    for i in range(h):
        row = g[start + i]
        for c in range(l + 1, r):
            color = row[c]
            if color != 3:
                counter[color] += 1
    if counter:
        return counter.most_common(1)[0][0]
    return 0

def build_output_row(width: int, is_border_row: bool, is_side: bool, fill_color: int, g_row: List[int], l: int) -> List[int]:
    row_out = []
    for j in range(width):
        if is_border_row or j == 0 or j == width - 1:
            row_out.append(3)
        else:
            c = l + j
            color = g_row[c]
            row_out.append(fill_color if color == 3 else color)
    return row_out

def complete_frame(g: List[List[int]], l: int, r: int, start: int, h: int, f: int) -> List[List[int]]:
    width = r - l + 1
    output = []
    for i in range(h):
        input_row = start + i
        g_row = g[input_row]
        is_border_row = (i == 0 or i == h - 1)
        row_out = build_output_row(width, is_border_row, False, f, g_row, l)
        # Check if inner was uniform 3's (pre-replacement)
        if 0 < i < h - 1:
            inner_uniform = all(g_row[l + j] == 3 for j in range(1, width - 1))
            if inner_uniform:
                for j in range(1, width - 1):
                    row_out[j] = f
        output.append(row_out)
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    l, r, start, h = find_three_border(g)
    if h == 0:
        return []
    f = compute_fill(g, l, r, start, h)
    return complete_frame(g, l, r, start, h, f)
```