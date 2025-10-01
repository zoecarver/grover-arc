```python
import typing as tp
from collections import Counter

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g:
        return []
    H = len(g)
    W = len(g[0]) if g else 0
    if W == 0:
        return [[] for _ in range(H)]
    B = g[0][0]
    # Find border columns
    border_cols = [c for c in range(W) if all(g[r][c] == B for r in range(H))]
    if not border_cols:
        # Fallback, treat whole as one panel or something, but assume exists
        return [[B] * W for _ in range(H)]
    out = []
    for r in range(H):
        inners = []
        for i in range(len(border_cols) - 1):
            start = border_cols[i] + 1
            end = border_cols[i + 1] - 1
            if start > end:
                inner = ()
            else:
                inner = tuple(g[r][j] for j in range(start, end + 1))
            inners.append(inner)
        if not inners:
            out.append([B])
            continue
        count = Counter(inners)
        chosen_panel = 0
        # Check for exactly one unique sequence when there are multiples
        uniques = [(seq, idx) for idx, seq in enumerate(inners) if count[seq] == 1]
        if len(uniques) == 1 and len(count) > 1:
            chosen_panel = uniques[0][1]
        else:
            # Choose the most common, take the first occurrence
            most_common_seq = count.most_common(1)[0][0]
            for idx, seq in enumerate(inners):
                if seq == most_common_seq:
                    chosen_panel = idx
                    break
        # Extract the full panel slice
        left = border_cols[chosen_panel]
        right = border_cols[chosen_panel + 1]
        row_out = g[r][left:right + 1]
        out.append(row_out)
    return out
```