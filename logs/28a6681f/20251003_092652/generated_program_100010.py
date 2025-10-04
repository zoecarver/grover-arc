```python
from typing import List

def remove_misplaced_ones(grid: List[List[int]], r: int) -> None:
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

def fill_gaps(grid: List[List[int]], r: int) -> None:
    row = grid[r]
    n = len(row)
    i = 0
    while i < n:
        while i < n and row[i] in {0, 1, 9}:
            i += 1
        if i >= n:
            break
        C = row[i]
        j = i
        while j < n and row[j] == C:
            j += 1
        i = j
        gap_start = i
        gap_len = 0
        while i < n and row[i] == 0:
            gap_len += 1
            i += 1
        if gap_len <= 3 and i < n and row[i] == C:
            for pos in range(gap_start, i):
                row[pos] = 1
        # if not, i is already advanced

def process_one_runs(grid: List[List[int]], r: int) -> None:
    row = grid[r]
    n = len(row)
    i = 0
    while i < n:
        if row[i] != 1 or (i > 0 and row[i - 1] == 1):
            i += 1
            continue
        j = i
        while j < n and row[j] == 1:
            j += 1
        run_left = i
        run_right = j - 1
        left_pos = run_left - 1
        if left_pos >= 0 and row[left_pos] != 0:
            i = j
            continue
        l = 0
        pos = left_pos
        while pos >= 0 and row[pos] == 0:
            l += 1
            pos -= 1
        hit = pos
        if l > 3 or hit < 0:
            for k in range(run_left, run_right + 1):
                row[k] = 0
        else:
            for k in range(hit + 1, left_pos + 1):
                row[k] = 1
        i = j

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    for r in range(10):
        remove_misplaced_ones(out, r)
        fill_gaps(out, r)
        process_one_runs(out, r)
    return out
```