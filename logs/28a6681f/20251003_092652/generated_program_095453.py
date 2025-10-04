```python
from typing import List

def remove_misplaced_ones(grid: List[List[int]], r: int):
    # Scans row for non-0 sequences; if contains both 9 and 1, zeros out all 1s in that sequence.
    # Helpful for cleaning invalid fillers near boundaries; works well in training 1/3 but misses in 2 where 1s should persist.
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
    # Fills specific 0-gaps between matching Cs (non-0/1/9), for k=1: C-0-C -> C-1-C; for k=2: C-0-0-C -> C-1-1-C.
    # Partially helpful for simple connections but too rigid—misses longer gaps or patterns without trailing 1, leading to under-filling in complex rows.
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
        if i + 3 < n and row[i + 1] == 0 and row[i + 2] == 0 and row[i + 3] == C:
            row[i + 1] = 1
            row[i + 2] = 1
            i += 3
            continue
        i += 1

def process_one_runs(grid: List[List[int]], r: int):
    # Finds isolated 1-runs; if left-adjacent is non-0 and left 0-gap <=3, fills gap with 1s; else removes run.
    # Useful for validating/expanding fillers but buggy on gap counting (starts from run-left-1) and hit boundary, causing incorrect removals in training 2.
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
    for r in range(10):
        remove_misplaced_ones(out, r)
    for r in range(10):
        fill_gaps(out, r)
    for r in range(10):
        process_one_runs(out, r)
    return out
```