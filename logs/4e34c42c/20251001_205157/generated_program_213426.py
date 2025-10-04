```python
from typing import List, Tuple
from collections import Counter

def find_background(g: List[List[int]]) -> int:
    """Find the background color as the most frequent color in the grid."""
    if not g:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return max(set(flat), key=Counter(flat).get)

def extract_block(g: List[List[int]], start_r: int, bg: int, num_rows: int, num_cols: int) -> Tuple[int, int] or None:
    """Extract the left and right columns for a 5-row block starting at start_r, applying cap exclusion if applicable."""
    min_c = num_cols
    max_c = -1
    h = len(g)
    for dr in range(num_rows):
        r = start_r + dr
        if r >= h:
            return None
        for c in range(num_cols):
            if g[r][c] != bg:
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    if max_c < 0:
        return None
    # Find leftmost cap column with 9 in top and bottom
    cap_c = -1
    for c in range(min_c, max_c + 1):
        top = g[start_r][c]
        bottom = g[start_r + num_rows - 1][c] if start_r + num_rows - 1 < h else bg
        if top == 9 and bottom == 9:
            cap_c = c
            break
    extract_left = min_c + 1 if cap_c == min_c else min_c
    return extract_left, max_c

def find_valid_blocks(g: List[List[int]], bg: int, height: int, num_cols: int) -> List[Tuple[int, int, int]]:
    """Find all valid 5-row blocks and their extraction ranges."""
    blocks = []
    i = 0
    while i < height - 4:
        # Check if row i has non-background
        has_non_bg_start = any(g[i][c] != bg for c in range(num_cols))
        if has_non_bg_start:
            # Check if row i+4 has non-background
            has_non_bg_end = any(g[i + 4][c] != bg for c in range(num_cols))
            if has_non_bg_end:
                extract = extract_block(g, i, bg, 5, num_cols)
                if extract is not None:
                    left, right = extract
                    blocks.append((i, left, right))
                    i += 5
                    continue
        i += 1
    return blocks

def max_overlap(left_sub: List[List[int]], right_sub: List[List[int]]) -> int:
    """Compute the maximum overlap k where the right k columns of left_sub match the left k columns of right_sub."""
    w1 = len(left_sub[0]) if left_sub and left_sub[0] else 0
    w2 = len(right_sub[0]) if right_sub and right_sub[0] else 0
    max_k = min(w1, w2)
    for k in range(max_k, -1, -1):
        match = True
        for row in range(5):
            for j in range(k):
                if left_sub[row][w1 - k + j] != right_sub[row][j]:
                    match = False
                    break
            if not match:
                break
        if match:
            return k
    return 0

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    bg = find_background(g)
    blocks = find_valid_blocks(g, bg, h, w)
    # Sort by starting row decreasing (bottom first)
    blocks.sort(key=lambda x: x[0], reverse=True)
    if not blocks:
        return [[bg for _ in range(w)] for _ in range(5)]
    # Extract first subgrid
    i, left, right = blocks[0]
    sub = [[g[r][c] for c in range(left, right + 1)] for r in range(i, i + 5)]
    strip = sub
    # Append remaining subgrids with overlap merging
    for blk in blocks[1:]:
        j, l, r = blk
        next_sub = [[g[r][c] for c in range(l, r + 1)] for r in range(j, j + 5)]
        k = max_overlap(strip, next_sub)
        ws = len(strip[0])
        for row_idx in range(5):
            strip[row_idx] = strip[row_idx][:ws - k] + next_sub[row_idx][k:]
    return strip
```