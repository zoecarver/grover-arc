```python
from typing import List, Dict, Tuple
from collections import Counter

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = Counter(cell for row in g for cell in row).most_common(1)[0][0]
    visited = [[False] * n for _ in range(n)]
    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    components: List[Dict[str, any]] = []
    for i in range(n):
        for j in range(n):
            if g[i][j] != bg and not visited[i][j]:
                comp_cells: List[Tuple[int, int]] = []
                stack: List[Tuple[int, int]] = [(i, j)]
                visited[i][j] = True
                minr, maxr = i, i
                minc, maxc = j, j
                has8 = False
                while stack:
                    x, y = stack.pop()
                    comp_cells.append((x, y))
                    if g[x][y] == 8:
                        has8 = True
                    minr = min(minr, x)
                    maxr = max(maxr, x)
                    minc = min(minc, y)
                    maxc = max(maxc, y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] != bg and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if comp_cells:
                    components.append({
                        'cells': comp_cells,
                        'minr': minr,
                        'maxr': maxr,
                        'minc': minc,
                        'maxc': maxc,
                        'has8': has8
                    })
    components.sort(key=lambda c: (c['minr'], c['minc']))
    blocks: List[List[Dict[str, any]]] = []
    if components:
        current_block = [components[0]]
        cur_maxr = components[0]['maxr']
        for comp in components[1:]:
            if comp['minr'] <= cur_maxr:
                current_block.append(comp)
                cur_maxr = max(cur_maxr, comp['maxr'])
            else:
                blocks.append(current_block)
                current_block = [comp]
                cur_maxr = comp['maxr']
        blocks.append(current_block)
    out = [[bg] * n for _ in range(n)]
    for block in blocks:
        left_comps = [c for c in block if c['has8']]
        right_comps = [c for c in block if not c['has8']]
        def pack_side(comps: List[Dict[str, any]], start_col: int, out_grid: List[List[int]], g_grid: List[List[int]]) -> None:
            if not comps:
                return
            sorted_comps = sorted(comps, key=lambda c: c['minc'])
            current_col = start_col
            for comp in sorted_comps:
                shift = current_col - comp['minc']
                for r, c in comp['cells']:
                    new_c = c + shift
                    if 0 <= new_c < n:
                        out_grid[r][new_c] = g_grid[r][c]
                width = comp['maxc'] - comp['minc'] + 1
                current_col += width
        # Pack left
        pack_side(left_comps, 0, out, g)
        # Pack right
        if right_comps:
            block_min_minc = min(c['minc'] for c in right_comps)
            total_w = sum(c['maxc'] - c['minc'] + 1 for c in right_comps)
            start_col = 12 if block_min_minc < 9 else n - total_w
            pack_side(right_comps, start_col, out, g)
    return out
```