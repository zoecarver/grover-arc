```python
from typing import List, Tuple

def fill(width: int, runs: List[Tuple[int, int]], mod_offset: int = 0) -> List[int]:
    if not runs:
        return [0] * width
    c, n = runs[0]
    pattern = [0] * width
    slot_indices: List[int] = []
    for i in range(width):
        if (i % n) == mod_offset:
            pattern[i] = c
        else:
            slot_indices.append(i)
    if len(runs) > 1:
        sub_runs = runs[1:]
        next_n = sub_runs[0][1]
        sub_offset = (n - 1) % next_n
        sub_pattern = fill(len(slot_indices), sub_runs, sub_offset)
        for j, idx in enumerate(slot_indices):
            pattern[idx] = sub_pattern[j]
    return pattern

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    num_rows = len(g)
    cols = len(g[0])
    # Find r from first row
    r = next((i for i, val in enumerate(g[0]) if val != 0), None)
    if r is None:
        return [row[:] for row in g]
    result = [row[:] for row in g]
    for row_idx in range(num_rows):
        row = g[row_idx]
        # Build runs: closest first
        runs: List[Tuple[int, int]] = []
        i = r - 1
        while i >= 0:
            if row[i] == 0:
                i -= 1
                continue
            c = row[i]
            n = 1
            i -= 1
            while i >= 0 and row[i] == c:
                n += 1
                i -= 1
            runs.append((c, n))
        w = cols - r - 1
        right = fill(w, runs, 0)
        for j in range(w):
            result[row_idx][r + 1 + j] = right[j]
    return result
```