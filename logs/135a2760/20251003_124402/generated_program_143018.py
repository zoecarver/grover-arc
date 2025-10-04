```python
from typing import List
from collections import Counter

def get_best_pattern(inner: List[int], C: int, F: int, L: int) -> List[int]:
    best_pattern = inner[:]
    min_changes = float('inf')
    max_prefix = -1
    for k in range(1, L // 2 + 2):
        U = [C] * k + [F]
        ulen = len(U)
        if ulen > L:
            continue
        for s in range(ulen):
            cycled = U[s:] + U[:s]
            pattern = cycled * (L // ulen) + cycled[: L % ulen]
            changes = sum(1 for j in range(L) if pattern[j] != inner[j])
            pref = 0
            while pref < L and pattern[pref] == inner[pref]:
                pref += 1
            if changes < min_changes or (changes == min_changes and pref > max_prefix):
                min_changes = changes
                max_prefix = pref
                best_pattern = pattern
    return best_pattern

def find_frame_color(g: List[List[int]]) -> int:
    h = len(g)
    if h < 3:
        return g[0][1] if g else 0
    col1_counts = Counter(g[r][1] for r in range(1, h - 1))
    return col1_counts.most_common(1)[0][0]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h, w = len(g), len(g[0])
    outer_color = g[0][0]
    frame_color = find_frame_color(g)
    out = [row[:] for row in g]
    for r in range(h):
        if 1 < w - 1 and g[r][1] == frame_color and g[r][w - 2] == frame_color:
            inner_start = 2
            inner_len = w - 4
            if inner_len <= 0:
                continue
            inner = g[r][inner_start: inner_start + inner_len]
            L = inner_len
            color_count = Counter(inner)
            if outer_color in color_count:
                del color_count[outer_color]
            if frame_color in color_count:
                del color_count[frame_color]
            if not color_count:
                continue
            C = color_count.most_common(1)[0][0]
            F = outer_color
            best = get_best_pattern(inner, C, F, L)
            out[r][inner_start: inner_start + L] = best
    return out
```