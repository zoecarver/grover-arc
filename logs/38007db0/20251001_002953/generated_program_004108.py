```python
from typing import List
from collections import Counter

def get_wall_positions(n: int) -> List[int]:
    if n <= 1:
        return [0]
    k = (n - 1) // 6
    if k == 0:
        return [0, n - 1]
    step = (n - 1) // k
    walls = [i * step for i in range(k + 1)]
    return walls

def identify_colors(g: List[List[int]]) -> tuple:
    b = g[0][0]
    g_color = g[1][1]
    s = None
    for row in g:
        for cell in row:
            if cell != b and cell != g_color:
                s = cell
                break
        if s is not None:
            break
    return b, g_color, s

def get_bay_patterns(row: List[int], walls: List[int]) -> List[List[int]]:
    patterns = []
    for i in range(len(walls) - 1):
        start = walls[i] + 1
        end = walls[i + 1]
        pattern = row[start:end]
        patterns.append(pattern)
    return patterns

def choose_pattern(patterns: List[List[int]], g: int, s: int) -> List[int]:
    if not patterns:
        return []
    pattern_tuples = [tuple(p) for p in patterns]
    count = Counter(pattern_tuples)
    if len(count) == 1:
        return list(pattern_tuples[0])
    odd = None
    majority = None
    for p_t, c in count.items():
        if c == 1:
            odd_candidate = list(p_t)
            if s in odd_candidate:
                odd = odd_candidate
        if c > 1:
            majority = list(p_t)
    if odd is not None:
        return odd
    return majority if majority is not None else list(pattern_tuples[0])

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    b, g_color, s = identify_colors(g)
    walls = get_wall_positions(n)
    out = []
    for row in g:
        patterns = get_bay_patterns(row, walls)
        chosen = choose_pattern(patterns, g_color, s)
        out_row = [b] + chosen + [b]
        out.append(out_row)
    return out
```