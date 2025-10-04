```python
from typing import List, Tuple
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    flat = [cell for row in g for cell in row]
    bg = Counter(flat).most_common(1)[0][0]
    visited = [[False] * n for _ in range(n)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    all_comps: List[Tuple[int, int, int, int, bool]] = []
    for i in range(n):
        for j in range(n):
            if g[i][j] != bg and not visited[i][j]:
                min_r = max_r = i
                min_c = max_c = j
                has_e = False
                stack = [(i, j)]
                visited[i][j] = True
                positions = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    if g[x][y] == 8:
                        has_e = True
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            positions.append((nx, ny))
                all_comps.append((min_r, max_r, min_c, max_c, has_e))
    left_comps = [c for c in all_comps if c[4]]
    right_comps = [c for c in all_comps if not c[4]]
    left_comps.sort(key=lambda x: x[0])
    right_comps.sort(key=lambda x: x[0])
    def get_blocks(comps: List[Tuple[int, int, int, int, bool]]) -> List[List[Tuple[int, int, int, int, bool]]]:
        if not comps:
            return []
        blocks = []
        current_block = [comps[0]]
        cur_max_r = comps[0][1]
        for comp in comps[1:]:
            if comp[0] <= cur_max_r:
                current_block.append(comp)
                cur_max_r = max(cur_max_r, comp[1])
            else:
                blocks.append(current_block)
                current_block = [comp]
                cur_max_r = comp[1]
        blocks.append(current_block)
        return blocks
    out_g = [[bg] * n for _ in range(n)]
    # left
    left_blocks = get_blocks(left_comps)
    for block in left_blocks:
        block.sort(key=lambda x: x[2])
        total_w = sum(x[3] - x[2] + 1 for x in block)
        curr_col = 0
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
                            out_g[r][dst_c] = nv
            curr_col += w
    # right
    right_blocks = get_blocks(right_comps)
    for block in right_blocks:
        block.sort(key=lambda x: x[2])
        total_w = sum(x[3] - x[2] + 1 for x in block)
        start_col = n - total_w
        curr_col = max(0, start_col)
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
                            out_g[r][dst_c] = nv
            curr_col += w
    return out_g
```