```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    output = [row[:] for row in g]
    INF = 100
    # Handle odd rows: replace groups of three 7's with 8,6,8; rest 0
    for r in range(1, rows, 2):
        for c in range(cols):
            output[r][c] = 0
        i = 0
        while i < cols - 2:
            if g[r][i] == 7 and g[r][i + 1] == 7 and g[r][i + 2] == 7:
                output[r][i] = 8
                output[r][i + 1] = 6
                output[r][i + 2] = 8
                i += 3
            else:
                i += 1
    # Collect centers for each odd row
    centers = [[] for _ in range(rows)]
    for r in range(1, rows, 2):
        i = 0
        while i < cols - 2:
            if g[r][i] == 7 and g[r][i + 1] == 7 and g[r][i + 2] == 7:
                centers[r].append(i + 1)
                i += 3
            else:
                i += 1
    # Place 6's in even rows
    for r in range(0, rows, 2):
        adj = set()
        if r - 1 >= 0:
            adj.update(centers[r - 1])
        if r + 1 < rows:
            adj.update(centers[r + 1])
        for c in adj:
            if 0 <= c < cols:
                output[r][c] = 6
    # Now process even rows
    for r in range(0, rows, 2):
        six_set = {c for c in range(cols) if output[r][c] == 6}
        six_list = sorted(six_set)
        if r == 0:
            # Top row special: set non-0 non-6 to 8
            for c in range(cols):
                if g[r][c] != 0 and output[r][c] != 6:
                    output[r][c] = 8
            continue
        # Default: set non-0 non-6 to 8
        for c in range(cols):
            if g[r][c] != 0 and output[r][c] != 6:
                output[r][c] = 8
        # Adjacent to 0 rules
        zero_pos = [c for c in range(cols) if g[r][c] == 0]
        z_idx = 0
        while z_idx < len(zero_pos):
            c = zero_pos[z_idx]
            # Previous segment
            prev_z = -1 if z_idx == 0 else zero_pos[z_idx - 1]
            seg_start_b = prev_z + 1
            seg_end_b = c - 1
            has_six_b = any(cc in six_set for cc in range(max(0, seg_start_b), seg_end_b + 1)) if seg_start_b <= seg_end_b else False
            # Next segment
            next_z = cols if z_idx + 1 == len(zero_pos) else zero_pos[z_idx + 1]
            seg_start_a = c + 1
            seg_end_a = next_z - 1
            has_six_a = any(cc in six_set for cc in range(seg_start_a, min(cols - 1, seg_end_a) + 1)) if seg_start_a <= seg_end_a else False
            # Apply
            if r == rows - 1:  # bottom, only after
                if has_six_a and seg_start_a < cols and output[r][seg_start_a] != 0 and output[r][seg_start_a] != 6:
                    output[r][seg_start_a] = 3
            else:  # internal
                if has_six_b and seg_end_b >= 0 and output[r][seg_end_b] != 0 and output[r][seg_end_b] != 6:
                    output[r][seg_end_b] = 3
                if has_six_a and seg_start_a < cols and output[r][seg_start_a] != 0 and output[r][seg_start_a] != 6:
                    output[r][seg_start_a] = 3
            z_idx += 1
        # Border extensions
        if len(six_list) == 0:
            continue
        first6 = six_list[0]
        last6 = six_list[-1]
        # Left
        prefix_has_zero = any(g[r][cc] == 0 for cc in range(first6))
        k_upper_l = min(centers[r - 1]) if centers[r - 1] else INF
        k_lower_l = min(centers[r + 1]) if r + 1 < rows and centers[r + 1] else INF
        left_cond = k_upper_l <= k_lower_l
        if left_cond and not prefix_has_zero:
            l_left = first6
            output[r][0] = 3
            if l_left <= 4 and 1 < cols:
                output[r][1] = 3
        else:
            if left_cond:  # met but zero, keep input at 0
                output[r][0] = g[r][0]
        # Right
        suffix_has_zero = any(g[r][cc] == 0 for cc in range(last6 + 1, cols))
        k_upper_r = max(centers[r - 1]) if centers[r - 1] else -1
        k_lower_r = max(centers[r + 1]) if r + 1 < rows and centers[r + 1] else -1
        right_cond = (r + 1 >= rows) or (k_lower_r <= k_upper_r)
        if right_cond and not suffix_has_zero:
            l_right = cols - 1 - last6
            output[r][cols - 1] = 3
            if l_right <= 4 and cols > 1:
                output[r][cols - 2] = 3
        else:
            if right_cond:  # met but zero, keep input at m
                output[r][cols - 1] = g[r][cols - 1]
    return output
```