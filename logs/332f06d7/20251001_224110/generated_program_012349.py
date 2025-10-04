```python
from typing import List, Tuple

def find_largest_hole(grid: List[List[int]], n: int) -> Tuple[int, int, int]:
    k = 0
    hr, hc = -1, -1
    for size in range(n // 2, 0, -1):
        found = False
        for r in range(n - size + 1):
            for c in range(n - size + 1):
                is_empty = True
                for i in range(size):
                    for j in range(size):
                        if grid[r + i][c + j] != 0:
                            is_empty = False
                            break
                    if not is_empty:
                        break
                if not is_empty:
                    continue
                # Check adjacent to 1
                adjacent_1 = False
                # Top
                if r > 0:
                    for j in range(size):
                        if grid[r - 1][c + j] == 1:
                            adjacent_1 = True
                            break
                # Bottom
                if not adjacent_1 and r + size < n:
                    for j in range(size):
                        if grid[r + size][c + j] == 1:
                            adjacent_1 = True
                            break
                # Left
                if not adjacent_1 and c > 0:
                    for i in range(size):
                        if grid[r + i][c - 1] == 1:
                            adjacent_1 = True
                            break
                # Right
                if not adjacent_1 and c + size < n:
                    for i in range(size):
                        if grid[r + i][c + size] == 1:
                            adjacent_1 = True
                            break
                if adjacent_1:
                    k = size
                    hr, hc = r, c
                    found = True
                    break
            if found:
                break
        if found:
            break
    return k, hr, hc

def find_flippable_red(grid: List[List[int]], n: int, k: int) -> Tuple[int, int, int]:
    pr, pc = -1, -1
    for r in range(n - k + 1):
        for c in range(n - k + 1):
            is_red = True
            for i in range(k):
                for j in range(k):
                    if grid[r + i][c + j] != 2:
                        is_red = False
                        break
                if not is_red:
                    break
            if not is_red:
                continue
            # Check adjacent to 1
            adjacent_1 = False
            # Top
            if r > 0:
                for j in range(k):
                    if grid[r - 1][c + j] == 1:
                        adjacent_1 = True
                        break
            # Bottom
            if not adjacent_1 and r + k < n:
                for j in range(k):
                    if grid[r + k][c + j] == 1:
                        adjacent_1 = True
                        break
            # Left
            if not adjacent_1 and c > 0:
                for i in range(k):
                    if grid[r + i][c - 1] == 1:
                        adjacent_1 = True
                        break
            # Right
            if not adjacent_1 and c + k < n:
                for i in range(k):
                    if grid[r + i][c + k] == 1:
                        adjacent_1 = True
                        break
            if adjacent_1:
                touches_left = (c == 0)
                touches_bottom = (r + k - 1 == n - 1)
                if k == 1 or not (touches_left or touches_bottom):
                    pr, pc = r, c
                    return k, pr, pc, 2
    return 0, -1, -1, 0

def find_protruding_ones(grid: List[List[int]], n: int, k: int) -> Tuple[int, int, int]:
    pr, pc = -1, -1
    for r in range(n - k + 1):
        for c in range(n - k - 1):  # Ensure room for right check
            is_one = True
            for i in range(k):
                for j in range(k):
                    if grid[r + i][c + j] != 1:
                        is_one = False
                        break
                if not is_one:
                    break
            if not is_one:
                continue
            # Check right side all adjacent to 3
            right_adj_3 = True
            for i in range(k):
                if c + k >= n or grid[r + i][c + k] != 3:
                    right_adj_3 = False
                    break
            if right_adj_3:
                pr, pc = r, c
                return k, pr, pc
    return 0, -1, -1

def flip_block(grid: List[List[int]], r: int, c: int, k: int, new_val: int):
    for i in range(k):
        for j in range(k):
            grid[r + i][c + j] = new_val

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    n = len(grid)
    k, hr, hc = find_largest_hole(grid, n)
    if k == 0:
        return grid
    # Try to find red to flip
    rk, pr, pc, flip_val = find_flippable_red(grid, n, k)
    if rk > 0:
        flip_block(grid, pr, pc, k, 0)
    else:
        # Find protruding 1's
        pk, pr, pc = find_protruding_ones(grid, n, k)
        if pk > 0:
            flip_block(grid, pr, pc, k, 0)
    # Fill the hole
    if hr != -1 and hc != -1:
        flip_block(grid, hr, hc, k, 1)
    return grid
```