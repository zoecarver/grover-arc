```python
from typing import List
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    flat = [g[i][j] for i in range(len(g)) for j in range(len(g[0]))]
    counts = Counter(flat)
    return counts.most_common(1)[0][0]

def find_divider_color(g: List[List[int]], bg: int) -> int:
    h = len(g)
    w = len(g[0])
    col_colors = []
    for j in range(w):
        col_flat = [g[i][j] for i in range(h)]
        if len(set(col_flat)) == 1 and col_flat[0] != bg:
            col_colors.append(col_flat[0])
    if col_colors:
        return Counter(col_colors).most_common(1)[0][0]
    return -1

def find_divider_cols(g: List[List[int]], divider_color: int) -> List[int]:
    if divider_color == -1:
        return []
    h = len(g)
    w = len(g[0])
    cols = []
    for j in range(w):
        if all(g[i][j] == divider_color for i in range(h)):
            cols.append(j)
    return cols

def compute_panel_width(w: int, divider_cols: List[int]) -> int:
    num_div = len(divider_cols)
    num_panels = num_div + 1
    total_panel = w - num_div
    return total_panel // num_panels

def extract_left_panel(g: List[List[int]], divider_cols: List[int], panel_width: int) -> List[List[int]]:
    h = len(g)
    first_div = divider_cols[0] if divider_cols else len(g[0])
    left_w = min(first_div, panel_width)
    left_g = [[g[i][j] for j in range(left_w)] for i in range(h)]
    # Pad if necessary
    for row in left_g:
        while len(row) < panel_width:
            row.append(left_g[0][0] if left_g else 0)  # pad with bg, but bg not known yet
    return left_g

def pack_row(row: List[int], fg: int, threshold: int = 3) -> List[int]:
    positions = [j for j in range(len(row)) if row[j] == fg]
    if not positions:
        return row
    if len(positions) == 1:
        return row  # keep single in place
    p1 = positions[0]
    span = positions[-1] - p1
    new_row = [row[k] if k not in positions else 0 for k in range(len(row))]  # temp remove
    if span > threshold:
        new_row[p1] = fg  # keep leftmost
    else:
        for p in positions:
            new_p = p - p1
            new_row[new_p] = fg
    return new_row

def find_clusters(g: List[List[int]], fg: int) -> List[tuple]:
    h = len(g)
    clusters = []
    i = 0
    while i < h:
        if any(g[i][j] == fg for j in range(len(g[i]))):
            start = i
            total = sum(1 for j in range(len(g[i])) if g[i][j] == fg)
            i += 1
            while i < h and any(g[i][j] == fg for j in range(len(g[i]))):
                total += sum(1 for j in range(len(g[i])) if g[i][j] == fg)
                i += 1
            if total >= 4:
                clusters.append((start, i - 1, total))
        else:
            i += 1
    return clusters  # only first cluster for top

def apply_cluster_adjust(out: List[List[int]], g: List[List[int]], fg: int, panel_width: int):
    # Only process the top cluster
    clusters = find_clusters(g, fg)
    if not clusters:
        return out
    # Take the first (top) cluster
    start, end, _ = clusters[0]
    for r in range(start, end + 1):
        if r < len(out):
            out[r] = pack_row(out[r], fg)
    # Remove lower clusters by setting to bg
    for r in range(len(out)):
        has_fg = any(out[r][j] == fg for j in range(panel_width))
        if has_fg and r < start or r > end:
            out[r] = [0] * panel_width  # temp bg
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    bg = find_background(g)
    divider_color = find_divider_color(g, bg)
    divider_cols = find_divider_cols(g, divider_color)
    h = len(g)
    w = len(g[0])
    panel_width = compute_panel_width(w, divider_cols)
    left_g = extract_left_panel(g, divider_cols, panel_width)
    # Find fg
    flat = [g[i][j] for i in range(h) for j in range(w)]
    counts = Counter(flat)
    fg_candidates = [k for k, v in counts.items() if k != bg and k != divider_color and v > 0]
    fg = fg_candidates[0] if fg_candidates else bg
    # Replace pad with bg
    for row in left_g:
        row[:] = [bg if x == 0 else x for x in row]
    # Apply cluster adjust using left_g as g for cluster
    out = apply_cluster_adjust(left_g, left_g, fg, panel_width)
    return out
```