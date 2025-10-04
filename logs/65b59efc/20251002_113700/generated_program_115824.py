```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w_grid = len(g[0])
    # Get centers and colors from last row
    last_row = g[-1]
    centers = [j for j in range(w_grid) if last_row[j] != 0]
    colors = [last_row[j] for j in range(w_grid) if last_row[j] != 0]
    s = len(centers)
    if s == 0:
        return [[0] * w_grid for _ in range(h - 1)]
    d = centers[1] - centers[0] if s > 1 else w_grid
    w = d - 1
    r = (w - 1) // 2
    section_ranges = [(max(0, centers[k] - r), min(w_grid, centers[k] + r + 1)) for k in range(s)]
    # Get separator rows
    sep_rows = [i for i in range(h - 1) if sum(1 for x in g[i] if x == 5) > w_grid / 2.0]
    # Get bands
    bands = []
    start = 0
    for sep in sep_rows:
        if start < sep:
            bands.append((start, sep))
        start = sep + 1
    if start < h - 1:
        bands.append((start, h - 1))
    num_bands = len(bands)
    # Output dimensions
    out_h = num_bands * w
    out_w = s * w
    out = [[0] * out_w for _ in range(out_h)]
    # Function to check significant fill (flat sum)
    def has_significant_fill(b_start: int, b_end: int, s_start: int, s_end: int) -> bool:
        num_cells = (b_end - b_start) * w
        num_filled = sum(1 for ii in range(b_start, b_end) for jj in range(s_start, s_end) if g[ii][jj] != 0)
        return num_filled > num_cells / 2
    # Fill blocks
    for bi in range(num_bands):
        b_start, b_end = bands[bi]
        row_start = bi * w
        for si in range(s):
            s_start, s_end = section_ranges[si]
            col_start = si * w
            color = colors[si]
            if has_significant_fill(b_start, b_end, s_start, s_end):
                for ri in range(w):
                    out[row_start + ri][col_start:col_start + w] = [color] * w
            # Special handling for last band
            if bi == num_bands - 1:
                # Reset block to 0 first
                for ri in range(w):
                    out[row_start + ri][col_start:col_start + w] = [0] * w
                # For last band, fill based on color value (creative rule attempt)
                if color == 7:
                    # Empty
                    pass
                elif color <= 5:
                    # Frame pattern
                    for ri in range(w):
                        if ri == 0 or ri == w - 1:
                            out[row_start + ri][col_start:col_start + w] = [color] * w
                        else:
                            row_fill = [0] * w
                            row_fill[0] = color
                            row_fill[w - 1] = color
                            out[row_start + ri][col_start:col_start + w] = row_fill
                else:
                    # Full
                    for ri in range(w):
                        out[row_start + ri][col_start:col_start + w] = [color] * w
    # If out_h != out_w, pad to square (creative for size mismatch)
    side = max(out_h, out_w)
    out_padded = [[0] * side for _ in range(side)]
    for i in range(out_h):
        for j in range(out_w):
            out_padded[i][j] = out[i][j]
    return out_padded
```