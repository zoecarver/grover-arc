```python
from typing import List

def remove_misplaced_ones(grid: List[List[int]], r: int) -> None:
    # Rule: In each contiguous non-zero sequence in the row, if both 9 and 1 are present, set all 1s in that sequence to 0.
    # This cleans invalid 1s adjacent to or mixed with boundary markers (9s).
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
    # Rule: Fill short gaps (1 to 3 zeros) between identical non-0/1/9 values (C) with 1s.
    # Patterns: C-0-C -> C-1-C; C-0-0-C -> C-1-1-C; C-0-0-0-C -> C-1-1-1-C.
    # This completes interrupted runs of the same object/color horizontally.
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
        # k=3
        if i + 4 < n and row[i + 1] == 0 and row[i + 2] == 0 and row[i + 3] == 0 and row[i + 4] == C:
            row[i + 1] = 1
            row[i + 2] = 1
            row[i + 3] = 1
            i += 4
            continue
        i += 1

def process_one_runs(grid: List[List[int]], r: int) -> None:
    # Rule: For each run of consecutive 1s, if immediately adjacent left to a non-0 or has a left gap of <=3 zeros to a non-0 (bounded left), fill the gap with 1s to connect; else, remove the entire run by setting to 0s.
    # This validates and extends short 1-runs (connectors/fillers) leftward to stable objects, removes isolated/unbounded ones.
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
    # Composes the rules: Copy input, then per row apply removal of misplaced 1s, gap filling between matching objects, and validation/extension of 1-runs.
    # All operations are row-independent, producing a cleaned grid with completed short connections and removed invalid fillers.
    out = [row[:] for row in g]
    for r in range(10):
        remove_misplaced_ones(out, r)
        fill_gaps(out, r)
        process_one_runs(out, r)
    return out
```