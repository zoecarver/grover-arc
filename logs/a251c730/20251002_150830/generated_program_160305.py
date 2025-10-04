```python
from typing import List
import collections

def find_candidates(g: List[List[int]]) -> List[Tuple[int, int, int, int]]:
    # Finds rows with longest consecutive same color >5, returns (row, b, start_col, end_col)
    candidates = []
    n = len(g)
    if n == 0:
        return candidates
    m = len(g[0])
    for r in range(n):
        curr_len = 0
        curr_start = -1
        curr_b = -1
        for c in range(m + 1):
            if c < m and g[r][c] == curr_b:
                curr_len += 1
            else:
                if curr_len > 5:
                    candidates.append((r, curr_b, curr_start, curr_start + curr_len - 1))
                if c < m:
                    curr_b = g[r][c]
                    curr_start = c
                    curr_len = 1
                else:
                    curr_len = 0
    return candidates

def get_frame_bounds(candidates: List[Tuple[int, int, int, int]]) -> tuple:
    # Groups by b, for each with >=2 cands, computes top=min row, bottom=max row, left=min start, right=max end, w=right-left+1, h=bottom-top+1
    # Skips if w == full m, chooses max len(cands), tie max w
    from collections import defaultdict
    groups = defaultdict(list)
    for tup in candidates:
        groups[tup[1]].append(tup)
    best_top = best_bottom = best_left = best_right = best_b = -1
    best_count = best_w = 0
    n = len(candidates)  # dummy full m
    m = 30  # assumed full width
    for b, cands in groups.items():
        if len(cands) < 2:
            continue
        cands.sort(key=lambda x: x[0])
        top = cands[0][0]
        bottom = cands[-1][0]
        l = min(c[2] for c in cands)
        r = max(c[3] for c in cands)
        w = r - l + 1
        if w == m:
            continue
        h = bottom - top + 1
        count = len(cands)
        if (count > best_count) or (count == best_count and w > best_w):
            best_count = count
            best_w = w
            best_top = top
            best_bottom = bottom
            best_left = l
            best_right = r
            best_b = b
    if best_top == -1:
        return None
    return best_top, best_bottom, best_left, best_right, best_b

def compute_fill(g: List[List[int]], left: int, right: int, top: int, bottom: int, b: int) -> int:
    # Most common non-b color in inner area
    inner_colors = []
    for r in range(top, bottom + 1):
        for c in range(left + 1, right):
            color = g[r][c]
            if color != b:
                inner_colors.append(color)
    if not inner_colors:
        return 1  # default
    counter = collections.Counter(inner_colors)
    return counter.most_common(1)[0][0]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    candidates = find_candidates(g)
    bounds = get_frame_bounds(candidates)
    if bounds is None:
        return []
    top, bottom, left, right, b = bounds
    height = bottom - top + 1
    width = right - left + 1
    f = compute_fill(g, left, right, top, bottom, b)
    output = []
    for i in range(height):
        r = top + i
        if i == 0 or i == height - 1:
            row = [3] * width
        else:
            row = g[r][left:right + 1][:]
            row[0] = 3
            row[-1] = 3
            inner = row[1:-1]
            if all(x == b for x in inner):
                inner = [f] * len(inner)
                row = [3] + inner + [3]
        output.append(row)
    return output
```