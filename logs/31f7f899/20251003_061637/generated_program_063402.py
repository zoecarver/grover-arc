```python
from typing import List

def find_center(g: List[List[int]]) -> int:
    n = len(g)
    for i in range(n):
        if 6 in g[i]:
            return i
    return n // 2

def d_for_one(j: int, center_row: List[int], n: int) -> int:
    count = 0
    k = j + 1
    while k < n and center_row[k] == 6:
        count += 1
        k += 1
    return 4 if count >= 3 else 1

def d_for_seven(j: int, one_positions: List[int]) -> int:
    adjacent = any(abs(k - j) == 1 for k in one_positions)
    return 3 if adjacent else 2

def d_for_two() -> int:
    return 2

def d_for_five(j: int) -> int:
    return 1 if j <= 2 else 2

def d_for_four() -> int:
    return 1

def d_for_nine(j: int, n: int) -> int:
    half = n // 2
    return 5 if j > half else 1

def compute_d(c: int, j: int, n: int, center_row: List[int], one_positions: List[int]) -> int:
    if c == 1:
        return d_for_one(j, center_row, n)
    elif c == 7:
        return d_for_seven(j, one_positions)
    elif c == 2:
        return d_for_two()
    elif c == 5:
        return d_for_five(j)
    elif c == 4:
        return d_for_four()
    elif c == 9:
        return d_for_nine(j, n)
    else:
        return 0

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    center = find_center(g)
    center_row = g[center]
    one_positions = [j for j in range(n) if center_row[j] == 1]
    output = [[8] * n for _ in range(n)]
    for j in range(n):
        output[center][j] = center_row[j]
    for j in range(n):
        c = center_row[j]
        if c == 8 or c == 6:
            continue
        d = compute_d(c, j, n, center_row, one_positions)
        start_row = max(0, center - d)
        end_row = min(n, center + d + 1)
        for i in range(start_row, end_row):
            output[i][j] = c
    return output
```