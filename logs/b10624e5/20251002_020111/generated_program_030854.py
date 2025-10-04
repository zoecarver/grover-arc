```python
from typing import List
from copy import deepcopy

def make_grid_copy(g: List[List[int]]) -> List[List[int]]:
    return deepcopy(g)

def get_sequence(grid: List[List[int]], r: int, start_c: int) -> List[int]:
    seq = []
    c = start_c
    while c < 13 and grid[r][c] != 4:
        seq.append(grid[r][c])
        c += 1
    return seq

def is_continuation(grid: List[List[int]], r: int, i: int, sequence: List[int]) -> bool:
    if r == 0:
        return False
    prev_seq = get_sequence(grid, r - 1, i)
    return len(prev_seq) == len(sequence) and prev_seq == sequence

def mirror_left_to_right(grid: List[List[int]]):
    for r in range(27):
        if r == 13:
            continue
        i = 0
        while i < 13:
            if grid[r][i] == 4:
                i += 1
                continue
            j = i
            sequence = []
            while j < 13 and grid[r][j] != 4:
                sequence.append(grid[r][j])
                j += 1
            len_s = len(sequence)
            if len_s < 1:
                i = j
                continue
            t_start = 26 - (j - 1)
            rev_s = sequence[::-1]
            # Check conflict and partial
            conflict = False
            has_partial = False
            for k in range(len_s):
                c = t_start + k
                expected = rev_s[k]
                if grid[r][c] != 4:
                    if grid[r][c] != expected:
                        conflict = True
                    else:
                        has_partial = True
            if conflict:
                i = j
                continue
            fill = False
            if not is_continuation(grid, r, i, sequence):
                fill = True
            elif has_partial:
                fill = True
            if fill:
                for k in range(len_s):
                    c = t_start + k
                    if grid[r][c] == 4:
                        grid[r][c] = rev_s[k]
            # Extension up for same color length >=2 new sequences, skip if color ==1
            if not is_continuation(grid, r, i, sequence) and len_s >= 2 and all(x == sequence[0] for x in sequence) and sequence[0] != 1:
                if r > 0:
                    for k in range(len_s):
                        c = t_start + k
                        expected = rev_s[k]
                        if grid[r - 1][c] == 4:
                            grid[r - 1][c] = expected
            i = j

def complete_two_runs_with_three_prefix(grid: List[List[int]]):
    for r in range(14, 27):
        i = 14
        while i < 27:
            if grid[r][i] != 2:
                i += 1
                continue
            j = i
            while j < 27 and grid[r][j] == 2:
                j += 1
            len_s = j - i
            if len_s >= 2:
                for p in range(len_s):
                    c = i - 1 - p
                    if c >= 14 and grid[r][c] == 4:
                        grid[r][c] = 3
            i = j

def add_eight_block_below_two_blob(grid: List[List[int]]):
    blobs = extract_blobs(grid, 2)
    for blob in blobs:
        positions = [pos for pos in blob if pos[1] > 13 and pos[0] > 13]
        if not positions:
            continue
        rows_min = min(p[0] for p in positions)
        rows_max = max(p[0] for p in positions)
        cols_min = min(p[1] for p in positions)
        cols_max = max(p[1] for p in positions)
        h = rows_max - rows_min + 1
        l = cols_max - cols_min + 1
        for dr in range(1, h + 1):
            rr = rows_max + dr
            if rr >= 27:
                break
            for dc in range(l):
                cc = cols_min + dc
                if grid[rr][cc] == 4:
                    grid[rr][cc] = 8
        # Partial on left for first row of eight block
        first_rr = rows_max + 1
        if first_rr < 27 and grid[first_rr][3] == 4:
            grid[first_rr][3] = 8

def complete_partial_left_two(grid: List[List[int]]):
    for r in range(14, 27):
        for c in range(12):
            if grid[r][c] == 2 and grid[r][c + 1] == 4:
                grid[r][c + 1] = 3

def extract_blobs(g: List[List[int]], color: int) -> List[List[Tuple[int, int]]]:
    rows, cols = len(g), len(g[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    blobs = []
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == color and not visited[i][j] and not (j == 13 or i == 13):
                blob = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    blob.append((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == color and not visited[nx][ny] and not (ny == 13 or nx == 13):
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(blob) > 1:
                    blobs.append(blob)
    return blobs

def program(g: List[List[int]]) -> List[List[int]]:
    grid = make_grid_copy(g)
    mirror_left_to_right(grid)
    complete_two_runs_with_three_prefix(grid)
    add_eight_block_below_two_blob(grid)
    complete_partial_left_two(grid)
    return grid
```