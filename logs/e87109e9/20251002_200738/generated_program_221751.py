```python
def get_background(g: List[List[int]]) -> int:
    return g[6][0]

def shift_and_fill(g: List[List[int]], background: int) -> List[List[int]]:
    h = len(g)
    w = len(g[0])
    out = [[background for _ in range(w)] for _ in range(h)]
    for i in range(18):
        for j in range(w):
            val = g[i + 6][j]
            if val != 5:
                out[i][j] = val
    return out

def find_seed_columns_and_max_row(g: List[List[int]]) -> tuple:
    h = len(g)
    w = len(g[0])
    seed_cols = set()
    max_row = -1
    for i in range(6, h):
        for j in range(w):
            if g[i][j] == 8:
                seed_cols.add(j)
                if i > max_row:
                    max_row = i
    return list(seed_cols), max_row - 6 if max_row >= 6 else -1

def expand_vertical(out: List[List[int]], seed_cols: list, background: int, max_row: int):
    if max_row < 0:
        return
    h = len(out)
    w = len(out[0])
    for j in seed_cols:
        for i in range(max_row + 1):
            if out[i][j] == background:
                out[i][j] = 8

def expand_sideways(out: List[List[int]], seed_cols: list, background: int, lower_row: int):
    if lower_row < 0 or not seed_cols:
        return
    h = len(out)
    w = len(out[0])
    left = min(seed_cols)
    right = max(seed_cols)
    # expand left
    j = left - 1
    while j >= 0 and out[lower_row][j] == background:
        out[lower_row][j] = 8
        j -= 1
    # expand right
    j = right + 1
    while j < w and out[lower_row][j] == background:
        out[lower_row][j] = 8
        j += 1

def program(g: List[List[int]]) -> List[List[int]]:
    background = get_background(g)
    out = shift_and_fill(g, background)
    seed_cols, lower_row = find_seed_columns_and_max_row(g)
    expand_vertical(out, seed_cols, background, lower_row)
    expand_sideways(out, seed_cols, background, lower_row)
    return out
```