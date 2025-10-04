```python
from math import gcd
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    num_rows = len(g)
    num_cols = len(g[0]) if num_rows > 0 else 0
    output = [row[:] for row in g]
    if num_rows > num_cols:
        # Horizontal mode: process each row from left
        for i in range(num_rows):
            row = output[i]
            if row[0] == 0:
                continue
            c = row[0]
            positions = [j for j in range(num_cols) if g[i][j] == c]
            if len(positions) <= 1:
                continue
            d = positions[0]
            for p in positions[1:]:
                d = gcd(d, p)
            if d == 0:
                continue
            r = positions[0] % d
            candidates = [k for k in range(num_cols) if k % d == r]
            pos_to_color: dict[int, int] = {}
            group_colors = []
            for k in candidates:
                colr = g[i][k]
                if colr != 0:
                    group_colors.append(colr)
                    pos_to_color[k] = colr
            if not group_colors:
                continue
            is_same = all(gc == c for gc in group_colors)
            fill_color = c
            max_pos = -1
            if not is_same:
                max_pos = max(pos_to_color.keys())
                fill_color = pos_to_color[max_pos]
            to_fill = candidates if is_same else [k for k in candidates if k <= max_pos]
            for k in to_fill:
                output[i][k] = fill_color
    else:
        # Vertical mode: process each column from bottom
        for j in range(num_cols):
            if g[num_rows - 1][j] == 0:
                continue
            c = g[num_rows - 1][j]
            positions = []
            for ii in range(num_rows):
                if g[ii][j] == c:
                    p = num_rows - 1 - ii
                    positions.append(p)
            if len(positions) <= 1:
                continue
            d = positions[0]
            for p in positions[1:]:
                d = gcd(d, p)
            if d == 0:
                continue
            r = positions[0] % d
            max_p = num_rows - 1
            candidates_p = [p for p in range(max_p + 1) if p % d == r]
            pos_to_color: dict[int, int] = {}
            group_colors = []
            for p in candidates_p:
                ii = num_rows - 1 - p
                colr = g[ii][j]
                if colr != 0:
                    group_colors.append(colr)
                    pos_to_color[p] = colr
            if not group_colors:
                continue
            is_same = all(gc == c for gc in group_colors)
            fill_color = c
            max_pos = -1
            if not is_same:
                max_pos = max(pos_to_color.keys())
                fill_color = pos_to_color[max_pos]
            to_fill_p = candidates_p if is_same else [p for p in candidates_p if p <= max_pos]
            for p in to_fill_p:
                ii = num_rows - 1 - p
                output[ii][j] = fill_color
    return output
```