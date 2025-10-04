```python
from typing import List
from copy import deepcopy

def make_grid_copy(g: List[List[int]]) -> List[List[int]]:
    return deepcopy(g)

def get_sequence(grid: List[List[int]], r: int, start_c: int) -> tuple[int, List[int]]:
    seq = []
    c = start_c
    while c < 13 and grid[r][c] != 4:
        seq.append(grid[r][c])
        c += 1
    actual_start = c - len(seq)
    return actual_start, seq

def is_continuation(grid: List[List[int]], r: int, start_c: int, sequence: List[int]) -> bool:
    if r == 0:
        return False
    prev_start, prev_seq = get_sequence(grid, r - 1, start_c)
    return len(prev_seq) == len(sequence) and prev_seq == sequence and prev_start == start_c

def mirror_left_to_right(grid: List[List[int]]) -> List[List[int]]:
    for r in range(27):
        if r == 13:
            continue
        start_c, seq = get_sequence(grid, r, 0)
        if not seq:
            continue
        if is_continuation(grid, r, start_c, seq):
            continue
        len_seq = len(seq)
        end_left = start_c + len_seq - 1
        start_right = 26 - end_left
        if start_right < 14:
            continue
        reversed_seq = seq[::-1]
        overwrite = any(x in [1, 3, 9] for x in seq)
        for i in range(len_seq):
            d = start_right + i
            if grid[r][d] == 4 or overwrite:
                grid[r][d] = reversed_seq[i]
    return grid

def complete_right_two_with_three_prefix(grid: List[List[int]]) -> List[List[int]]:
    for r in range(27):
        if r == 13:
            continue
        # Skip if row has 9 on left
        if any(grid[r][c] == 9 for c in range(13)):
            continue
        c = 26
        while c >= 14:
            if grid[r][c] == 2:
                end = c
                start = c
                while start >= 14 and grid[r][start] == 2:
                    start -= 1
                k = end - start + 1
                prefix_start = start - k
                if prefix_start < 14:
                    c = start - 1
                    continue
                can_fill = all(grid[r][j] == 4 for j in range(prefix_start, start))
                if can_fill:
                    for j in range(prefix_start, start):
                        grid[r][j] = 3
                c = start - 1
            else:
                c -= 1
    return grid

def complete_left_two_with_three_suffix(grid: List[List[int]]) -> List[List[int]]:
    for r in range(27):
        if r == 13:
            continue
        c = 0
        while c < 12:
            if grid[r][c] == 2:
                start = c
                while c < 13 and grid[r][c] == 2:
                    c += 1
                k = c - start
                suffix_start = c
                if suffix_start + k - 1 > 12:
                    c = suffix_start
                    continue
                can_fill = all(grid[r][j] == 4 for j in range(suffix_start, suffix_start + k))
                if can_fill:
                    for j in range(suffix_start, suffix_start + k):
                        grid[r][j] = 3
                c = suffix_start + k - 1
            else:
                c += 1
    return grid

def extract_blobs(grid: List[List[int]], color: int) -> List[List[tuple[int, int]]]:
    rows, cols = 27, 27
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    for i in range(rows):
        if i == 13:
            continue
        for j in range(cols):
            if j == 13:
                continue
            if grid[i][j] == color and not visited[i][j]:
                blob = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    blob.append((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == color and not visited[nx][ny] and nx != 13 and ny != 13:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(blob) > 1:
                    blobs.append(blob)
    return blobs

def add_eight_blocks(grid: List[List[int]]) -> List[List[int]]:
    blobs = extract_blobs(grid, 2)
    for blob in blobs:
        if not blob:
            continue
        min_r = min(p[0] for p in blob)
        max_r = max(p[0] for p in blob)
        min_c = min(p[1] for p in blob)
        max_c = max(p[1] for p in blob)
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        if h * w != len(blob):
            continue  # only rectangular
        if max_r < 13:  # upper
            add_h = h - 1 if h > 1 else 0
            for i in range(add_h):
                add_r = min_r - 1 - i
                if add_r < 0:
                    break
                for j in range(min_c, max_c + 1):
                    if grid[add_r][j] == 4:
                        grid[add_r][j] = 8
        else:  # lower
            for i in range(h):
                add_r = max_r + 1 + i
                if add_r >= 27:
                    break
                for j in range(min_c, max_c + 1):
                    if grid[add_r][j] == 4:
                        grid[add_r][j] = 8
    return grid

def complete_rectangular_two_blobs(grid: List[List[int]]) -> List[List[int]]:
    # For left
    blobs = extract_blobs(grid, 2)
    for blob in blobs:
        min_r = min(p[0] for p in blob)
        max_r = max(p[0] for p in blob)
        min_c = min(p[1] for p in blob)
        max_c = max(p[1] for p in blob)
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        if h * w == len(blob) and min_c >= 0 and max_c < 13 and w % 2 == 0 and w >= 2:
            num9 = w // 2
            num1 = w
            # Fill 9's left
            for rr in range(min_r, max_r + 1):
                for i in range(num9):
                    cc = min_c - 1 - i
                    if cc >= 0 and grid[rr][cc] == 4:
                        grid[rr][cc] = 9
                for i in range(num1):
                    cc = max_c + 1 + i
                    if cc < 13 and grid[rr][cc] == 4:
                        grid[rr][cc] = 1
    # For right symmetric
    for blob in blobs:
        min_r = min(p[0] for p in blob)
        max_r = max(p[0] for p in blob)
        min_c = min(p[1] for p in blob)
        max_c = max(p[1] for p in blob)
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        if h * w == len(blob) and min_c >= 14 and max_c < 27 and w % 2 == 0 and w >= 2:
            num9 = w // 2
            num1 = w
            # Fill 9's right outer
            for rr in range(min_r, max_r + 1):
                for i in range(num9):
                    cc = max_c + 1 + i
                    if cc < 27 and grid[rr][cc] == 4:
                        grid[rr][cc] = 9
                for i in range(num1):
                    cc = min_c - 1 - i
                    if cc >= 14 and grid[rr][cc] == 4:
                        grid[rr][cc] = 1
    return grid

def program(g: List[List[int]]) -> List[List[int]]:
    grid = make_grid_copy(g)
    grid = complete_rectangular_two_blobs(grid)
    grid = complete_left_two_with_three_suffix(grid)
    grid = mirror_left_to_right(grid)
    grid = complete_right_two_with_three_prefix(grid)
    grid = add_eight_blocks(grid)
    return grid
```