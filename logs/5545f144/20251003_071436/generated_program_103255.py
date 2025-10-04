```python
from typing import List
from collections import Counter

def get_bg(g: List[List[int]]) -> int:
    """Get the background color as the most common value in the grid."""
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_divider_positions(w: int, k: int) -> List[int]:
    """Compute divider column positions for given w and k."""
    divs = []
    current = w
    for _ in range(k - 1):
        divs.append(current)
        current += w + 1
    return divs

def find_valid_configuration(g: List[List[int]], bg: int) -> tuple:
    """Find the valid configuration with maximal k where dividers are constant non-bg."""
    h = len(g)
    if h == 0:
        return None
    w_in = len(g[0])
    n = w_in + 1
    possible_ds = []
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            possible_ds.append(i)
            if i != n // i:
                possible_ds.append(n // i)
    possible_ds = list(set(possible_ds))
    possible_ds.sort(reverse=True)
    valid_configs = []
    for d in possible_ds:
        if d < 2:
            continue
        k = n // d
        ww = d - 1
        divs = get_divider_positions(ww, k)
        if not divs or divs[-1] >= w_in:
            continue
        # Check first divider
        col0 = divs[0]
        col_vals = [g[r][col0] for r in range(h)]
        if len(set(col_vals)) != 1:
            continue
        dd = col_vals[0]
        if dd == bg:
            continue
        # Check other dividers
        is_valid = True
        for col in divs[1:]:
            col_vals = [g[r][col] for r in range(h)]
            if set(col_vals) != {dd}:
                is_valid = False
                break
        if is_valid:
            valid_configs.append((k, ww, divs, dd))
    if not valid_configs:
        return None
    # Maximal k, then maximal ww
    valid_configs.sort(key=lambda x: (-x[0], -x[1]))
    return valid_configs[0]

def get_fg(g: List[List[int]], bg: int, d: int) -> int:
    """Get the foreground color, the remaining unique color."""
    flat = [cell for row in g for cell in row]
    colors = set(flat) - {bg, d}
    return list(colors)[0] if colors else bg

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to solve the puzzle."""
    h = len(g)
    if h == 0:
        return []
    w_in = len(g[0])
    bg = get_bg(g)
    config = find_valid_configuration(g, bg)
    if config is None:
        # No valid folding, return uniform background
        return [[bg for _ in range(w_in)] for _ in range(h)]
    k, w, divs, d = config
    fg = get_fg(g, bg, d)
    # Panel starts
    panel_starts = [0]
    for dd_pos in divs:
        panel_starts.append(dd_pos + 1)
    # Extract panels
    panels = []
    for start in panel_starts:
        pan = [[g[r][start + j] for j in range(w)] for r in range(h)]
        panels.append(pan)
    # Find all base positions
    base_pos = []
    for r in range(h):
        for c in range(w):
            if all(pan[r][c] == fg for pan in panels):
                base_pos.append((r, c))
    if not base_pos:
        return [[bg for _ in range(w)] for _ in range(h)]
    # Minimal r_base
    r_base = min(r for r, _ in base_pos)
    c_bases = [c for r, c in base_pos if r == r_base]
    span_end = r_base + k
    # Initialize output
    out = [[bg for _ in range(w)] for _ in range(h)]
    # Set bases within span
    for r, c in base_pos:
        if r <= span_end and r < h:
            out[r][c] = fg
    # Propagation from c_bases at r_base
    for c_base in c_bases:
        if k == 2:
            # Straight
            straight_r = r_base + 1
            if straight_r < h:
                out[straight_r][c_base] = fg
            # Branch
            branch_r = r_base + 2
            if branch_r < h:
                for off in [-1, 1]:
                    cc = c_base + off
                    if 0 <= cc < w:
                        out[branch_r][cc] = fg
        else:
            # Branch
            branch_r = r_base + 1
            if branch_r < h:
                offsets = [-1, 1]
                if k % 2 == 0:
                    offsets.append(0)
                for off in offsets:
                    cc = c_base + off
                    if 0 <= cc < w:
                        out[branch_r][cc] = fg
    return out
```