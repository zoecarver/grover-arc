```python
from typing import List, Tuple

def find_candidates(g: List[List[int]]) -> List[Tuple[int, int, int]]:
    candidates = []
    for r in range(30):
        max_len = 0
        best_start = -1
        best_end = -1
        curr_len = 0
        curr_start = -1
        for c in range(31):
            if c < 30 and g[r][c] == 3:
                if curr_len == 0:
                    curr_start = c
                curr_len += 1
            else:
                if curr_len > max_len:
                    max_len = curr_len
                    best_start = curr_start
                    best_end = curr_start + curr_len - 1
                curr_len = 0
        if max_len > 5:
            candidates.append((r, best_start, best_end))
    return candidates

def extract_frame(g: List[List[int]], top: int, left: int, right: int, bottom: int) -> List[List[int]]:
    out = []
    for r in range(top, bottom + 1):
        row = [g[r][c] for c in range(left, right + 1)]
        if len(row) > 1:
            row[0] = 3
            row[-1] = 3
        out.append(row)
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    candidates = find_candidates(g)
    if len(candidates) < 2:
        return []
    top_r, l1, r1 = candidates[0]
    bot_r, l2, r2 = candidates[-1]
    l = max(l1, l2)
    r = min(r1, r2)
    if l > r:
        return []
    return extract_frame(g, top_r, l, r, bot_r)
```