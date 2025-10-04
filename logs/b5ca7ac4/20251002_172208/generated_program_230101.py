```python
from collections import Counter
from typing import List, Dict, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def flood_fill(g: List[List[int]], start_r: int, start_c: int, visited: List[List[bool]], bg: int, n: int) -> List[Tuple[int, int]]:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    cells = []
    stack = [(start_r, start_c)]
    visited[start_r][start_c] = True
    while stack:
        x, y = stack.pop()
        cells.append((x, y))
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] != bg:
                visited[nx][ny] = True
                stack.append((nx, ny))
    return cells

def extract_components(g: List[List[int]], bg: int, n: int, seed_color: int, visited: List[List[bool]]) -> List[Dict[str, int]]:
    comps = []
    for i in range(n):
        for j in range(n):
            if g[i][j] == seed_color and not visited[i][j]:
                cells = flood_fill(g, i, j, visited, bg, n)
                if cells:
                    rs = [r for r, _ in cells]
                    cs = [c for _, c in cells]
                    comps.append({
                        'cells': cells,
                        'minr': min(rs),
                        'maxr': max(rs),
                        'minc': min(cs),
                        'maxc': max(cs)
                    })
    return comps

def group_into_blocks(comps: List[Dict[str, int]], threshold: int) -> List[List[Dict[str, int]]]:
    if not comps:
        return []
    comps = sorted(comps, key=lambda c: c['minr'])
    blocks = []
    current_block = [comps[0]]
    cur_max_r = comps[0]['maxr']
    for comp in comps[1:]:
        if comp['minr'] <= cur_max_r + threshold:
            current_block.append(comp)
            cur_max_r = max(cur_max_r, comp['maxr'])
        else:
            blocks.append(current_block)
            current_block = [comp]
            cur_max_r = comp['maxr']
    blocks.append(current_block)
    return blocks

def place_block(out: List[List[int]], g: List[List[int]], block: List[Dict[str, int]], start_col: int, n: int):
    if not block:
        return
    block = sorted(block, key=lambda c: c['minc'])
    curr_col = start_col
    for comp in block:
        delta = curr_col - comp['minc']
        for r, c in comp['cells']:
            new_c = c + delta
            if 0 <= new_c < n:
                out[r][new_c] = g[r][c]
        w = comp['maxc'] - comp['minc'] + 1
        curr_col += w

def get_right_start(block: List[Dict[str, int]]) -> int:
    if not block:
        return 17
    min_min_c = min(c['minc'] for c in block)
    return 12 if min_min_c < 9 else 17

def program(g: List[List[int]]) -> List[List[int]]:
    n = 22
    bg = get_background(g)
    visited = [[False] * n for _ in range(n)]
    left_comps = extract_components(g, bg, n, 8, visited)
    right_comps = extract_components(g, bg, n, 2, visited)
    left_blocks = group_into_blocks(left_comps, 1)
    right_blocks = group_into_blocks(right_comps, -1)
    out = [[bg] * n for _ in range(n)]
    for block in left_blocks:
        place_block(out, g, block, 0, n)
    for block in right_blocks:
        b_start = get_right_start(block)
        place_block(out, g, block, b_start, n)
    return out
```