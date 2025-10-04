```python
from typing import List
from collections import Counter

def find_best_period(inner: List[int]) -> int:
    n = len(inner)
    if n == 0:
        return 1
    best_p = 1
    best_score = 0
    for p in range(1, n // 2 + 2):
        score = sum(1 for i in range(n - p) if inner[i] == inner[i + p])
        if score > best_score:
            best_score = score
            best_p = p
    return best_p

def get_pattern(inner: List[int], p: int) -> List[int]:
    n = len(inner)
    pattern = [0] * p
    for r in range(p):
        pos_values = [inner[j] for j in range(r, n, p)]
        if pos_values:
            count = Counter(pos_values)
            most_common = count.most_common(1)[0][0]
            pattern[r] = most_common
    return pattern

def apply_pattern_to_row(out_row: List[int], start: int, end: int, pattern: List[int], p: int):
    for j in range(start, end + 1):
        idx = j - start
        out_row[j] = pattern[idx % p]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    for r in range(rows):
        start = 2
        end = cols - 3
        if end < start:
            continue
        inner = [g[r][c] for c in range(start, end + 1)]
        p = find_best_period(inner)
        pattern = get_pattern(inner, p)
        apply_pattern_to_row(out[r], start, end, pattern, p)
    return out
```