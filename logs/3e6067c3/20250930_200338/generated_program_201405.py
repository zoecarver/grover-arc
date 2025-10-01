```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    grid = [row[:] for row in g]
    if not grid:
        return grid
    n = len(grid)
    m = len(grid[0])
    bg = grid[-1][0]
    chain = [grid[n-2][j] for j in range(m) if grid[n-2][j] != bg]
    proto = None
    for row in grid[:-2]:
        non_bg_set = {c for c in row if c != bg}
        if len(non_bg_set) == 1:
            proto = next(iter(non_bg_set))
            break
    for i in range(n-2):
        non_bg_pos = [j for j in range(m) if grid[i][j] != bg]
        if not non_bg_pos:
            continue
        comps = []
        j = 0
        while j < len(non_bg_pos):
            start_j = non_bg_pos[j]
            end_j = start_j
            j += 1
            while j < len(non_bg_pos) and non_bg_pos[j] == end_j + 1:
                end_j += 1
                j += 1
            vals = {grid[i][k] for k in range(start_j, end_j + 1)}
            colors = [v for v in vals if v != bg and v != proto]
            comp_color = colors[0] if colors else proto
            comps.append((start_j, end_j, comp_color))
        for k in range(len(comps) - 1):
            if comps[k][2] == proto or comps[k + 1][2] == proto:
                continue
            c1 = comps[k][2]
            c2 = comps[k + 1][2]
            pos1 = [idx for idx in range(len(chain)) if chain[idx] == c1]
            pos2 = [idx for idx in range(len(chain)) if chain[idx] == c2]
            adjacent = any(abs(p1 - p2) == 1 for p1 in pos1 for p2 in pos2)
            if adjacent:
                all_pos = pos1 + pos2
                min_p = min(all_pos)
                fill_c = chain[min_p]
                end1 = comps[k][1]
                start2 = comps[k + 1][0]
                for jj in range(end1 + 1, start2):
                    grid[i][jj] = fill_c
    return grid
```