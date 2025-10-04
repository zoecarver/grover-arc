```python
from typing import List
from copy import deepcopy

def make_grid_copy(g: List[List[int]]) -> List[List[int]]:
    return deepcopy(g)

def is_continuation(g: List[List[int]], r: int, start: int, seq: List[int]) -> bool:
    if r == 0:
        return False
    prev_start = start
    prev_seq = []
    c = prev_start
    while c < 13 and g[r - 1][c] != 4:
        prev_seq.append(g[r - 1][c])
        c += 1
    return len(prev_seq) == len(seq) and prev_seq == seq and (c - len(prev_seq) == start)

def mirror_left_to_right(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    for r in range(27):
        if r == 13:
            continue
        c = 0
        while c < 13:
            if g[r][c] == 4:
                c += 1
                continue
            start = c
            seq = []
            while c < 13 and g[r][c] != 4:
                seq.append(g[r][c])
                c += 1
            length = len(seq)
            if length < 2:
                continue
            target_start = 26 - (start + length - 1)
            if target_start < 14 or target_start + length - 1 > 26:
                continue
            rev_seq = seq[::-1]
            conflict = False
            has_non_four = False
            for i in range(length):
                tc = target_start + i
                tv = g[r][tc]
                if tv != 4:
                    has_non_four = True
                    if tv != rev_seq[i]:
                        conflict = True
                        break
            if conflict:
                continue
            if not has_non_four:
                if is_continuation(g, r, start, seq):
                    continue
            for i in range(length):
                tc = target_start + i
                if g[r][tc] == 4:
                    g[r][tc] = rev_seq[i]
    return g

def vertical_propagate_up_upper(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    for r in range(1, 13):
        for c in range(27):
            if c == 13 or r == 13:
                continue
            if g[r - 1][c] == 4 and g[r][c] != 4:
                g[r - 1][c] = g[r][c]
    return g

def complete_two_runs(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    for r in range(27):
        if r == 13:
            continue
        # Left side (columns 0-12)
        c = 0
        while c < 13:
            if g[r][c] != 2:
                c += 1
                continue
            run_start = c
            k = 0
            while c < 13 and g[r][c] == 2:
                k += 1
                c += 1
            if k < 1:
                continue
            # Check if isolated: left adjacent 4 or bound, right adjacent 4 or bound
            left_adj = (run_start == 0 or g[r][run_start - 1] == 4)
            right_adj = (c == 13 or g[r][c] == 4)
            if not left_adj or not right_adj:
                continue
            # 9/1 for even k >=2
            if k >= 2 and k % 2 == 0:
                num9 = k // 2
                p_start = run_start - num9
                can_prefix9 = p_start >= 0 and all(g[r][p_start + i] == 4 for i in range(num9))
                if can_prefix9:
                    for i in range(num9):
                        g[r][p_start + i] = 9
                num1 = k
                s_start = c
                can_suffix1 = s_start + num1 - 1 < 13 and all(g[r][s_start + i] == 4 for i in range(num1))
                if can_suffix1:
                    for i in range(num1):
                        g[r][s_start + i] = 1
            # 3 suffix for odd k or k=1
            if k % 2 == 1 or k == 1:
                s_start3 = c
                can_suffix3 = s_start3 + k - 1 < 13 and all(g[r][s_start3 + i] == 4 for i in range(k))
                if can_suffix3:
                    for i in range(k):
                        g[r][s_start3 + i] = 3
        # Right side (columns 14-26)
        c = 14
        while c < 27:
            if g[r][c] != 2:
                c += 1
                continue
            run_start = c
            k = 0
            while c < 27 and g[r][c] == 2:
                k += 1
                c += 1
            if k < 1:
                continue
            left_adj = (run_start == 14 or g[r][run_start - 1] == 4)
            right_adj = (c == 27 or g[r][c] == 4)
            if not left_adj or not right_adj:
                continue
            # 1/9 for even k >=2
            if k >= 2 and k % 2 == 0:
                num1 = k
                p_start1 = run_start - num1
                can_prefix1 = p_start1 >= 14 and all(g[r][p_start1 + i] == 4 for i in range(num1))
                if can_prefix1:
                    for i in range(num1):
                        g[r][p_start1 + i] = 1
                num9 = k // 2
                s_start9 = c
                can_suffix9 = s_start9 + num9 - 1 <= 26 and all(g[r][s_start9 + i] == 4 for i in range(num9))
                if can_suffix9:
                    for i in range(num9):
                        g[r][s_start9 + i] = 9
            # 3 prefix for odd k or k=1
            if k % 2 == 1 or k == 1:
                p_start3 = run_start - k
                can_prefix3 = p_start3 >= 14 and all(g[r][p_start3 + i] == 4 for i in range(k))
                if can_prefix3:
                    for i in range(k):
                        g[r][p_start3 + i] = 3
    return g

def extract_blobs(g: List[List[int]], color: int) -> List[List[Tuple[int, int]]]:
    rows, cols = 27, 27
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        if i == 13:
            continue
        for j in range(cols):
            if j == 13:
                continue
            if g[i][j] == color and not visited[i][j]:
                blob = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    blob.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and g[nx][ny] == color and not visited[nx][ny] and nx != 13 and ny != 13:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(blob) >= 1:  # include singles for 2
                    blobs.append(blob)
    return blobs

def is_rectangular(blob: List[Tuple[int, int]]) -> bool:
    if not blob:
        return False
    min_r = min(p[0] for p in blob)
    max_r = max(p[0] for p in blob)
    min_c = min(p[1] for p in blob)
    max_c = max(p[1] for p in blob)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    return len(blob) == h * w

def extend_two_blobs_with_eights(g: List[List[int]]) -> List[List[int]]:
    g = make_grid_copy(g)
    blobs = extract_blobs(g, 2)
    for blob in blobs:
        if not is_rectangular(blob):
            continue
        positions = set(blob)
        min_r = min(p[0] for p in blob)
        max_r = max(p[0] for p in blob)
        min_c = min(p[1] for p in blob)
        max_c = max(p[1] for p in blob)
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        if min_r < 13:  # upper, extend up
            ext_min_r = min_r - h
            if ext_min_r < 0:
                continue
            can_extend = True
            for er in range(ext_min_r, min_r):
                for ec in range(min_c, max_c + 1):
                    if (er, ec) not in positions and g[er][ec] not in (4, 8):
                        can_extend = False
                        break
                if not can_extend:
                    break
            if can_extend:
                for er in range(ext_min_r, min_r):
                    for ec in range(min_c, max_c + 1):
                        g[er][ec] = 8
        else:  # lower, extend down
            ext_max_r = max_r + h
            if ext_max_r > 26:
                continue
            can_extend = True
            for er in range(max_r + 1, ext_max_r + 1):
                for ec in range(min_c, max_c + 1):
                    if g[er][ec] not in (4, 8):
                        can_extend = False
                        break
                if not can_extend:
                    break
            if can_extend:
                for er in range(max_r + 1, ext_max_r + 1):
                    for ec in range(min_c, max_c + 1):
                        g[er][ec] = 8
    return g

def program(g: List[List[int]]) -> List[List[int]]:
    g = mirror_left_to_right(g)
    g = vertical_propagate_up_upper(g)
    g = complete_two_runs(g)
    g = extend_two_blobs_with_eights(g)
    return g
```