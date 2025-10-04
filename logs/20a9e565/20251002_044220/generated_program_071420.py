```python
from typing import List

def get_five_positions(g: List[List[int]]) -> List[tuple[int, int]]:
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
        return -1, -1, -1, -1
    min_r = min(r for r, _ in positions)
    max_r = max(r for r, _ in positions)
    min_c = min(c for _, c in positions)
    max_c = max(c for _, c in positions)
    return min_r, max_r, min_c, max_c

def find_main_color(g: List[List[int]], min_r: int, max_r: int, cols: int) -> int:
    # Find leftmost topmost >1 !=5 in bbox rows
    found = False
    c = 0
    for j in range(cols):
        for i in range(min_r, max_r + 1):
            val = g[i][j]
            if val > 1 and val != 5:
                c = val
                found = True
                break
        if found:
            break
    if not found:
        # Fallback to whole grid
        rows = len(g)
        for j in range(cols):
            for i in range(rows):
                val = g[i][j]
                if val > 1 and val != 5:
                    c = val
                    found = True
                    break
            if found:
                break
    return c

def get_left_right_colors(clean_row: List[int]) -> List[int]:
    groups = []
    i = 0
    n = len(clean_row)
    while i < n:
        if clean_row[i] == 0:
            i += 1
            continue
        start = i
        left_c = clean_row[i]
        i += 1
        while i < n and clean_row[i] != 0:
            i += 1
        right_c = clean_row[i - 1]
        size = i - start
        if size >= 2:
            groups.append((left_c, right_c))
    if groups:
        return [groups[0][0], groups[-1][1]]
    # Fallback to first non-zero duplicated
    single_c = 0
    for val in clean_row:
        if val != 0:
            single_c = val
            break
    return [single_c, single_c]

def program(g: List[List[int]]) -> List[List[int]]:
    positions = get_five_positions(g)
    if not positions:
        return []
    min_r, max_r, min_c, max_c = compute_bbox(positions)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    if h <= 0 or w <= 0:
        return []
    cols = len(g[0]) if g else 0
    output = [[0] * w for _ in range(h)]
    if w == 2:
        # Special case for w=2: extract pairs from bbox rows
        pairs = []
        for r in range(min_r, max_r + 1):
            clean_row = [0 if x == 5 else x for x in g[r]]
            pair = get_left_right_colors(clean_row)
            pairs.append(pair)
        k = h // 2
        upper = pairs[:k]
        lower = []
        for idx in range(1, k):
            p = upper[idx]
            lower.append([p[1], p[0]])
        if k > 0:
            last_upper = upper[k - 1]
            lower.append([last_upper[1], last_upper[0]])
        if h % 2 == 1:
            # For odd h, append the center unchanged (pairs[k])
            lower = lower[:-1]  # Adjust if needed, but no example
            lower.append(pairs[k])
        if len(lower) < h - k:
            # Pad if necessary, but for even it should be k
            pass
        full_pairs = upper + lower
        for i in range(h):
            output[i] = full_pairs[i]
        return output
    # General case: single color alternating pattern
    c = find_main_color(g, min_r, max_r, cols)
    if c == 0:
        return output  # All zero
    for i in range(h):
        if i % 2 == 0 or (i == h - 1 and h % 2 == 0):
            # Full row
            output[i] = [c] * w
        else:
            # Sparse row
            if w <= 3:
                sparse = [c] + [0] * (w - 2) + [c] if w >= 2 else [c]
            else:
                sparse = [c] + [0] * (w - 1)
            output[i] = sparse
    return output
```