```python
from collections import Counter
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int, n: int) -> List[Tuple[int, int, int, int, bool]]:
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    all_comps = []
    for i in range(n):
        for j in range(n):
            if g[i][j] != bg and not visited[i][j]:
                min_r = max_r = i
                min_c = max_c = j
                has_e = False
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    if g[x][y] == 8:
                        has_e = True
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                all_comps.append((min_r, max_r, min_c, max_c, has_e))
    return all_comps

def group_into_blocks(comps: List[Tuple[int, int, int, int, bool]]) -> List[List[Tuple[int, int, int, int, bool]]]:
    if not comps:
        return []
    comps = sorted(comps, key=lambda x: x[0])
    blocks = []
    current_block = [comps[0]]
    cur_max_r = comps[0][1]
    for comp in comps[1:]:
        if comp[0] <= cur_max_r + 1:
            current_block.append(comp)
            cur_max_r = max(cur_max_r, comp[1])
        else:
            blocks.append(current_block)
            current_block = [comp]
            cur_max_r = comp[1]
    blocks.append(current_block)
    return blocks

def pack_block(g: List[List[int]], out: List[List[int]], block: List[Tuple[int, int, int, int, bool]], bg: int, n: int, is_left: bool):
    if not block:
        return
    block = sorted(block, key=lambda x: x[2])
    total_w = sum(x[3] - x[2] + 1 for x in block)
    curr_col = 0 if is_left else max(0, n - total_w)
    for comp in block:
        minr, maxr, minc, maxc, _ = comp
        w = maxc - minc + 1
        for r in range(minr, maxr + 1):
            for k in range(w):
                src_c = minc + k
                dst_c = curr_col + k
                if 0 <= dst_c < n:
                    nv = g[r][src_c]
                    if nv != bg:
                        out[r][dst_c] = nv
        curr_col += w

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = get_background(g)
    out = [[bg for _ in range(n)] for _ in range(n)]
    all_comps = find_components(g, bg, n)
    left_comps = [c for c in all_comps if c[4]]
    right_comps = [c for c in all_comps if not c[4]]
    left_blocks = group_into_blocks(left_comps)
    right_blocks = group_into_blocks(right_comps)
    for block in left_blocks:
        pack_block(g, out, block, bg, n, is_left=True)
    for block in right_blocks:
        pack_block(g, out, block, bg, n, is_left=False)
    return out
```