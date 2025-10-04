```python
from typing import List
from collections import Counter

def find_five_positions(g: List[List[int]]) -> List[tuple[int, int]]:
    positions = []
    rows = len(g)
    if rows == 0:
        return positions
    cols = len(g[0])
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 5:
                positions.append((r, c))
    return positions

def compute_bbox(positions: List[tuple[int, int]]) -> tuple[int, int, int, int]:
    if not positions:
        raise ValueError("No 5's found")
    min_r = min(r for r, _ in positions)
    max_r = max(r for r, _ in positions)
    min_c = min(c for _, c in positions)
    max_c = max(c for _, c in positions)
    return min_r, max_r, min_c, max_c

def get_main_color(g: List[List[int]], min_r: int, max_r: int, min_c: int) -> int:
    ignore = {0, 1, 5}
    row_counts = Counter()
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    for r in range(min_r, max_r + 1):
        row_has = set()
        for c in range(min(min_c, cols)):
            val = g[r][c]
            if val not in ignore:
                row_has.add(val)
        for colr in row_has:
            row_counts[colr] += 1
    if row_counts:
        max_rows_cnt = max(row_counts.values())
        candidates = [col for col, cnt in row_counts.items() if cnt == max_rows_cnt]
        return min(candidates)
    # fallback global
    global_counts = Counter()
    for r in range(rows):
        for c in range(cols):
            val = g[r][c]
            if val not in ignore:
                global_counts[val] += 1
    if global_counts:
        return global_counts.most_common(1)[0][0]
    return 0

def get_left_right_colors(row_data: List[int]) -> List[int]:
    n = len(row_data)
    groups = []
    i = 0
    while i < n:
        if row_data[i] == 0 or row_data[i] == 5:
            i += 1
            continue
        start = i
        left_c = row_data[i]
        i += 1
        while i < n and row_data[i] != 0 and row_data[i] != 5:
            i += 1
        right_c = row_data[i - 1]
        size = i - start
        if size >= 2:
            groups.append((left_c, right_c))
    if groups:
        return [groups[0][0], groups[-1][1]]
    # single
    single_c = 0
    for val in row_data:
        if val != 0 and val != 5:
            single_c = val
            break
    return [single_c, single_c]

def program(g: List[List[int]]) -> List[List[int]]:
    positions = find_five_positions(g)
    if not positions:
        return []
    min_r, max_r, min_c, max_c = compute_bbox(positions)
    H = max_r - min_r + 1
    W = max_c - min_c + 1
    output = [[0] * W for _ in range(H)]
    if W == 2 and H > W:
        # special case for width 2 vertical: upper half computed, lower half swapped upper
        mid = H // 2
        upper = []
        for k in range(mid):
            r = min_r + k
            pair = get_left_right_colors(g[r])
            upper.append(pair)
        lower = [[b, a] for a, b in upper]
        full = upper + lower
        for rr in range(H):
            output[rr] = full[rr]
    else:
        C = get_main_color(g, min_r, max_r, min_c)
        is_vertical = H > W
        # fill left column all
        for rr in range(H):
            output[rr][0] = C
        # fill right column conditionally
        for rr in range(H):
            if is_vertical or rr == 0 or rr == H - 1:
                output[rr][W - 1] = C
        # fill top and bottom full
        for cc in range(W):
            output[0][cc] = C
            if H > 1:
                output[H - 1][cc] = C
        # middle connection for width 3 vertical
        if W == 3 and is_vertical:
            for rr in range(H):
                if rr % 2 == 0:
                    output[rr][1] = C
    return output
```