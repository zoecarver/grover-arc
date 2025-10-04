```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    height = len(g)
    width = len(g[0])
    out = [[0] * width for _ in range(height)]
    # Place pinks and local 8's in data rows
    for ii in range(1, height, 2):
        if ii >= height:
            break
        row = g[ii]
        j = 0
        while j < width - 2:
            if row[j] == 7 and row[j + 1] == 7 and row[j + 2] == 7:
                c = j + 1
                out[ii][j] = 8
                out[ii][c] = 6
                out[ii][j + 2] = 8
                if ii - 1 >= 0:
                    out[ii - 1][c] = 6
                if ii + 1 < height:
                    out[ii + 1][c] = 6
                j += 3
            else:
                j += 1
    # Fill frame rows (even i) and place 3's
    for i in range(0, height, 2):
        row_in = g[i]
        has_gap = any(row_in[j] == 0 for j in range(width))
        # Fill
        for j in range(width):
            if out[i][j] == 0:
                if row_in[j] == 0:
                    out[i][j] = 0
                else:
                    out[i][j] = 8
        # Place 3's
        if i == 0:
            continue
        if not has_gap:
            if i == height - 1:
                # bottom no gap
                if out[i][0] == 8:
                    out[i][0] = 3
                if out[i][width - 1] == 8:
                    out[i][width - 1] = 3
            else:
                # internal no gap
                pink_positions = [j for j in range(width) if out[i][j] == 6]
                if pink_positions:
                    first_c = min(pink_positions)
                    p = first_c - 1
                    if p >= 0 and out[i][p] == 8 and i > 0 and out[i - 1][p] == 8 and p + 1 < width and out[i - 1][p + 1] == 6:
                        if out[i][0] == 8:
                            out[i][0] = 3
                        if 1 < width and out[i][1] == 8:
                            out[i][1] = 3
                    last_c = max(pink_positions)
                    q = last_c + 1
                    if q < width and out[i][q] == 8 and i > 0 and out[i - 1][q] == 8 and q - 1 >= 0 and out[i - 1][q - 1] == 6:
                        if out[i][width - 1] == 8:
                            out[i][width - 1] = 3
                        if width > 1 and out[i][width - 2] == 8:
                            out[i][width - 2] = 3
        else:
            # has gap
            if i == height - 1:
                # bottom with gap
                for j in range(width - 1):
                    if row_in[j] == 0 and out[i][j] == 0 and out[i][j + 1] == 8:
                        out[i][j + 1] = 3
                if out[i][width - 1] == 8:
                    out[i][width - 1] = 3
            else:
                # internal with gap
                if row_in[0] == 3 and out[i][0] == 8:
                    out[i][0] = 3
                if row_in[width - 1] == 3 and out[i][width - 1] == 8:
                    out[i][width - 1] = 3
                for j in range(1, width):
                    if row_in[j] == 0 and out[i][j] == 0 and out[i][j - 1] == 8:
                        out[i][j - 1] = 3
    return out
```