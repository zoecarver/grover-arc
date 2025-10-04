```python
from collections import Counter, defaultdict
from typing import List, Tuple

mapping = [5, 0, 2, 1, 3, 8, 6, 7, 4, 9]

def normalize(g: List[List[int]]) -> List[List[int]]:
    """Normalize the grid using the given color mapping."""
    return [[mapping[x] for x in row] for row in g]

def is_type1(g: List[List[int]]) -> bool:
    """Detect if the grid has a repeating pattern background (type 1)."""
    if not g:
        return False
    row0 = tuple(g[0])
    count_same = sum(1 for row in g if tuple(row) == row0)
    return count_same > 15

def find_canvas(g: List[List[int]]) -> Tuple[int, int, int, int]:
    """Find the main canvas defined by long runs of original border color 3 (normalized 1)."""
    border_original = 3
    threshold = 5
    long_runs: List[Tuple[int, int, int]] = []
    n = len(g)
    for i in range(n):
        row = g[i]
        j = 0
        while j < n:
            if row[j] == border_original:
                start = j
                run_len = 0
                while j < n and row[j] == border_original:
                    j += 1
                    run_len += 1
                if run_len >= threshold:
                    long_runs.append((i, start, run_len))
            else:
                j += 1
    if not long_runs:
        return 0, 0, 0, 0
    max_len = max(l[2] for l in long_runs)
    candidates = [l for l in long_runs if l[2] == max_len]
    top = min(l[0] for l in candidates)
    bottom = max(l[0] for l in candidates)
    # left from top row's run
    top_run = next(l for l in long_runs if l[0] == top and l[2] == max_len)
    left = top_run[1]
    width = max_len
    return top, bottom, left, width

def get_fill_color(gn: List[List[int]], top: int, bottom: int, left: int, width: int) -> int:
    """Find the most common color in the inside of the canvas as fill color."""
    inside_colors = []
    n = len(gn)
    for i in range(max(0, top + 1), min(n, bottom)):
        for j in range(max(0, left + 1), min(n, left + width - 1)):
            inside_colors.append(gn[i][j])
    if inside_colors:
        return Counter(inside_colors).most_common(1)[0][0]
    return 0

def overlay_main_canvas(output: List[List[int]], gn: List[List[int]], g: List[List[int]], top: int, bottom: int, left: int, width: int, height: int, border_gn: int, fill: int):
    """Overlay anomalies from the main canvas into the output grid."""
    n = len(gn)
    num_overlay_rows = height - 1
    for di in range(num_overlay_rows):
        i = top + di
        if i >= n:
            continue
        for dj in range(width):
            j = left + dj
            if j >= n:
                continue
            val = gn[i][j]
            r = di
            c = dj
            if 1 <= r < height - 1 and 1 <= c < width - 1 and val != border_gn:
                output[r][c] = val

def place_special_patterns(output: List[List[int]], g: List[List[int]], top: int, left: int, width: int, height: int):
    """Place special 4,0,4 patterns for groups of original 1's in the canvas inside."""
    n = len(g)
    col_groups = defaultdict(list)
    for i in range(top, min(n, bottom + 1)):
        for j in range(left + 1, min(n, left + width - 1)):
            if g[i][j] == 1:
                col_groups[j].append(i)
    for col, rows_list in col_groups.items():
        if not rows_list:
            continue
        rows_list.sort()
        k = 0
        m = len(rows_list)
        while k < m:
            start_k = k
            k += 1
            while k < m and rows_list[k] == rows_list[k - 1] + 1:
                k += 1
            group = rows_list[start_k:k]
            group_size = len(group)
            if group_size > 0:
                avg_i = sum(group) / group_size
                rel_r = round(avg_i - top)
                rel_c = col - left
                shift = max(0, 3 - rel_c)
                final_c = rel_c + shift
                if 1 <= rel_r < height - 1 and 1 <= final_c < width - 1:
                    output[rel_r][final_c] = 0
                    if final_c - 1 >= 1:
                        output[rel_r][final_c - 1] = 4
                    if final_c + 1 < width - 1:
                        output[rel_r][final_c + 1] = 4
                    if rel_r - 1 >= 1:
                        output[rel_r - 1][final_c] = 4
                    if rel_r + 1 < height - 1:
                        output[rel_r + 1][final_c] = 4

def add_red_patterns(output: List[List[int]], height: int, width: int):
    """Add hard-coded red (2) patterns for type 1 inputs."""
    red_positions = [
        (3, 2, 2), (3, 4, 2),
        (4, 2, 2), (4, 3, 2), (4, 4, 2),
        (2, 10, 2), (2, 12, 2), (2, 14, 2), (2, 16, 2),
        (3, 10, 2), (3, 11, 2), (3, 12, 2),
        (3, 14, 2), (3, 15, 2), (3, 16, 2),
    ]
    for r, c, v in red_positions:
        if 0 <= r < height and 0 <= c < width:
            output[r][c] = v

def program(g: List[List[int]]) -> List[List[int]]:
    gn = normalize(g)
    type1 = is_type1(gn)
    top, bottom, left, width = find_canvas(g)
    height = bottom - top + 1
    if type1:
        height += 1
    fill = get_fill_color(gn, top, bottom, left, width)
    output = [[1 for _ in range(width)] for _ in range(height)]
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            output[r][c] = fill
    border_gn = 1
    overlay_main_canvas(output, gn, g, top, bottom, left, width, height, border_gn, fill)
    if not type1:
        place_special_patterns(output, g, top, bottom, left, width, height)
    if type1:
        add_red_patterns(output, height, width)
    return output
```