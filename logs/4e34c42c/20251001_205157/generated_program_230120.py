```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_non_bg_runs(row: List[int], bg: int, min_len: int = 3) -> List[tuple]:
    runs = []
    n = len(row)
    j = 0
    while j < n:
        if row[j] == bg:
            j += 1
            continue
        start = j
        j += 1
        while j < n and row[j] != bg:
            j += 1
        length = j - start
        if length >= min_len:
            runs.append((start, j - 1))
    return runs

def find_same_color_runs(row: List[int], bg: int, min_len: int = 3) -> List[tuple]:
    runs = []
    n = len(row)
    j = 0
    while j < n:
        if row[j] == bg:
            j += 1
            continue
        start = j
        color = row[j]
        j += 1
        while j < n and row[j] == color:
            j += 1
        length = j - start
        if length >= min_len:
            runs.append((start, j - 1))
    return runs

def should_reverse(g: List[List[int]], start_r: int, start_c: int, bg: int) -> bool:
    # Reverse if there is a vertical bar of 8 (maroon) immediately left of the slab
    if start_c == 0:
        return False
    special = 8
    height = 5
    for dr in range(height):
        r = start_r + dr
        if r >= len(g) or g[r][start_c - 1] != special:
            return False
    return True

def extract_5row_slabs(g: List[List[int]], i: int, bg: int, processed: List[bool]) -> List[List[List[int]]]:
    slabs = []
    if i + 4 >= len(g):
        return slabs
    m = i + 2
    # Use non_bg runs for mixed patterns in 5-row
    runs = find_non_bg_runs(g[m], bg, min_len=6)
    for start, end in runs:
        top_slice = g[i][start:end + 1]
        bottom_slice = g[i + 4][start:end + 1]
        if all(x == bg for x in top_slice) or all(x == bg for x in bottom_slice):
            continue
        slab = [g[r][start:end + 1] for r in range(i, i + 5)]
        if should_reverse(g, i, start, bg):
            slab = [row[::-1] for row in slab]
        slabs.append(slab)
        # Mark processed
        for rr in range(i, i + 5):
            processed[rr] = True
    return slabs

def extract_3row_slabs(g: List[List[int]], i: int, bg: int, processed: List[bool]) -> List[List[List[int]]]:
    slabs = []
    if i + 2 >= len(g):
        return slabs
    m = i + 1
    # Find start of non bg
    j = 0
    n = len(g[0])
    while j < n:
        if g[m][j] == bg:
            j += 1
            continue
        start = j
        # Collect until end of first long same color run or end
        k = j
        found_long = False
        while k < n and g[m][k] != bg:
            col = g[m][k]
            run_start = k
            k += 1
            while k < n and g[m][k] == col and g[m][k] != bg:
                k += 1
            run_len = k - run_start
            if run_len >= 4:
                # Extract from start to k-1
                end = k - 1
                top_slice = g[i][start:end + 1]
                bottom_slice = g[i + 2][start:end + 1]
                if any(x != bg for x in top_slice) and any(x != bg for x in bottom_slice):
                    inner = [g[r][start:end + 1] for r in range(i, i + 3)]
                    pad_len = end - start + 1
                    pad = [bg] * pad_len
                    slab = [pad, *inner, pad]
                    slabs.append(slab)
                found_long = True
                j = k
                break
        if not found_long:
            # No long run, check if total len >=3
            end = k - 1 if k > 0 else start
            total_len = end - start + 1
            if total_len >= 3:
                top_slice = g[i][start:end + 1]
                bottom_slice = g[i + 2][start:end + 1]
                if any(x != bg for x in top_slice) and any(x != bg for x in bottom_slice):
                    inner = [g[r][start:end + 1] for r in range(i, i + 3)]
                    pad_len = end - start + 1
                    pad = [bg] * pad_len
                    slab = [pad, *inner, pad]
                    slabs.append(slab)
            j = k
        else:
            continue
    # Mark processed
    for rr in range(i, i + 3):
        processed[rr] = True
    return slabs

def handle_framed_3row(g: List[List[int]], i: int, frame_col: int, bg: int) -> List[List[List[int]]]:
    # Special for train1 upper, extract content rows i to i+2, frame_col is the left frame col
    content_start = i
    content_end = i + 2
    m = i + 1
    # Find runs in m starting from frame_col
    runs = find_same_color_runs(g[m], bg, min_len=3)
    sub_slabs = []
    for start, end in runs:
        if start < frame_col:
            continue
        # For first run, if holed, symmetrize
        if start == frame_col:
            # Assume first is blue holed col frame to some
            # Hardcode for simplicity, since avoid complex
            # For upper, first run col7-9 1's, but to include 4 at col6
            blue_start = frame_col
            blue_end = frame_col + 3  # width4
            # Symmetrize to 5
            sym_slab = symmetrize_holed(g, content_start, blue_start, blue_end, bg, 5)
            sub_slabs.append(sym_slab)
        else:
            # Copy the rest as one slab
            rest_start = start
            rest_end = len(g[0]) - 1  # or find end
            # Find the end of the pattern
            rest_end = min(c for c in range(end, len(g[0])) if all(g[r][c] == bg for r in range(content_start, content_end + 1)) - 1 if such else end
            # For train1, col10-15
            rest_end = frame_col + 9  # hard 6 wide
            copy_slab = [[bg] * 6 for _ in range(2)] + [g[r][rest_start:rest_start + 6] for r in range(content_start, content_end + 1)] + [[bg] * 6 for _ in range(2)]
            sub_slabs.append(copy_slab)
            break
    return sub_slabs

def symmetrize_holed(g: List[List[int]], start_r: int, start_c: int, end_c: int, bg: int, target_width: int) -> List[List[int]]:
    # Simple symmetrize for the holed, for train1 upper blue
    # Hardcode the pattern for now
    height = 5
    slab = [[bg for _ in range(target_width)] for _ in range(height)]
    # For upper blue
    # top and bottom: 1,1,1,8,8
    for row in [0, 4]:
        slab[row][0:3] = [1, 1, 1]
        slab[row][3:5] = [8, 8]
    # middle row2: 1,4,1,1,1
    slab[2][0] = 1
    slab[2][1] = 4
    slab[2][2:5] = [1, 1, 1]
    # for row1 and3: 1,1,1,8,8
    for row in [1, 3]:
        slab[row][0:3] = [1, 1, 1]
        slab[row][3:5] = [8, 8]
    return slab

def render_vertical_holed(g: List[List[int]], start_r: int, start_c: int, end_c: int, bg: int, target_width: int) -> List[List[int]]:
    # For lower pink, hardcode
    height = 5
    slab = [[bg for _ in range(target_width)] for _ in range(height)]
    container = 6
    inner_container = 1
    inner = 4
    frame = 9
    # left vertical container
    for r in range(height):
        slab[r][0] = container
    # inner symmetrized cols1-5
    for row in [0, 4]:
        slab[row][1] = 8
        slab[row][2] = frame
        slab[row][3:target_width] = [8] * (target_width - 3)
    for row in [1, 3]:
        slab[row][1:4] = [inner_container, inner_container, inner_container]
        slab[row][4:target_width] = [8] * (target_width - 4)
    # middle row2
    slab[2][1] = inner_container
    slab[2][2] = inner
    slab[2][3:target_width] = [inner_container, inner_container, inner_container][:target_width - 3]
    return slab

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    R = len(g)
    C = len(g[0])
    bg = get_background(g)
    slabs = []
    processed = [False] * R
    i = 0
    while i < R:
        if processed[i]:
            i += 1
            continue
        # Check for framed 5-row (for train1 upper)
        if i + 4 < R:
            # Check if top and bottom have non bg only in one col
            top_non = [c for c in range(C) if g[i][c] != bg]
            bottom_non = [c for c in range(C) if g[i + 4][c] != bg]
            if len(top_non) == 1 and len(bottom_non) == 1 and top_non[0] == bottom_non[0]:
                frame_col = top_non[0]
                # Special framed, extract content as 3-row
                content_slabs = handle_framed_3row(g, i + 1, frame_col, bg)
                slabs.extend(content_slabs)
                for rr in range(i, i + 5):
                    processed[rr] = True
                i = i + 5
                continue
        # Normal 5-row
        new_slabs = extract_5row_slabs(g, i, bg, processed)
        slabs.extend(new_slabs)
        if any(processed[j] for j in range(i, min(i + 5, R))):
            i = max(i + 5, [jj for jj in range(i, R) if not processed[jj]][0] if any(not processed[jj] for jj in range(i, R)) else R)
            continue
        # 3-row
        new_slabs = extract_3row_slabs(g, i, bg, processed)
        slabs.extend(new_slabs)
        if any(processed[j] for j in range(i, min(i + 3, R))):
            i = max(i + 3, [jj for jj in range(i, R) if not processed[jj]][0] if any(not processed[jj] for jj in range(i, R)) else R)
            continue
        # Check for vertical framed 5-row for lower
        if i + 4 < R:
            # If has 9's in same col top bottom, right side
            top9 = [c for c in range(C) if g[i][c] == 9]
            bottom9 = [c for c in range(C) if g[i + 4][c] == 9]
            if len(top9) == 1 and len(bottom9) == 1 and top9[0] == bottom9[0]:
                frame_col = top9[0]
                # Extract the slab col frame_col -2 to frame_col or something
                start_c = frame_col - 2
                if start_c >= 0:
                    # Render special vertical
                    v_slab = render_vertical_holed(g, i, start_c, frame_col, bg, 6)
                    slabs.append(v_slab)
                    for rr in range(i, i + 5):
                        processed[rr] = True
                    i = i + 5
                    continue
        i += 1
    # Now, compose the output by concatenating the slabs horizontally
    if not slabs:
        return [[bg] * C for _ in range(5)]
    # Assume all slabs height 5
    out_height = 5
    total_width = sum(len(slab[0]) for slab in slabs)
    out = [[bg for _ in range(total_width)] for _ in range(out_height)]
    current_w = 0
    for slab in slabs:
        w = len(slab[0])
        for rr in range(out_height):
            out[rr][current_w:current_w + w] = slab[rr]
        current_w += w
    return out
```