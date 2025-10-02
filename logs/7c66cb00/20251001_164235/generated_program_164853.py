```python
from typing import List, Tuple

def find_components(g: List[List[int]], color: int, noise_rows: List[int]) -> List[List[Tuple[int, int]]]:
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in noise_rows:
        for c in range(w):
            if g[r][c] == color and not visited[r][c]:
                component = []
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    component.append((cr, cc))
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < h and 0 <= nc < w and g[nr][nc] == color and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                if len(component) > 1:
                    components.append(component)
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    h, w = len(g), len(g[0])
    background = g[0][0]
    blocks = []
    r = 0
    while r < h:
        if (g[r][0] == g[r][w-1] and
            g[r][0] != g[r][1] and
            all(g[r][j] == g[r][1] for j in range(1, w-1))):
            b = g[r][0]
            i_color = g[r][1]
            start_r = r
            while (r < h and
                   g[r][0] == b and g[r][w-1] == b and
                   g[r][1] == i_color and
                   all(g[r][j] == i_color for j in range(1, w-1))):
                r += 1
            end_r = r - 1
            blocks.append((start_r, end_r, b, i_color))
        else:
            r += 1
    block_rows = set()
    for start, end, _, _ in blocks:
        for rr in range(start, end + 1):
            block_rows.add(rr)
    noise_rows = [rr for rr in range(h) if rr not in block_rows]
    out = [[background] * w for _ in range(h)]
    color_to_comps = {}
    for i_color in set(b[3] for b in blocks):
        color_to_comps[i_color] = find_components(g, i_color, noise_rows)
    for start_r, end_r, b, i_color in blocks:
        inner = [i_color] * (w - 2)
        uniform_row = [b] + inner + [b]
        for rr in range(start_r, end_r + 1):
            out[rr] = uniform_row[:]
        for comp in color_to_comps.get(i_color, []):
            if not comp:
                continue
            bottom_small = max(sr for sr, sc in comp)
            for sr, sc in comp:
                rel_from_bottom = bottom_small - sr
                large_r = end_r - rel_from_bottom
                if start_r <= large_r <= end_r:
                    out[large_r][sc] = b
    return out
```