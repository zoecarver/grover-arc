```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def is_full(row: List[int], color: int, left: int, right: int, bg: int) -> bool:
    if left < 0 or right >= len(row):
        return False
    for k in range(left, right + 1):
        if row[k] != color:
            return False
    return True

def compute_component_size(grid: List[List[int]], si: int, sj: int, color: int) -> Tuple[int, set]:
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    if si < 0 or si >= h or sj < 0 or sj >= w or grid[si][sj] != color:
        return 0, set()
    visited = set()
    stack = [(si, sj)]
    visited.add((si, sj))
    size = 1
    while stack:
        x, y = stack.pop()
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == color and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((nx, ny))
                size += 1
    return size, visited

def find_legs(row: List[int], bg: int) -> List[Tuple[int, int, int]]:
    res = []
    n = len(row)
    i = 0
    while i < n - 9:
        if row[i] == bg:
            i += 1
            continue
        c = row[i]
        start = i
        i += 1
        while i < n and row[i] == bg:
            i += 1
        if i >= n or row[i] != c:
            i = start + 1
            continue
        right = i
        clean = True
        for k in range(start + 1, right):
            if row[k] != bg:
                clean = False
                break
        if not clean:
            i = right + 1
            continue
        j = i + 1
        if j < n and row[j] == c:
            i = j + 1
            continue
        len_span = right - start + 1
        if len_span >= 10:
            res.append((start, right, c))
        i = j
    return res

def get_k(c: int, l: int, s: int) -> int:
    if c == 1:
        return 4 - l
    if c == 2:
        return 1 if s == 1 else 2
    if c == 3:
        return 1
    if c == 8:
        return 6
    return c // 2 + 1

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    output = [[bg] * w for _ in range(h)]
    for s in range(h - 4):
        legs1 = find_legs(g[s + 1], bg)
        legs2 = find_legs(g[s + 2], bg)
        legs3 = find_legs(g[s + 3], bg)
        set1 = set(legs1)
        set2 = set(legs2)
        set3 = set(legs3)
        common = set1 & set2 & set3
        for l, r, c in common:
            if not is_full(g[s], c, l, r, bg):
                continue
            if not is_full(g[s + 4], c, l, r, bg):
                continue
            effective_r = l + 10
            k = get_k(c, l, s)
            # top
            for j in range(l, r + 1):
                output[s][j] = c
            # bottom
            for j in range(l, r + 1):
                output[s + 4][j] = c
            # middle rows
            for mid in range(1, 4):
                row_idx = s + mid
                output[row_idx][l] = c
                if mid != 2:
                    output[row_idx][r] = c
                else:
                    output[row_idx][effective_r] = c
            # pattern in central
            mid_row = s + 2
            pos = effective_r
            count = 0
            while count < k and pos >= l:
                output[mid_row][pos] = c
                pos -= 2
                count += 1
    # remove small components
    flat_visited = set()
    for i in range(h):
        for j in range(w):
            if output[i][j] != bg and (i, j) not in flat_visited:
                size, comp = compute_component_size(output, i, j, output[i][j])
                if size < 20:
                    for x, y in comp:
                        output[x][y] = bg
                flat_visited.update(comp)
    return output
```