```python
from typing import List

def has_non_zero(row: List[int]) -> bool:
    return any(c != 0 for c in row)

def find_longest_block(g: List[List[int]]) -> tuple[int, int]:
    n = len(g)
    max_len = 0
    current_len = 0
    best_start = 0
    best_end = 0
    for i in range(n):
        if has_non_zero(g[i]):
            current_len += 1
            if current_len > max_len:
                max_len = current_len
                best_start = i - current_len + 1
                best_end = i
        else:
            current_len = 0
    return best_start, best_end

def find_min_col(g: List[List[int]], start: int, end: int) -> int:
    min_j = 20
    for i in range(start, end + 1):
        for j in range(20):
            if g[i][j] != 0:
                min_j = min(min_j, j)
                break
    return min_j

def find_max_col(g: List[List[int]], start: int, end: int) -> int:
    max_j = -1
    for i in range(start, end + 1):
        for j in range(19, -1, -1):
            if g[i][j] != 0:
                max_j = max(max_j, j)
                break
    return max_j

def program(g: List[List[int]]) -> List[List[int]]:
    start, end = find_longest_block(g)
    h = end - start + 1
    min_c = find_min_col(g, start, end)
    max_c = find_max_col(g, start, end)
    w = max_c - min_c + 1
    result = []
    for i in range(start, end + 1):
        row = g[i][min_c : min_c + w]
        result.append(row)
    return result
```