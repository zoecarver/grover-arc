```python
from typing import List, Tuple
from collections import Counter

def count_colors(g: List[List[int]]) -> dict:
    flat = [cell for row in g for cell in row]
    return dict(Counter(flat))

def find_global_bg(counts: dict) -> int:
    return max(counts, key=counts.get)

def find_max_run_length(g: List[List[int]], color: int) -> int:
    max_len = 0
    for row in g:
        curr = 0
        for cell in row:
            if cell == color:
                curr += 1
                max_len = max(max_len, curr)
            else:
                curr = 0
    return max_len

def find_run_start(g: List[List[int]], color: int, length: int) -> Tuple[int, int]:
    n = len(g)
    for r in range(n):
        curr = 0
        start = -1
        for c in range(n):
            if g[r][c] == color:
                if curr == 0:
                    start = c
                curr += 1
                if curr == length:
                    return r, start
            else:
                curr = 0
    return -1, -1

def find_largest_deco(g: List[List[int]], G: int, C: int) -> int:
    counts = count_colors(g)
    max_a = 0
    d = 0
    for color in counts:
        if color == G or color == C:
            continue
        a = counts[color]
        if a > max_a:
            max_a = a
            d = color
    return d

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    counts = count_colors(g)
    G = find_global_bg(counts)
    max_s = 0
    C = 0
    for color in counts:
        if color == G:
            continue
        s = find_max_run_length(g, color)
        if s > max_s:
            max_s = s
            C = color
    S = max_s
    if S == 0:
        return []
    r, c = find_run_start(g, C, S)
    if r == -1:
        return [[C for _ in range(S)] for _ in range(S)]
    # Find the starting row for the block
    min_r = n
    max_r = -1
    for rr in range(n):
        has_c = any(g[rr][cc] == C for cc in range(c, c + S))
        if has_c:
            min_r = min(min_r, rr)
            max_r = max(max_r, rr)
    r_start = min_r
    # Extract subgrid (crop to S rows from min_r)
    sub = [g[r_start + i][c : c + S] for i in range(S)]
    # Find largest deco color
    deco = find_largest_deco(g, G, C)
    # Create output
    output = [[C for _ in range(S)] for _ in range(S)]
    for i in range(S):
        for j in range(S):
            if sub[i][j] == G:
                output[i][j] = deco
    return output
```