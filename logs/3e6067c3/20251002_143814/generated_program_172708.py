```python
from typing import List, Tuple, Dict
from copy import deepcopy
from collections import defaultdict, deque

def find_key_row(g: List[List[int]], h: int, w: int) -> int:
    for r in range(h - 1, -1, -1):
        count_clues = sum(1 for cell in g[r] if 2 <= cell <= 9)
        if 3 <= count_clues <= 12:
            runs = 0
            in_run = False
            for cell in g[r]:
                if 2 <= cell <= 9:
                    if not in_run:
                        runs += 1
                        in_run = True
                else:
                    in_run = False
            if runs == count_clues:
                return r
    return h - 2

def extract_sequence(g: List[List[int]], key_row: int) -> List[int]:
    return [cell for cell in g[key_row] if 2 <= cell <= 9]

def find_connected_blocks(g: List[List[int]]) -> Dict[int, List[Tuple[int, int, int, int]]]:
    h = len(g)
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    blocks: Dict[int, List[Tuple[int, int, int, int]]] = defaultdict(list)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            cell = g[i][j]
            if 2 <= cell <= 9 and not visited[i][j]:
                min_r = max_r = i
                min_c = max_c = j
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == cell:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                blocks[cell].append((min_r, max_r, min_c, max_c))
    for c in blocks:
        blocks[c].sort(key=lambda b: (b[0], b[2]))
    return blocks

def fill_gap_horizontal(g: List[List[int]], b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int], c1: int, bg: int):
    minr1, maxr1, minc1, maxc1 = b1
    minr2, maxr2, minc2, maxc2 = b2
    olap_r_start = max(minr1, minr2)
    olap_r_end = min(maxr1, maxr2)
    if olap_r_start > olap_r_end:
        return
    if maxc1 < minc2:
        gap_start_c = maxc1 + 1
        gap_end_c = minc2 - 1
    elif maxc2 < minc1:
        gap_start_c = maxc2 + 1
        gap_end_c = minc1 - 1
    else:
        return
    if gap_start_c > gap_end_c:
        return
    for r in range(olap_r_start, olap_r_end + 1):
        for c in range(gap_start_c, gap_end_c + 1):
            if g[r][c] == bg:
                g[r][c] = c1

def fill_gap_vertical(g: List[List[int]], b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int], c1: int, bg: int):
    minr1, maxr1, minc1, maxc1 = b1
    minr2, maxr2, minc2, maxc2 = b2
    olap_c_start = max(minc1, minc2)
    olap_c_end = min(maxc1, maxc2)
    if olap_c_start > olap_c_end:
        return
    if maxr1 < minr2:
        gap_start_r = maxr1 + 1
        gap_end_r = minr2 - 1
    elif maxr2 < minr1:
        gap_start_r = maxr2 + 1
        gap_end_r = minr1 - 1
    else:
        return
    if gap_start_r > gap_end_r:
        return
    for c in range(olap_c_start, olap_c_end + 1):
        for r in range(gap_start_r, gap_end_r + 1):
            if g[r][c] == bg:
                g[r][c] = c1

def program(g: List[List[int]]) -> List[List[int]]:
    g = deepcopy(g)
    if not g or not g[0]:
        return g
    h = len(g)
    w = len(g[0])
    key_row = find_key_row(g, h, w)
    seq = extract_sequence(g, key_row)
    blocks = find_connected_blocks(g)
    available = {c: deque(blocks.get(c, [])) for c in set(seq)}
    bg = 8
    for i in range(len(seq) - 1):
        c1 = seq[i]
        c2 = seq[i + 1]
        if c1 not in available or not available[c1] or c2 not in available or not available[c2]:
            continue
        b1 = available[c1].popleft()
        b2 = available[c2].popleft()
        minr1, maxr1, minc1, maxc1 = b1
        minr2, maxr2, minc2, maxc2 = b2
        olap_r = max(0, min(maxr1, maxr2) - max(minr1, minr2) + 1)
        olap_c = max(0, min(maxc1, maxc2) - max(minc1, minc2) + 1)
        if olap_r > 0 and olap_c == 0:
            fill_gap_horizontal(g, b1, b2, c1, bg)
        elif olap_c > 0 and olap_r == 0:
            fill_gap_vertical(g, b1, b2, c1, bg)
    return g
```