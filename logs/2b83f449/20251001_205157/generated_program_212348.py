```python
from typing import List

def process_content_row(row: List[int]) -> None:
    j = 0
    w = len(row)
    while j < w - 2:
        if row[j] == 7 and row[j + 1] == 7 and row[j + 2] == 7:
            row[j] = 8
            row[j + 1] = 6
            row[j + 2] = 8
            j += 3
        else:
            j += 1

def get_six_positions(row: List[int]) -> set[int]:
    return {j for j in range(len(row)) if row[j] == 6}

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    m = len(g)
    w = len(g[0])
    out = [row[:] for row in g]
    for i in range(1, m, 2):
        process_content_row(out[i])
    for i in range(0, m, 2):
        input_row = g[i]
        for j in range(w):
            if input_row[j] != 0:
                out[i][j] = 8
        above_six = set() if i == 0 else get_six_positions(out[i - 1])
        below_six = set() if i == m - 1 else get_six_positions(out[i + 1])
        all_six = above_six | below_six
        for j in all_six:
            if out[i][j] == 8:
                out[i][j] = 6
        if i == 0:
            continue
        if i == m - 1:
            j = 0
            while j < w:
                if out[i][j] == 0:
                    j += 1
                    continue
                s = j
                has6 = False
                while j < w and out[i][j] != 0:
                    if out[i][j] == 6:
                        has6 = True
                    j += 1
                e = j
                if has6:
                    if out[i][s] == 8:
                        out[i][s] = 3
                    if e == w and out[i][w - 1] == 8:
                        out[i][w - 1] = 3
        else:
            j = 0
            while j < w:
                if out[i][j] == 0:
                    j += 1
                    continue
                s = j
                has6 = False
                while j < w and out[i][j] != 0:
                    if out[i][j] == 6:
                        has6 = True
                    j += 1
                e = j
                if has6:
                    if s > 0 and out[i][s - 1] == 0 and out[i][s] == 8:
                        out[i][s] = 3
                    if e < w and out[i][e] == 0 and out[i][e - 1] == 8:
                        out[i][e - 1] = 3
            min_a = min(above_six) if above_six else float('inf')
            min_b = min(below_six) if below_six else float('inf')
            max_a = max(above_six) if above_six else float('-inf')
            max_b = max(below_six) if below_six else float('-inf')
            if min_a < min_b:
                if out[i][0] == 8:
                    out[i][0] = 3
                if min_a <= 4 and w > 1 and out[i][1] == 8:
                    out[i][1] = 3
            if max_a > max_b:
                if out[i][w - 1] == 8:
                    out[i][w - 1] = 3
                dist = w - 1 - max_a
                if dist <= 4 and w > 1 and out[i][w - 2] == 8:
                    out[i][w - 2] = 3
    return out
```