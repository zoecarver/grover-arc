```python
from typing import List
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    flat = [g[i][j] for i in range(h) for j in range(w)]
    count_all = Counter(flat)
    bg = count_all.most_common(1)[0][0] if count_all else 0
    non_bg_count = Counter(c for c in flat if c != bg)
    if not non_bg_count:
        return [row[:] for row in g]
    boundary = non_bg_count.most_common(1)[0][0]

    def min_dist_to_boundary(color):
        if color == bg or color == boundary:
            return float('inf')
        seed_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == color]
        if not seed_pos:
            return float('inf')
        bound_pos = [(i, j) for i in range(h) for j in range(w) if g[i][j] == boundary]
        if not bound_pos:
            return float('inf')
        min_d = float('inf')
        for si, sj in seed_pos:
            for bi, bj in bound_pos:
                d = abs(si - bi) + abs(sj - bj)
                if d < min_d:
                    min_d = d
        return min_d

    possible_fills = [c for c in non_bg_count if c != boundary]
    if not possible_fills:
        return [row[:] for row in g]
    fill_dists = [(c, min_dist_to_boundary(c), non_bg_count[c]) for c in possible_fills]
    fill_dists.sort(key=lambda x: (x[1], -x[2]))
    fill = fill_dists[0][0]

    out = [row[:] for row in g]

    # Blockers: col -> min row with blocker
    blockers = {}
    for j in range(w):
        min_r = float('inf')
        for i in range(h):
            c = g[i][j]
            if c != bg and c != boundary and c != fill:
                min_r = min(min_r, i)
        if min_r != float('inf'):
            blockers[j] = min_r

    def should_skip(i, j):
        if j not in blockers:
            return False
        return i < blockers[j]

    # Internal fill
    changed_internal = 0
    for i in range(h):
        bound_pos = sorted([j for j in range(w) if out[i][j] == boundary])
        for k in range(len(bound_pos) - 1):
            left = bound_pos[k]
            right = bound_pos[k + 1]
            if right - left > 2:
                for j in range(left + 1, right):
                    if out[i][j] == bg and not should_skip(i, j):
                        out[i][j] = fill
                        changed_internal += 1

    is_closed = changed_internal > 10

    # Upward propagation if closed
    if is_closed:
        top_b_row = h
        for ii in range(h):
            if any(out[ii][jj] == boundary for jj in range(w)):
                top_b_row = ii
                break
        for r in range(top_b_row - 1, -1, -1):
            filled_in_below = [j for j in range(w) if out[r + 1][j] == fill]
            if not filled_in_below:
                continue
            has_blocker = any(g[r][j] != bg and g[r][j] != boundary and g[r][j] != fill for j in range(w))
            if has_blocker:
                # Copy positions from below
                for j in filled_in_below:
                    if out[r][j] == bg and not should_skip(r, j):
                        out[r][j] = fill
            else:
                # Extend
                min_f = min(filled_in_below)
                max_f = max(filled_in_below)
                new_min = max(0, min_f - 1)
                new_max = min(w - 1, max_f + 1)
                for j in range(new_min, new_max + 1):
                    if out[r][j] == bg and not should_skip(r, j):
                        out[r][j] = fill

    # If open, do left fill and upward narrowing
    else:
        # Find rows with boundary
        rows_with_bound = set(i for i in range(h) if any(out[i][j] == boundary for j in range(w)))
        if rows_with_bound:
            top_r = min(rows_with_bound)
            # Left fill in rows with boundary
            for i in rows_with_bound:
                bound_pos = [j for j in range(w) if out[i][j] == boundary]
                if bound_pos:
                    leftmost = min(bound_pos)
                    for j in range(leftmost):
                        if out[i][j] == bg:
                            out[i][j] = fill
            # Upward narrowing
            for r in range(top_r - 1, -1, -1):
                # Find L in r+1
                if r + 1 not in rows_with_bound:
                    # If r+1 no bound, continue narrowing? But assume chain
                    continue
                bound_pos_below = [j for j in range(w) if out[r + 1][j] == boundary]
                if not bound_pos_below:
                    continue
                L = min(bound_pos_below) - 1
                new_L = max(-1, L - 1)
                for j in range(new_L + 1):
                    if out[r][j] == bg:
                        out[r][j] = fill

    # Secondary widening near bottom
    bottom_start = max(0, h - 4)
    for i in range(bottom_start, h):
        j = 0
        while j < w - 1:
            if out[i][j] != bg and out[i][j] == out[i][j + 1] and out[i][j] != boundary and out[i][j] != fill:
                c = out[i][j]
                col_start = j
                k = 2
                while j + k < w and out[i][j + k] == c:
                    k += 1
                num_below = h - i - 1
                if k >= 2 and num_below >= 1:
                    # Apply widening
                    side = num_below
                    # Seed row i
                    l_start = max(0, col_start - side)
                    l_end = col_start - 1
                    for jj in range(l_start, l_end + 1):
                        if out[i][jj] == bg:
                            out[i][jj] = fill
                    r_start = col_start + k
                    r_end = min(w - 1, col_start + k + side - 1)
                    for jj in range(r_start, r_end + 1):
                        if out[i][jj] == bg:
                            out[i][jj] = fill
                    # Below rows
                    curr_row = i + 1
                    curr_side = side + 1
                    while curr_row < h:
                        l_start = max(0, col_start - curr_side)
                        l_end = col_start - 1
                        for jj in range(l_start, l_end + 1):
                            if out[curr_row][jj] == bg:
                                out[curr_row][jj] = fill
                        r_start = col_start + k
                        r_end = min(w - 1, col_start + k + curr_side - 1)
                        for jj in range(r_start, r_end + 1):
                            if out[curr_row][jj] == bg:
                                out[curr_row][jj] = fill
                        curr_row += 1
                        curr_side += 1
                j += k - 1
            else:
                j += 1

    return out
```