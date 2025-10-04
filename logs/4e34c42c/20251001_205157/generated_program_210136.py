```python
from typing import List, Tuple

def find_background(g: List[List[int]]) -> int:
    """Find the background color as the most frequent color in the grid."""
    if not g:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return max(set(flat), key=flat.count)

def extract_block(g: List[List[int]], start_r: int, bg: int, num_rows: int, num_cols: int) -> Tuple[int, int] or None:
    """Extract the left and right columns for a 5-row block starting at start_r, applying cap exclusion if applicable."""
    min_c = num_cols
    max_c = -1
    for dr in range(5):
        r = start_r + dr
        if r >= len(g):
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
        bottom = g[start_r + 4][c]
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
                extract = extract_block(g, i, bg, height - i, num_cols)
                if extract is not None:
                    left, right = extract
                    blocks.append((i, left, right))
                    i += 5
                    continue
        i += 1
    return blocks

def program(g: List[List[int]]) -> List[List[int]]:
    """Main function to generate the output grid by extracting and concatenating valid 5-row blocks."""
    if not g:
        return []
    num_rows = len(g)
    num_cols = len(g[0]) if num_rows > 0 else 0
    bg = find_background(g)
    blocks = find_valid_blocks(g, bg, num_rows, num_cols)
    # Order blocks by decreasing starting row (bottom to top)
    blocks.sort(key=lambda b: -b[0])
    if not blocks:
        return [[bg]]
    total_width = sum(b[2] - b[1] + 1 for b in blocks)
    out = [[bg for _ in range(total_width)] for _ in range(5)]
    cur_col = 0
    for start_r, left, right in blocks:
        w = right - left + 1
        for dr in range(5):
            r = start_r + dr
            for dc in range(w):
                out[dr][cur_col + dc] = g[r][left + dc]
        cur_col += w
    return out
```