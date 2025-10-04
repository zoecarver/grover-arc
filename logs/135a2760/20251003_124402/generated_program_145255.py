```python
from collections import Counter
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    if not g:
        return out
    n = len(g[0])
    h = len(g)
    if h == 0 or n < 4:
        return out
    b = g[0][0]
    i = g[1][1] if h > 1 else b
    s = b
    for r in range(h):
        row = g[r]
        is_full_border = all(x == b for x in row)
        if is_full_border:
            continue
        out[r][1] = i
        out[r][n - 2] = i
        m = n - 4
        if m <= 0:
            continue
        pattern_start = 2
        pattern_end = 2 + m
        input_pattern = row[pattern_start:pattern_end]
        color_counts = {}
        for c in input_pattern:
            if c != i and c != b:
                color_counts[c] = color_counts.get(c, 0) + 1
        if not color_counts:
            continue
        p = max(color_counts, key=color_counts.get)
        run_lengths = []
        current_run = 0
        for col in range(pattern_start, pattern_end):
            if row[col] == p:
                current_run += 1
            else:
                if current_run > 0:
                    run_lengths.append(current_run)
                current_run = 0
        if current_run > 0:
            run_lengths.append(current_run)
        if not run_lengths:
            continue
        run_counter = Counter(run_lengths)
        most_common = run_counter.most_common(1)[0]
        k = most_common[0]
        if len(run_counter) > 1 and run_counter.most_common(2)[1][1] == most_common[1]:
            k = max(run_lengths)
        period = k + 1
        min_diffs = float('inf')
        best_seq = [i] * m
        for j in range(period):
            seq = []
            for ii in range(m):
                pos = (ii + j) % period
                seq.append(p if pos < k else s)
            diffs = sum(a != bb for a, bb in zip(seq, input_pattern))
            if diffs < min_diffs:
                min_diffs = diffs
                best_seq = seq
        for ii in range(m):
            out[r][pattern_start + ii] = best_seq[ii]
    return out
```