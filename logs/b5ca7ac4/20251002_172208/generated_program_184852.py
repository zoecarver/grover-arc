```python
from collections import Counter
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int, bool]]:
    n = len(g)
    visited = [[False] * n for _ in range(n)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(n):
        for j in range(n):
            if g[i][j] != bg and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if comp:
                    rs = [r for r, _ in comp]
                    cs = [c for _, c in comp]
                    minr, maxr = min(rs), max(rs)
                    minc, maxc = min(cs), max(cs)
                    has8 = any(g[r][c] == 8 for r, c in comp)
                    components.append((minr, maxr, minc, maxc, has8))
    return components

def group_blocks(shapes: List[Tuple[int, int, int, int, bool]]) -> List[List[Tuple[int, int, int, int, bool]]]:
    blocks = []
    if not shapes:
        return blocks
    current_block = [shapes[0]]
    current_maxr = shapes[0][1]
    for s in shapes[1:]:
        minr = s[0]
        if minr > current_maxr + 1:
            blocks.append(current_block)
            current_block = [s]
            current_maxr = s[1]
        else:
            current_block.append(s)
            current_maxr = max(current_maxr, s[1])
    blocks.append(current_block)
    return blocks

def place_block(out: List[List[int]], g: List[List[int]], bg: int, block: List[Tuple[int, int, int, int, bool]], is_left: bool):
    if not block:
        return
    block = sorted(block, key=lambda x: x[2])
    ws = [x[3] - x[2] + 1 for x in block]
    total_w = sum(ws)
    if is_left:
        block_start = 0
    else:
        block_start = 22 - total_w
    current = block_start
    for idx, s in enumerate(block):
        minr, maxr, minc, maxc = s[0], s[1], s[2], s[3]
        w = ws[idx]
        for r in range(minr, maxr + 1):
            for k in range(w):
                c = minc + k
                oc = current + k
                if 0 <= oc < 22 and g[r][c] != bg:
                    out[r][oc] = g[r][c]
        current += w

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    components = find_components(g, bg)
    left = [ (minr, maxr, minc, maxc) for minr, maxr, minc, maxc, has8 in components if has8 ]
    right = [ (minr, maxr, minc, maxc) for minr, maxr, minc, maxc, has8 in components if not has8 ]
    left = sorted(left, key=lambda x: x[0])
    right = sorted(right, key=lambda x: x[0])
    left_blocks = group_blocks(left)
    right_blocks = group_blocks(right)
    out = [[bg for _ in range(22)] for _ in range(22)]
    for block in left_blocks:
        place_block(out, g, bg, block, True)
    for block in right_blocks:
        place_block(out, g, bg, block, False)
    return out
```