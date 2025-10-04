```python
from collections import Counter
from typing import List

def transform_line(line: List[int], bg: int, is_vertical: bool) -> List[int]:
    n = len(line)
    res = line.copy()
    i = 0
    while i < n:
        if res[i] == 2 and is_vertical:
            start_two = i
            i += 1
            while i < n and res[i] == 2:
                i += 1
            end_two = i
            s = end_two - start_two
            if end_two < n and res[end_two] == bg:
                start_gap = end_two
                j = end_two + 1
                while j < n and res[j] == bg:
                    j += 1
                end_gap = j
                g = end_gap - start_gap
                if end_gap < n and res[end_gap] != bg and res[end_gap] != 2 and res[end_gap] != 0:
                    obs_start = end_gap
                    k = end_gap + 1
                    while k < n and res[k] != bg and res[k] != 0 and res[k] != 2:
                        k += 1
                    obs_len = k - obs_start
                    if g > s and obs_len >= 2:
                        place_start = start_gap + g - s
                        res[place_start:end_gap] = [2] * s
                        res[start_gap:place_start] = [0] * (g - s)
                        res[start_two:end_two] = [0] * s
                i = end_gap
            else:
                i = end_two
            continue
        if res[i] == bg or res[i] == 0:
            i += 1
            continue
        start_obs = i
        i += 1
        while i < n and res[i] != bg and res[i] != 0 and res[i] != 2:
            i += 1
        end_obs = i
        obs_len = end_obs - start_obs
        if i >= n or res[i] != bg:
            continue
        start_gap = i
        i += 1
        while i < n and res[i] == bg:
            i += 1
        end_gap = i
        g = end_gap - start_gap
        if i >= n or res[i] != 2:
            continue
        start_two = i
        i += 1
        while i < n and res[i] == 2:
            i += 1
        end_two = i
        s = end_two - start_two
        if obs_len < 2 or g <= s:
            continue
        res[start_gap:start_gap + s] = [2] * s
        zero_start = start_gap + s
        zero_end = end_two
        res[zero_start:zero_end] = [0] * (zero_end - zero_start)
        extra_start = end_two
        extra_num = s - 1
        if extra_num > 0 and extra_start < n and res[extra_start] == bg:
            extra_end = min(n, extra_start + extra_num)
            res[extra_start:extra_end] = [0] * (extra_end - extra_start)
    return res

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    flat = [cell for row in g for cell in row]
    bg = Counter(flat).most_common(1)[0][0]
    grid = [row[:] for row in g]
    # Horizontal transformations (after only)
    for r in range(rows):
        grid[r] = transform_line(grid[r], bg, is_vertical=False)
    # Vertical transformations (both)
    for c in range(cols):
        col = [grid[r][c] for r in range(rows)]
        new_col = transform_line(col, bg, is_vertical=True)
        for r in range(rows):
            grid[r][c] = new_col[r]
    # Erase remaining original 2's to bg
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2 and g[r][c] == 2:
                grid[r][c] = bg
    return grid
```