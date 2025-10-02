```python
from typing import List

def is_solid(grid: List[List[int]], i: int, j: int, c: int) -> bool:
    for r in range(4):
        for cc in range(4):
            if grid[i + r][j + cc] != c:
                return False
    return True

def is_h(grid: List[List[int]], i: int, j: int, c: int) -> bool:
    for r in range(4):
        row = grid[i + r][j:j + 4]
        if r == 0 or r == 3:
            if row != [c, c, c, c]:
                return False
        elif r == 1 or r == 2:
            if row != [c, 0, 0, c]:
                return False
    return True

def extract_pattern(grid: List[List[int]], i: int, j: int) -> List[List[int]]:
    pattern = []
    for r in range(4):
        pattern.append(grid[i + r][j:j + 4])
    return pattern

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    h_list = []
    s_list = []
    for i in range(rows - 3):
        for j in range(cols - 3):
            sub = [g[i + r][j:j + 4] for r in range(4)]
            colors = set(val for row in sub for val in row if val != 0)
            if len(colors) == 1:
                c = next(iter(colors))
                if is_solid(g, i, j, c):
                    pattern = extract_pattern(g, i, j)
                    s_list.append((i, j, c, pattern))
                elif is_h(g, i, j, c):
                    pattern = extract_pattern(g, i, j)
                    h_list.append((i, j, c, pattern))
    h_sorted = sorted(h_list, key=lambda x: (x[0], x[1]))
    s_sorted = sorted(s_list, key=lambda x: (x[0], x[1]))
    num_h = len(h_sorted)
    num_s = len(s_sorted)
    num_blocks = max(num_h, num_s)
    output_rows = []
    empty_pat = [[0, 0, 0, 0] for _ in range(4)]
    for b in range(num_blocks):
        if b < num_h and b < num_s:
            left_pat = h_sorted[b][3]
            right_pat = s_sorted[b][3]
        elif b < num_h:
            left_pat = h_sorted[b][3]
            right_pat = empty_pat
        else:
            left_pat = empty_pat
            right_pat = s_sorted[b][3]
        for r in range(4):
            out_row = left_pat[r] + right_pat[r]
            output_rows.append(out_row)
    return output_rows
```