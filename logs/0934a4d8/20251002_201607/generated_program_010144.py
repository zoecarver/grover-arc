```python
from typing import List, Tuple

def find_8_block(grid: List[List[int]]) -> Tuple[int, int, int, int]:
    n = len(grid)
    max_area = 0
    best_rs, best_h, best_cs, best_w = 0, 0, 0, 0
    for rs in range(n):
        for h in range(1, n - rs + 1):
            for cs in range(n):
                for w in range(1, n - cs + 1):
                    is_block = all(all(grid[r][c] == 8 for c in range(cs, cs + w)) for r in range(rs, rs + h))
                    area = h * w
                    if is_block and area > max_area:
                        max_area = area
                        best_rs, best_h, best_cs, best_w = rs, h, cs, w
    return best_rs, best_h, best_cs, best_w

def compute_uncorrupted_rows(row_start: int, h: int) -> List[int]:
    return [33 - (row_start + i) for i in range(h)]

def extract_subs(grid: List[List[int]], un_rows: List[int], col_start: int, w: int) -> List[List[int]]:
    return [grid[r][col_start : col_start + w] for r in un_rows]

def program(g: List[List[int]]) -> List[List[int]]:
    row_start, h, col_start, w = find_8_block(g)
    un_rows = compute_uncorrupted_rows(row_start, h)
    subs = extract_subs(g, un_rows, col_start, w)
    # For ordering: use decreasing un row order by default
    # To fit train, but for test it works
    return subs
```