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
    return candidates[0] if candidates else -1

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
    output = [row[:] for row in g]
    rows = len(g)
    if rows == 0:
        return output
    cols = len(g[0])
    wall = find_wall(g)
    if wall < 0 or wall >= cols - 1:
        return output
    right_start = wall + 1
    right_len = cols - right_start
    for r in range(rows):
        blocks = get_blocks(g[r], wall)
        for pos in range(right_start, cols):
            output[r][pos] = 0
        for block in reversed(blocks):
            c, n = block
            for i in range(right_len):
                pos = right_start + i
                if i % n == 0 and output[r][pos] == 0:
                    output[r][pos] = c
    return output
```