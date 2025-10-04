```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    five_positions = [(r, c) for r in range(rows) for c in range(cols) if g[r][c] == 5]
    if not five_positions:
        return []
    min_r = min(r for r, c in five_positions)
    max_r = max(r for r, c in five_positions)
    min_c_5 = min(c for r, c in five_positions)
    max_c_5 = max(c for r, c in five_positions)
    h = max_r - min_r + 1
    w = max_c_5 - min_c_5 + 1
    # find c: leftmost >=2 !=5 in region rows, else global
    found = False
    min_col = float('inf')
    chosen_c = 0
    for r in range(min_r, max_r + 1):
        for j in range(cols):
            val = g[r][j]
            if val >= 2 and val != 5 and j < min_col:
                min_col = j
                chosen_c = val
                found = True
                break
        if found:
            break
    if not found:
        for r in range(rows):
            for j in range(cols):
                val = g[r][j]
                if val >= 2 and val != 5 and j < min_col:
                    min_col = j
                    chosen_c = val
                    found = True
                    break
            if found:
                break
    c = chosen_c if found else 0
    if w == 2:
        def get_pair(cleaned_row: List[int]) -> List[int]:
            n = len(cleaned_row)
            groups = []
            i = 0
            while i < n:
                if cleaned_row[i] == 0:
                    i += 1
                    continue
                start = i
                i += 1
                while i < n and cleaned_row[i] != 0:
                    i += 1
                len_g = i - start
                if len_g >= 2:
                    left = cleaned_row[start]
                    right = cleaned_row[i - 1]
                    groups.append((left, right))
            if groups:
                return [groups[0][0], groups[-1][1]]
            else:
                nz_js = [j for j in range(n) if cleaned_row[j] > 0]
                if not nz_js:
                    return [0, 0]
                minj = min(nz_js)
                maxj = max(nz_js)
                return [cleaned_row[minj], cleaned_row[maxj]]
        output = []
        for i in range(h):
            row_idx = min_r + i
            cleaned = [0 if x == 5 else x for x in g[row_idx]]
            pair = get_pair(cleaned)
            output.append(pair)
        return output
    else:
        output = []
        for i in range(h):
            if i % 2 == 0:
                row = [c] * w
            else:
                if w <= 3:
                    row = [c] + [0] * (w - 2) + [c] if w >= 2 else [c]
                else:
                    row = [c] + [0] * (w - 1)
            output.append(row)
        return output
```