```python
from collections import Counter
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    num_rows = len(g)
    num_cols = len(g[0])
    B = g[0][0]
    border_cols = [c for c in range(num_cols) if all(g[r][c] == B for r in range(num_rows))]
    if len(border_cols) < 2:
        return [[B] * num_cols for _ in range(num_rows)]  # degenerate case, return original borders
    M = border_cols[1] - border_cols[0] - 1
    num_panels = len(border_cols) - 1
    output = []
    for r in range(num_rows):
        patterns = []
        for k in range(num_panels):
            start = border_cols[k] + 1
            pat = tuple(g[r][start + j] for j in range(M))
            patterns.append(pat)
        freq = Counter(patterns)
        singletons = [pat for pat, cnt in freq.items() if cnt == 1]
        if len(singletons) == 1:
            chosen = singletons[0]
        else:
            chosen = patterns[-1]
        out_row = [B] + list(chosen) + [B]
        output.append(out_row)
    return output
```