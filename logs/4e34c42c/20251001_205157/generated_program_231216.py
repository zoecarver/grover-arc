```python
from typing import List, Tuple
from collections import Counter, defaultdict

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int]]]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(h):
        for c in range(w):
            if g[r][c] != bg and not visited[r][c]:
                comp = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    comp.append((cr, cc))
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and g[nr][nc] != bg:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                components.append(comp)
    return components

def get_bbox(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0
    min_r = min(pos[0] for pos in comp)
    max_r = max(pos[0] for pos in comp)
    min_c = min(pos[1] for pos in comp)
    max_c = max(pos[1] for pos in comp)
    return min_r, max_r, min_c, max_c

def has_hole(min_r: int, max_r: int, min_c: int, max_c: int, num_non_bg: int) -> bool:
    total_cells = (max_r - min_r + 1) * (max_c - min_c + 1)
    return total_cells > num_non_bg

def trim_columns(sub: List[List[int]], bg: int) -> List[List[int]]:
    rows = len(sub)
    if rows == 0:
        return sub
    cols = len(sub[0]) if sub[0] else 0
    if cols == 0:
        return sub
    left = 0
    while left < cols and all(sub[r][left] == bg for r in range(rows)):
        left += 1
    right = cols - 1
    while right >= left and all(sub[r][right] == bg for r in range(rows)):
        right -= 1
    if left > right:
        return [[bg] for _ in range(rows)]
    return [row[left : right + 1] for row in sub]

def is_left_framed(sub: List[List[int]], bg: int) -> Tuple[bool, int]:
    if len(sub) < 5 or not sub[0]:
        return False, -1
    non_bg_cols = [j for j, val in enumerate(sub[0]) if val != bg]
    if len(non_bg_cols) == 1:
        f = non_bg_cols[0]
        if sub[4][f] != bg:
            return True, f
    return False, -1

def is_right_framed(sub: List[List[int]], bg: int) -> Tuple[bool, int]:
    if len(sub) < 5 or not sub[0]:
        return False, -1
    non_bg_cols = [j for j, val in enumerate(sub[0]) if val != bg]
    if len(non_bg_cols) == 1:
        f = non_bg_cols[0]
        if f == len(sub[0]) - 1 and sub[4][f] != bg:
            return True, f
    return False, -1

def extract_and_normalize(comp: List[Tuple[int, int]], g: List[List[int]], bg: int) -> Tuple[int, int, List[List[int]]]:
    num_non_bg = len(comp)
    min_r, max_r, min_c, max_c = get_bbox(comp)
    h = max_r - min_r + 1
    if h not in (3, 5) or not has_hole(min_r, max_r, min_c, max_c, num_non_bg):
        return -1, -1, []
    raw_sub = [[g[r][c] for c in range(min_c, max_c + 1)] for r in range(min_r, max_r + 1)]
    trimmed = trim_columns(raw_sub, bg)
    if not trimmed or not trimmed[0]:
        return min_r, max_r, []
    if h == 3:
        pad_row = [bg] * len(trimmed[0])
        padded = [[bg] * len(trimmed[0])] + trimmed + [[bg] * len(trimmed[0])]
        sub = padded
    else:
        framed_left, f_left = is_left_framed(trimmed, bg)
        temp = [row[f_left + 1 :] for row in trimmed] if framed_left else trimmed
        temp = trim_columns(temp, bg)
        framed_right, f_right = is_right_framed(temp, bg)
        sub = [row[:f_right] for row in temp] if framed_right else temp
        sub = trim_columns(sub, bg)
    if not sub or not sub[0]:
        return min_r, max_r, []
    return min_r, max_r, sub

def compute_max_overlap(strip: List[List[int]], next_sub: List[List[int]]) -> int:
    if not strip or not next_sub or not strip[0] or not next_sub[0]:
        return 0
    w1 = len(strip[0])
    w2 = len(next_sub[0])
    max_k = min(w1, w2)
    for k in range(max_k, -1, -1):
        match = True
        for r in range(5):
            for j in range(k):
                if strip[r][w1 - k + j] != next_sub[r][j]:
                    match = False
                    break
            if not match:
                break
        if match:
            return k
    return 0

def merge_subgrids(subgrids: List[List[List[int]]], bg: int) -> List[List[int]]:
    if not subgrids:
        return [[bg] for _ in range(5)]
    strip = [row[:] for row in subgrids[0]]
    for nxt in subgrids[1:]:
        k = compute_max_overlap(strip, nxt)
        for r in range(5):
            strip[r].extend(nxt[r][k:])
    return strip

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    comps = find_components(g, bg)
    slabs = []
    for comp in comps:
        min_r, max_r, sub = extract_and_normalize(comp, g, bg)
        if sub:
            slabs.append((max_r, min_r, min_c? Wait, need min_c for sorting, but in extract I returned min_r max_r sub, but need original min_c
Wait, fix: in extract_and_normalize return original min_r, max_r, original min_c, sub

Wait, adjust:

In extract_and_normalize, return min_r, max_r, min_c, sub

Yes, add min_c to return.

Then slabs.append( (max_r, min_c, sub) )  # for sorting -max_r, min_c

No, sort key=(-max_r, min_c)

Yes.

In function:

def extract_and_normalize(comp: List[Tuple[int, int]], g: List[List[int]], bg: int) -> Tuple[int, int, int, List[List[int]]]:
    ... 
    min_r, max_r, min_c, max_c = get_bbox(comp)
    ...
    # at end
    return min_r, max_r, min_c, sub

Then in program:

    slabs = []
    for comp in comps:
        min_r, max_r, orig_min_c, sub = extract_and_normalize(comp, g, bg)
        if sub and len(sub[0]) > 0:
            slabs.append((max_r, orig_min_c, sub))

    slabs.sort(key=lambda x: (-x[0], x[1]))

    subgrids = [slab[2] for slab in slabs]

    output = merge_subgrids(subgrids, bg)
    return output
```