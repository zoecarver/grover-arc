```python
from collections import Counter
from typing import List

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_separator_columns(g: List[List[int]], bg: int) -> List[int]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    seps = []
    for j in range(w):
        col = [g[i][j] for i in range(h)]
        if len(set(col)) == 1 and col[0] != bg:
            seps.append(j)
    return sorted(seps)

def get_divider_color(g: List[List[int]], seps: List[int], bg: int) -> int:
    if not seps:
        return None
    col_samples = [g[0][j] for j in seps]
    return Counter(col_samples).most_common(1)[0][0]

def get_foreground_color(g: List[List[int]], bg: int, d: int) -> int:
    flat = [cell for row in g for cell in row]
    non_bg_d = [cell for cell in flat if cell != bg and cell != d]
    if not non_bg_d:
        return bg
    return Counter(non_bg_d).most_common(1)[0][0]

def get_panel_starts(seps: List[int], w: int, w_panel: int, k: int) -> List[int]:
    starts = [0]
    current = 0
    for i in range(k - 1):
        current = seps[i] + 1
        starts.append(current)
    return starts

def find_bases(g: List[List[int]], starts: List[int], k: int, h: int, w_panel: int, fg: int, bg: int) -> List[tuple]:
    bases = []
    for r in range(h):
        for c in range(w_panel):
            is_common = all(
                j := starts[p] + c < len(g[0]) and g[r][j] == fg
                for p in range(k)
            )
            if not is_common:
                continue
            is_isolated = True
            if r > 0:
                is_isolated = is_isolated and all(
                    j := starts[p] + c < len(g[0]) and g[r - 1][j] == bg
                    for p in range(k)
                )
            if r < h - 1:
                is_isolated = is_isolated and all(
                    j := starts[p] + c < len(g[0]) and g[r + 1][j] == bg
                    for p in range(k)
                )
            if is_isolated:
                bases.append((r, c))
    return bases

def propagate_pattern(output: List[List[int]], r_base: int, c_bases: List[int], k: int, h: int, w_panel: int, fg: int, direction: str):
    # Set bases
    for cb in c_bases:
        if 0 <= r_base < h and 0 <= cb < w_panel:
            output[r_base][cb] = fg
    # Determine num_lev
    if k % 2 == 0:
        num_lev = 2 if direction == 'down' else 1
    else:
        num_lev = 1
    step = 1 if direction == 'down' else -1
    for lev in range(1, num_lev + 1):
        rr = r_base + lev * step
        if not (0 <= rr < h):
            continue
        if direction == 'down':
            if lev == 1:
                if k % 2 == 0:
                    # center
                    for cb in c_bases:
                        cc = cb
                        if 0 <= cc < w_panel:
                            output[rr][cc] = fg
                else:
                    # left right
                    for cb in c_bases:
                        for dcc in [-1, 1]:
                            cc = cb + dcc
                            if 0 <= cc < w_panel:
                                output[rr][cc] = fg
            elif lev == 2:
                # left right
                for cb in c_bases:
                    for dcc in [-1, 1]:
                        cc = cb + dcc
                        if 0 <= cc < w_panel:
                            output[rr][cc] = fg
        else:  # up
            # left center right
            for cb in c_bases:
                for dcc in [-1, 0, 1]:
                    cc = cb + dcc
                    if 0 <= cc < w_panel:
                        output[rr][cc] = fg

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    bg = find_background(g)
    seps = find_separator_columns(g, bg)
    if seps:
        d = get_divider_color(g, seps, bg)
        fg = get_foreground_color(g, bg, d)
        m = len(seps)
        k = m + 1
        total_panel = w - m
        if total_panel % k != 0:
            # fallback
            k = 3
            seps = []
            fg = get_foreground_color(g, bg, None)
        else:
            w_panel = total_panel // k
            starts = get_panel_starts(seps, w, w_panel, k)
    else:
        k = 3
        w_panel = w // k
        starts = [p * w_panel for p in range(k)]
        fg = get_foreground_color(g, bg, None)
    output = [[bg for _ in range(w_panel)] for _ in range(h)]
    bases = find_bases(g, starts, k, h, w_panel, fg, bg)
    if bases:
        bases.sort()
        r_base = bases[0][0]
        c_bases = [c for rr, c in bases if rr == r_base]
        down_space = h - r_base
        up_space = r_base
        direction = 'down' if down_space >= up_space else 'up'
        propagate_pattern(output, r_base, c_bases, k, h, w_panel, fg, direction)
    else:
        # copy left panel
        for rr in range(h):
            for cc in range(w_panel):
                jj = cc  # left start 0
                if jj < w:
                    output[rr][cc] = g[rr][jj]
    return output
```