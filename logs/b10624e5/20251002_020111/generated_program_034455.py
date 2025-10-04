```python
from typing import List, Tuple
from copy import deepcopy

def make_grid_copy(g: List[List[int]]) -> List[List[int]]:
    return deepcopy(g)

def get_left_run(grid: List[List[int]], r: int) -> Tuple[int, List[int]]:
    seq = []
    c = 0
    while c < 13 and grid[r][c] != 4:
        seq.append(grid[r][c])
        c += 1
    return c - len(seq), seq

def is_continuation(grid: List[List[int]], r: int) -> bool:
    if r == 0:
        return False
    prev_start, prev_seq = get_left_run(grid, r - 1)
    curr_start, curr_seq = get_left_run(grid, r)
    return prev_start == curr_start and prev_seq == curr_seq

def mirror_left_to_right(grid: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(grid)
    for r in range(27):
        if r == 13:
            continue
        start_c, seq = get_left_run(g, r)
        if len(seq) < 2 or is_continuation(g, r):
            continue
        # Check if target has at least one matching non-4
        sym_start = 26 - (start_c + len(seq) - 1)
        has_match = False
        for j in range(len(seq)):
            sym_c = sym_start + j
            expected = seq[len(seq) - 1 - j]
            if 14 <= sym_c <= 26 and g[r][sym_c] != 4 and g[r][sym_c] == expected:
                has_match = True
                break
        if not has_match:
            continue
        # Fill 4's
        for j in range(len(seq)):
            sym_c = sym_start + j
            if 14 <= sym_c <= 26 and g[r][sym_c] == 4:
                g[r][sym_c] = seq[len(seq) - 1 - j]
    return g

def complete_2_runs_with_3(grid: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(grid)
    # Left: suffix 3's after 2 run
    for r in range(27):
        if r == 13:
            continue
        c = 0
        while c < 13:
            if g[r][c] == 2:
                k = 0
                start = c
                while c < 13 and g[r][c] == 2:
                    k += 1
                    c += 1
                can_fill = True
                for i in range(k):
                    p = c + i
                    if p >= 13 or g[r][p] != 4:
                        can_fill = False
                        break
                if can_fill:
                    for i in range(k):
                        g[r][c + i] = 3
                c += k - 1  # adjust
            else:
                c += 1
    # Right: prefix 3's before 2 run
    for r in range(27):
        if r == 13:
            continue
        c = 14
        while c <= 26:
            if g[r][c] == 2 and (c == 14 or g[r][c - 1] != 2):
                k = 0
                run_start = c
                while c <= 26 and g[r][c] == 2:
                    k += 1
                    c += 1
                prefix_start = run_start - k
                can_fill = prefix_start >= 14 and all(g[r][p] == 4 for p in range(prefix_start, run_start))
                if can_fill:
                    for p in range(prefix_start, run_start):
                        g[r][p] = 3
                c = run_start + k - 1
            else:
                c += 1
    return g

def complete_uniform_2_with_9_1_left(grid: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(grid)
    for r in range(27):
        if r == 13:
            continue
        c = 0
        while c < 13:
            if g[r][c] == 2:
                k = 0
                start2 = c
                while c < 13 and g[r][c] == 2:
                    k += 1
                    c += 1
                if k >= 2 and k % 2 == 0:
                    num9 = k // 2
                    p_start = start2 - num9
                    if p_start >= 0 and all(g[r][p] == 4 for p in range(p_start, start2)):
                        for p in range(p_start, start2):
                            g[r][p] = 9
                    s_start = c
                    s_end = s_start + k
                    if all(g[r][p] == 4 for p in range(s_start, min(s_end, 13))):
                        for p in range(s_start, min(s_end, 13)):
                            g[r][p] = 1
            else:
                c += 1
    return g

def complete_2_run_right_with_1_9(grid: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(grid)
    for r in range(27):
        if r == 13:
            continue
        c = 14
        while c <= 26:
            if g[r][c] == 2 and (c == 14 or g[r][c - 1] != 2):
                k = 0
                run_start = c
                while c <= 26 and g[r][c] == 2:
                    k += 1
                    c += 1
                if k >= 2 and k % 2 == 0:
                    num9 = k // 2
                    ones_start = run_start - k
                    if ones_start >= 14 and all(g[r][p] == 4 for p in range(ones_start, run_start)):
                        for p in range(ones_start, run_start):
                            g[r][p] = 1
                    nines_start = run_start + k - 1 + 1
                    if all(g[r][p] == 4 for p in range(nines_start, nines_start + num9) if nines_start + num9 - 1 <= 26):
                        for p in range(nines_start, min(nines_start + num9, 27)):
                            g[r][p] = 9
                c = run_start + k - 1
            else:
                c += 1
    return g

def propagate_vertical(grid: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(grid)
    # Up propagation (fill above from below)
    for r in range(1, 27):
        for c in range(27):
            if r == 13 or c == 13:
                continue
            if g[r - 1][c] == 4 and g[r][c] != 4:
                g[r - 1][c] = g[r][c]
    # Down propagation (fill below from above)
    for r in range(26):
        for c in range(27):
            if r == 13 or c == 13:
                continue
            if g[r][c] != 4 and g[r + 1][c] == 4:
                g[r + 1][c] = g[r][c]
    return g

def extract_blobs(g: List[List[int]], color: int) -> List[List[Tuple[int, int]]]:
    rows, cols = 27, 27
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] == color and not visited[i][j] and i != 13 and j != 13:
                blob = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    blob.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == color and not visited[nx][ny] and nx != 13 and ny != 13:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(blob) > 1 or (len(blob) == 1 and color == 2):  # include singles for 2
                    blobs.append(blob)
    return blobs

def extend_2_with_8(grid: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(grid)
    blobs = extract_blobs(g, 2)
    for blob in blobs:
        positions = blob
        min_r = min(r for r, c in positions)
        max_r = max(r for r, c in positions)
        min_c = min(c for r, c in positions)
        max_c = max(c for r, c in positions)
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        if len(positions) != height * width:
            continue  # only rectangular
        avg_c = sum(c for _, c in positions) / len(positions)
        is_left = avg_c < 13.5
        is_upper = min_r < 13
        if is_upper:
            # extend above for upper blobs
            ext_start_r = min_r - height
            if ext_start_r < 0:
                continue
            can_extend = True
            for dr in range(height):
                er = ext_start_r + dr
                for dc in range(width):
                    ec = min_c + dc
                    if g[er][ec] != 4 and g[er][ec] != 8:
                        can_extend = False
            if can_extend:
                for dr in range(height):
                    er = ext_start_r + dr
                    for dc in range(width):
                        ec = min_c + dc
                        if g[er][ec] == 4:
                            g[er][ec] = 8
        else:
            # extend below for lower blobs
            ext_start_r = max_r + 1
            ext_end_r = ext_start_r + height - 1
            if ext_end_r > 26:
                continue  # cannot full, skip for now
            can_extend = True
            for dr in range(height):
                er = ext_start_r + dr
                for dc in range(width):
                    ec = min_c + dc
                    if g[er][ec] != 4:
                        can_extend = False
            if can_extend:
                for dr in range(height):
                    er = ext_start_r + dr
                    for dc in range(width):
                        ec = min_c + dc
                        g[er][ec] = 8
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    grid = make_grid_copy(g)
    grid = mirror_left_to_right(grid)
    grid = complete_uniform_2_with_9_1_left(grid)
    grid = complete_2_run_right_with_1_9(grid)
    grid = complete_2_runs_with_3(grid)
    grid = propagate_vertical(grid)
    grid = extend_2_with_8(grid)
    return grid
```