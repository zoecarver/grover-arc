```python
from typing import List, Dict, Set, Tuple
import collections

def program(g: List[List[int]]) -> List[List[int]]:
    height = len(g)
    width = len(g[0]) if height > 0 else 0
    if height == 0 or width == 0:
        return [row[:] for row in g]
    # Find F and frame_color
    F = -1
    frame_color = 0
    for col in range(width):
        col_colors = [row[col] for row in g]
        if all(cc == col_colors[0] and cc > 0 for cc in col_colors):
            F = col
            frame_color = col_colors[0]
            break
    if F == -1:
        return [row[:] for row in g]
    S = F + 1
    mid_col = (F - 1) // 2
    out = [row[:] for row in g]
    # Anchors
    anchors = collections.defaultdict(list)
    for r in range(height):
        c = g[r][S]
        if c > 0 and c != frame_color:
            anchors[c].append(r)
    # Clues
    clues = collections.defaultdict(list)
    for p in range(S, width - 1):
        c = g[0][p]
        if c > 0 and c != frame_color:
            clues[c].append(p)
    # Shapes
    shapes = {}
    for c in set(anchors.keys()) & set(clues.keys()):
        left_cells = [(r, col) for r in range(height) for col in range(F) if g[r][col] == c]
        if not left_cells:
            continue
        min_r = min(r for r, _ in left_cells)
        max_r = max(r for r, _ in left_cells)
        orig_center = min_r + (max_r - min_r) // 2
        upper_offset = orig_center - min_r
        lower_offset = max_r - orig_center
        shape = collections.defaultdict(set)
        for r, col in left_cells:
            delta_r = r - orig_center
            delta_c = col - mid_col
            shape[delta_r].add(delta_c)
        shapes[c] = (shape, orig_center, upper_offset, lower_offset)
    # Clear left for C in shapes
    for r in range(height):
        for col in range(F):
            c = g[r][col]
            if c in shapes:
                out[r][col] = 0
    # Set mirror
    for r in range(height):
        out[r][width - 1] = g[r][S]
    # Place shapes
    row_to_protecting = collections.defaultdict(set)
    placed_anchors = {}
    for c in shapes:
        anchor_rs = anchors.get(c, [])
        if not anchor_rs:
            continue
        _, orig_center, _, _ = shapes[c]
        chosen_r = min(anchor_rs, key=lambda rr: abs(rr - orig_center))
        placed_anchors[c] = chosen_r
        # place
        ps = clues.get(c, [])
        if not ps:
            continue
        p = min(ps)
        shape, _, upper_offset, lower_offset = shapes[c]
        for delta_r, d_cols in shape.items():
            pr = chosen_r + delta_r
            if 0 <= pr < height:
                for delta_c in d_cols:
                    pc = p + delta_c
                    if 0 <= pc < width and out[pr][pc] == 0:
                        out[pr][pc] = c
        # protected
        upper_pr = chosen_r - upper_offset
        center_pr = chosen_r
        if 0 <= upper_pr < height:
            row_to_protecting[upper_pr].add(c)
        row_to_protecting[center_pr].add(c)
    # Skipped anchors adjacent fill
    for c in anchors:
        chosen = placed_anchors.get(c, None)
        for r in anchors[c]:
            if r == chosen:
                continue
            # adjacent fill
            ps = clues.get(c, [])
            for p in ps:
                for di in [-1, 0, 1]:
                    pc = p + di
                    if 0 <= pc < width and out[r][pc] == 0:
                        out[r][pc] = c
    # Clue single fills for c with multiple ps
    for c in clues:
        if len(clues[c]) <= 1:
            continue
        ps = clues[c]
        for r in range(height):
            if r in row_to_protecting and c not in row_to_protecting[r]:
                continue
            for p in ps:
                if out[r][p] == 0:
                    out[r][p] = c
    return out
```