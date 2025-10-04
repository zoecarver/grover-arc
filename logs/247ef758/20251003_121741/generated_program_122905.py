```python
from typing import List, Set, Tuple

def find_stem(g: List[List[int]]) -> Tuple[int, int]:
    H = len(g)
    if H == 0:
        raise ValueError("Empty grid")
    W = len(g[0])
    for col in range(W):
        col_colors = [row[col] for row in g]
        first = col_colors[0]
        if first != 0 and all(c == first for c in col_colors):
            return col, first
    raise ValueError("No stem column found")

def find_base_colors(g: List[List[int]], stem_col: int) -> Set[int]:
    H = len(g)
    W = len(g[0])
    left_colors: Set[int] = set()
    right_colors: Set[int] = set()
    for i in range(H):
        for col in range(stem_col):
            c = g[i][col]
            if c != 0:
                left_colors.add(c)
        for col in range(stem_col, W):
            c = g[i][col]
            if c != 0:
                right_colors.add(c)
    return left_colors - right_colors

def clean_left_columns(g: List[List[int]], stem_col: int, base_colors: Set[int]) -> List[List[int]]:
    H = len(g)
    W = len(g[0])
    out = [row[:] for row in g]
    for i in range(H):
        for col in range(stem_col):
            if out[i][col] not in base_colors:
                out[i][col] = 0
    return out

def enforce_stem_column(g: List[List[int]], stem_col: int, stem_color: int) -> List[List[int]]:
    H = len(g)
    out = [row[:] for row in g]
    for i in range(H):
        out[i][stem_col] = stem_color
    return out

def process_top_and_bottom(g: List[List[int]], stem_col: int) -> List[List[int]]:
    H = len(g)
    out = [row[:] for row in g]
    for i in [0, H - 1]:
        # Already cleaned and stemmed in previous steps
        pass  # Keep the rest as is
    return out

def process_middle_rows(g: List[List[int]], stem_col: int, stem_color: int) -> List[List[int]]:
    H = len(g)
    W = len(g[0])
    out = [row[:] for row in g]
    branch_col = stem_col + 1
    for i in range(1, H - 1):
        if branch_col < W:
            C = out[i][branch_col]
        else:
            C = 0
        # Zero columns from branch_col + 1 to W - 2
        for col in range(branch_col + 1, W - 1):
            out[i][col] = 0
        # Set last column to C
        out[i][W - 1] = C
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    stem_col, stem_color = find_stem(g)
    base_colors = find_base_colors(g, stem_col)
    out = clean_left_columns(g, stem_col, base_colors)
    out = enforce_stem_column(out, stem_col, stem_color)
    # Top and bottom keep their middle parts
    out = process_top_and_bottom(out, stem_col)
    # Middle rows zero middle parts and set last
    out = process_middle_rows(out, stem_col, stem_color)
    return out
```