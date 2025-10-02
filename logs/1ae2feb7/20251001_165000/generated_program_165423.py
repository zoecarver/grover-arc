```python
from typing import List, Tuple

def find_wall(g: List[List[int]]) -> int:
    rows = len(g)
    if rows == 0:
        return -1
    cols = len(g[0])
    candidates = []
    for j in range(cols):
        non_zeros = set(g[r][j] for r in range(rows) if g[r][j] != 0)
        if len(non_zeros) == 1:
            candidates.append(j)
    # Assume exactly one such column
    return candidates[0]

def get_blocks(row: List[int], wall: int) -> List[Tuple[int, int]]:
    blocks = []
    i = 0
    left_end = wall - 1
    while i <= left_end:
        if row[i] == 0:
            i += 1
            continue
        c = row[i]
        start = i
        i += 1
        while i <= left_end and row[i] == c:
            i += 1
        n = i - start
        blocks.append((c, n))
    return blocks

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    wall = find_wall(g)
    output = [row[:] for row in g]
    num_rows = len(g)
    num_cols = len(g[0])
    for r in range(num_rows):
        blocks = get_blocks(g[r], wall)
        right_start = wall + 1
        if right_start >= num_cols:
            continue
        right_end = num_cols - 1
        for c, n in blocks:
            pos = right_start
            while pos <= right_end:
                output[r][pos] = c
                pos += n
    return output
```