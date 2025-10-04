```python
from typing import List
from collections import defaultdict
import copy

def process_line(line: List[int], n: int):
    pos_by_c = defaultdict(list)
    for i in range(n):
        if line[i] != 0:
            pos_by_c[line[i]].append(i)
    for c in list(pos_by_c):
        poss = pos_by_c[c]
        if len(poss) != 2:
            continue
        p1, p2 = sorted(poss)
        d = p2 - p1
        if d == 0:
            continue
        # Extend right (increasing indices)
        chain_right = set([p1, p2])
        current = p2
        while True:
            nextp = current + d
            if nextp >= n:
                break
            if line[nextp] == 0 or line[nextp] == c:
                line[nextp] = c
                chain_right.add(nextp)
                current = nextp
            else:
                conflict_c = line[nextp]
                for pp in chain_right:
                    line[pp] = conflict_c
                break
        # Extend left (decreasing indices)
        chain_left = set([p1, p2])
        current = p1
        while True:
            nextp = current - d
            if nextp < 0:
                break
            if line[nextp] == 0 or line[nextp] == c:
                line[nextp] = c
                chain_left.add(nextp)
                current = nextp
            else:
                conflict_c = line[nextp]
                for pp in chain_left:
                    line[pp] = conflict_c
                break

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    num_rows = len(g)
    num_cols = len(g[0]) if num_rows > 0 else 0
    grid = copy.deepcopy(g)
    if num_rows > num_cols:
        # Process horizontal (rows)
        for i in range(num_rows):
            process_line(grid[i], num_cols)
    else:
        # Process vertical (columns)
        for j in range(num_cols):
            col = [grid[i][j] for i in range(num_rows)]
            process_line(col, num_rows)
            for i in range(num_rows):
                grid[i][j] = col[i]
    return grid
```