```python
from collections import defaultdict, Counter
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    H = len(g)
    W = len(g[0])
    # Find stem_col and frame_color
    stem_col = -1
    frame_color = 0
    for col in range(W):
        col_colors = [row[col] for row in g]
        counter = Counter(col_colors)
        if counter:
            mode, count = counter.most_common(1)[0]
            if mode != 0 and count > H // 2 and g[0][col] == mode == g[H - 1][col]:
                stem_col = col
                frame_color = mode
                break
    if stem_col == -1:
        return [row[:] for row in g]
    mid_col = (stem_col - 1) // 2
    # Base colors: unique to left
    left_colors = set()
    right_colors = set()
    for i in range(H):
        for c in range(stem_col):
            if g[i][c] != 0:
                left_colors.add(g[i][c])
        for c in range(stem_col, W):
            if g[i][c] != 0:
                right_colors.add(g[i][c])
    base_colors = left_colors - right_colors
    # Output grid
    out = [row[:] for row in g]
    # Clean left in all rows
    for i in range(H):
        for c in range(stem_col):
            if out[i][c] not in base_colors:
                out[i][c] = 0
    # Enforce stem column
    for i in range(H):
        if g[i][stem_col] != frame_color:
            out[i][stem_col] = g[i][stem_col]
        else:
            out[i][stem_col] = frame_color
    # Determine key_col
    is_uniform = all(out[i][stem_col] == frame_color for i in range(H))
    key_col = stem_col if not is_uniform else stem_col + 1
    if key_col >= W:
        return out
    # Mirror to last column
    for i in range(H):
        out[i][W - 1] = out[i][key_col]
    # Zero inner right in middle rows
    for i in range(1, H - 1):
        for c in range(key_col + 1, W - 1):
            out[i][c] = 0
    # Extract anchors (middle rows)
    anchors = defaultdict(list)
    for i in range(1, H - 1):
        c = out[i][key_col]
        if c != 0 and c != frame_color:
            anchors[c].append(i)
    # Extract clues (top row)
    clues = defaultdict(list)
    for c in range(key_col, W - 1):
        cc = g[0][c]
        if cc != 0 and cc != frame_color:
            clues[cc].append(c)
    # Placement
    for C in sorted(anchors.keys() & clues.keys()):
        left_cells = [(r, cc) for r in range(H) for cc in range(stem_col) if g[r][cc] == C]
        if not left_cells:
            continue
        min_r_ = min(r for r, _ in left_cells)
        max_r_ = max(r for r, _ in left_cells)
        orig_center = min_r_ + (max_r_ - min_r_) // 2
        shape = defaultdict(set)
        for r, cc in left_cells:
            dr = r - orig_center
            dc = cc - mid_col
            shape[dr].add(dc)
        # Find widest_dr: max len, tie smallest |dr|, tie smallest dr
        widest_dr = None
        max_len = -1
        for dr in sorted(shape):
            l = len(shape[dr])
            curr_abs = abs(dr)
            if l > max_len or (l == max_len and (curr_abs < abs(widest_dr) if widest_dr is not None else True) or (l == max_len and curr_abs == abs(widest_dr) and dr < widest_dr)):
                max_len = l
                widest_dr = dr
        flip = widest_dr > 0
        place_shape = defaultdict(set)
        if flip:
            flipped = defaultdict(set)
            for dr in shape:
                flipped[-dr] |= shape[dr]
            shift = widest_dr
            for dr in flipped:
                place_shape[dr + shift] |= flipped[dr]
        else:
            place_shape = shape
        # Place for each anchor
        for anchor_r in anchors[C]:
            for p in clues[C]:
                placed_drs = set()
                for dr in place_shape:
                    if abs(dr) > 1:
                        continue
                    placed_drs.add(dr)
                    for dc in place_shape[dr]:
                        t_row = anchor_r + dr
                        t_col = p + dc
                        if 1 <= t_row < H - 1 and key_col < t_col < W - 1 and out[t_row][t_col] == 0:
                            out[t_row][t_col] = C
                # Add missing adjacent singles (dc=0)
                for adj_dr in [-1, 1]:
                    if adj_dr not in placed_drs:
                        t_row = anchor_r + adj_dr
                        if 1 <= t_row < H - 1:
                            t_col = p + 0
                            if key_col < t_col < W - 1 and out[t_row][t_col] == 0:
                                out[t_row][t_col] = C
    return out
```