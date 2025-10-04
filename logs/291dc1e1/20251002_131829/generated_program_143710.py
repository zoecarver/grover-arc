```python
from typing import List, Tuple

def find_frame_col(g: List[List[int]]) -> int:
    h = len(g)
    if h == 0:
        return -1
    w = len(g[0])
    if w == 0:
        return -1
    counts = [0] * w
    for j in range(w):
        for i in range(1, h):
            if g[i][j] in (1, 2):
                counts[j] += 1
    max_count = max(counts)
    candidates = [j for j, c in enumerate(counts) if c == max_count]
    if len(candidates) != 1:
        return -1  # Assume exactly one
    return candidates[0]

def get_blocks(inner_rows: List[List[int]], col_start: int, col_end: int) -> List[Tuple[int, int, int, int]]:
    h_inner = len(inner_rows)
    w_inner = len(inner_rows[0]) if h_inner > 0 else 0
    visited = [[False] * w_inner for _ in range(h_inner)]
    blocks = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h_inner):
        for j in range(col_start, col_end + 1):
            if inner_rows[i][j] != 8 and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                min_r = max_r = i
                min_c = max_c = j
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h_inner and col_start <= ny <= col_end and inner_rows[nx][ny] != 8 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                exp_p = (max_r - min_r + 1) * (max_c - min_c + 1)
                if len(component) == exp_p:
                    blocks.append((min_r, max_r, min_c, max_c))
    return blocks

def program(g: List[List[int]]) -> List[List[int]]:
    frame_col = find_frame_col(g)
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    left_frame = frame_col == 0
    inner_rows = [row[:] for row in g[1:]]
    h_inner = len(inner_rows)
    if h_inner == 0:
        return []
    if left_frame:
        for row in inner_rows:
            del row[0]
        inner_w = w - 1
    else:
        for row in inner_rows:
            del row[-1]
        inner_w = w - 1
    if inner_w <= 0:
        return []
    full_8 = [k for k in range(inner_w) if all(inner_rows[i][k] == 8 for i in range(h_inner))]
    full_set = set(full_8)
    strips = []
    i = 0
    while i < inner_w:
        if i in full_set:
            i += 1
            continue
        j = i
        while j < inner_w and j not in full_set:
            j += 1
        if i < j:
            strips.append((i, j - 1))
        i = j
    num_strips = len(strips)
    multiple_mode = False
    if num_strips > 1:
        has_w1 = False
        prev_end = strips[0][1]
        for st in strips[1:]:
            curr_start = st[0]
            sep_w = curr_start - prev_end - 1
            if sep_w == 1:
                has_w1 = True
            prev_end = st[1]
        multiple_mode = has_w1
    if not multiple_mode:
        # single mode
        all_blocks = get_blocks(inner_rows, 0, inner_w - 1)
        def sort_key(b):
            minr, _, minc, _ = b
            if left_frame:
                return (minr, minc)
            else:
                return (minr, -minc)
        all_blocks.sort(key=sort_key)
    else:
        # multiple mode
        if left_frame:
            strips.sort(key=lambda s: s[0])
        else:
            strips.sort(key=lambda s: -s[0])
        all_blocks = []
        for st_start, st_end in strips:
            st_blocks = get_blocks(inner_rows, st_start, st_end)
            st_blocks.sort(key=lambda b: b[0])
            all_blocks.extend(st_blocks)
    # compute global_w
    max_p = 0
    for b in all_blocks:
        minr, maxr, minc, maxc = b
        p = (maxr - minr + 1) * (maxc - minc + 1)
        if p > max_p:
            max_p = p
    global_w = (max_p + 1) // 2
    # generate output rows
    output_rows = []
    for b in all_blocks:
        minr, maxr, minc, maxc = b
        hb = maxr - minr + 1
        wb = maxc - minc + 1
        p = hb * wb
        wl = (p + 1) // 2
        seq = []
        for cc in range(minc, maxc + 1):
            for rr in range(minr, maxr + 1):
                seq.append(inner_rows[rr][cc])
        bottom = seq[:wl]
        top = seq[wl:wl * 2]
        # pad
        padl = (global_w - wl) // 2
        padr = global_w - wl - padl
        top_pad = [8] * padl + top + [8] * padr
        bottom_pad = [8] * padl + bottom + [8] * padr
        # fill if short (for odd)
        while len(top_pad) < global_w:
            top_pad.append(8)
        while len(bottom_pad) < global_w:
            bottom_pad.append(8)
        output_rows.append(top_pad)
        output_rows.append(bottom_pad)
    return output_rows
```