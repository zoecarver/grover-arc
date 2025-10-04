```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    """Extract the background color from the top-left corner."""
    if not g or not g[0]:
        return 0
    return g[0][0]

def extract_subgrid(g: List[List[int]], start_r: int, bg: int, w: int) -> List[List[int]] | None:
    """Extract and trim the 5-row subgrid starting at start_r, bounding non-background cells and trimming full background columns."""
    h = len(g)
    min_c = w
    max_c = -1
    for dr in range(5):
        r = start_r + dr
        if r >= h:
            return None
        for c in range(w):
            if g[r][c] != bg:
                min_c = min(min_c, c)
                max_c = max(max_c, c)
    if min_c > max_c:
        return None
    # Trim leading background columns
    left = min_c
    while left <= max_c:
        if all(g[start_r + dr][left] == bg for dr in range(5)):
            left += 1
        else:
            break
    # Trim trailing background columns
    right = max_c
    while right >= left:
        if all(g[start_r + dr][right] == bg for dr in range(5)):
            right -= 1
        else:
            break
    if left > right:
        return None
    width = right - left + 1
    sub = [[g[start_r + dr][left + dc] for dc in range(width)] for dr in range(5)]
    return sub

def find_blocks(g: List[List[int]], bg: int, h: int, w: int) -> List[Tuple[int, List[List[int]]]]:
    """Find non-overlapping 5-row blocks starting at valid i, where both start and end rows have non-background cells, skipping 5 rows after each valid block."""
    blocks = []
    i = 0
    while i < h - 4:
        has_start = any(g[i][c] != bg for c in range(w))
        has_end = any(g[i + 4][c] != bg for c in range(w))
        if has_start and has_end:
            sub = extract_subgrid(g, i, bg, w)
            if sub is not None:
                blocks.append((i, sub))
                i += 5
                continue
        i += 1
    return blocks

def sort_blocks(blocks: List[Tuple[int, List[List[int]]]]) -> List[List[List[int]]]:
    """Sort blocks by decreasing starting row index (bottom to top) and extract subgrids."""
    sorted_blocks = sorted(blocks, key=lambda x: -x[0])
    return [sub for _, sub in sorted_blocks]

def compute_max_overlap(left_sub: List[List[int]], right_sub: List[List[int]]) -> int:
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

def merge_subgrids(subgrids: List[List[List[int]]], bg: int) -> List[List[int]]:
    """Merge subgrids sequentially from left to right using maximum overlap, starting with the first subgrid."""
    if not subgrids:
        return [[bg] for _ in range(5)]
    strip = [row[:] for row in subgrids[0]]
    for sub in subgrids[1:]:
        k = compute_max_overlap(strip, sub)
        for r in range(5):
            strip[r].extend(sub[r][k:])
    return strip

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program: find, sort, and merge 5-row blocks into a horizontal strip."""
    if not g:
        return []
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    bg = get_background(g)
    blocks = find_blocks(g, bg, h, w)
    sorted_subgrids = sort_blocks(blocks)
    return merge_subgrids(sorted_subgrids, bg)
```