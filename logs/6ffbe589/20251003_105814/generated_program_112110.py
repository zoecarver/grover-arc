```python
from typing import List

def count_nonzeros(row: List[int]) -> int:
    return sum(1 for x in row if x != 0)

def get_span(row: List[int]) -> int:
    n = len(row)
    first = None
    for i in range(n):
        if row[i] != 0:
            first = i
            break
    if first is None:
        return 0
    last = None
    for i in range(n - 1, -1, -1):
        if row[i] != 0:
            last = i
            break
    return last - first + 1 if last is not None else 0

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    spans = [get_span(row) for row in g]
    max_s = max(spans) if spans else 0
    size = max_s
    max_rows = [i for i, s in enumerate(spans) if s == max_s]
    min_first = n
    for r in max_rows:
        for c in range(n):
            if g[r][c] != 0:
                min_first = min(min_first, c)
                break
    left = min_first
    right = left + size - 1
    counts = [count_nonzeros(row) for row in g]
    best_start = 0
    best_sum = 0
    for start in range(n - size + 1):
        curr_sum = sum(counts[start:start + size])
        if curr_sum > best_sum:
            best_sum = curr_sum
            best_start = start
    output = []
    for r in range(best_start, best_start + size):
        row_out = g[r][left:right + 1]
        if len(row_out) < size:
            row_out += [0] * (size - len(row_out))
        output.append(row_out)
    return output
```