```python
from typing import List

def remove_misplaced_ones(grid: List[List[int]], r: int):
    row = grid[r]
    n = len(row)
    i = 0
    while i < n:
        if row[i] == 0:
            i += 1
            continue
        start = i
        has_9 = False
        has_1 = False
        j = i
        while j < n and row[j] != 0:
            if row[j] == 9:
                has_9 = True
            if row[j] == 1:
                has_1 = True
            j += 1
        if has_9 and has_1:
            for k in range(start, j):
                if row[k] == 1:
                    row[k] = 0
        i = j

def fill_gaps(grid: List[List[int]], r: int):
    row = grid[r]
    n = len(row)
    i = 0
    while i < n - 1:
        if row[i] == 0 or row[i] == 1 or row[i] == 9:
            i += 1
            continue
        C = row[i]
        # k=1
        if i + 2 < n and row[i + 1] == 0 and row[i + 2] == C:
            row[i + 1] = 1
            i += 2
            continue
        # k=2
        if i + 4 < n and row[i + 1] == 0 and row[i + 2] == 0 and row[i + 3] == C and row[i + 4] == 1:
            row[i + 1] = 1
            row[i + 2] = 1
            i += 3
            continue
        i += 1

def process_one_runs(grid: List[List[int]], r: int):
    row = grid[r]
    n = len(row)
    i = 0
    while i < n:
        if row[i] != 1 or (i > 0 and row[i - 1] == 1):
            i += 1
            continue
        # start of run
        j = i
        while j < n and row[j] == 1:
            j += 1
        run_left = i
        run_right = j - 1
        left_pos = run_left - 1
        if left_pos >= 0 and row[left_pos] != 0:
            i = run_right + 1
            continue
        # count l
        l = 0
        pos = left_pos
        while pos >= 0 and row[pos] == 0:
            l += 1
            pos -= 1
        hit = pos
        if l > 3 or hit < 0:
            # remove
            for k in range(run_left, run_right + 1):
                row[k] = 0
        else:
            # fill
            for k in range(hit + 1, left_pos + 1):
                row[k] = 1
        i = run_right + 1

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    h = len(out)
    if h == 0:
        return out
    w = len(out[0])
    for r in range(h):
        remove_misplaced_ones(out, r)
        fill_gaps(out, r)
        process_one_runs(out, r)
    return out
```