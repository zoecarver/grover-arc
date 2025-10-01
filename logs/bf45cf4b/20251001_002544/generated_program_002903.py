```python
from collections import Counter, deque
from typing import List, Tuple

def find_bg(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[List[Tuple[int, int]]]:
    rows = len(g)
    if rows == 0:
        return []
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                comp = []
                q = deque([(r, c)])
                visited[r][c] = True
                while q:
                    cr, cc = q.popleft()
                    comp.append((cr, cc))
                    for dr, dc in dirs:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] != bg:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                components.append(comp)
    return components

def identify_decoy_and_tile(g: List[List[int]], components: List[List[Tuple[int, int]]], bg: int) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    decoy_comp = None
    tile_comp = None
    for comp in components:
        colors = {g[r][c] for r, c in comp}
        if len(colors) == 1:
            if decoy_comp is None:
                decoy_comp = comp
        elif len(colors) > 1:
            if tile_comp is None:
                tile_comp = comp
    return decoy_comp, tile_comp

def get_decoy_info(g: List[List[int]], decoy_comp: List[Tuple[int, int]], bg: int) -> Tuple[int, int, int, int, List[List[bool]]]:
    if not decoy_comp:
        raise ValueError("No decoy component")
    min_r = min(r for r, c in decoy_comp)
    max_r = max(r for r, c in decoy_comp)
    min_c = min(c for r, c in decoy_comp)
    max_c = max(c for r, c in decoy_comp)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    decoy_color = g[decoy_comp[0][0]][decoy_comp[0][1]]
    mask = [[g[min_r + i][min_c + j] == decoy_color for j in range(w)] for i in range(h)]
    return min_r, min_c, h, w, mask

def get_tile_info(g: List[List[int]], tile_comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int, List[List[int]]]:
    if not tile_comp:
        raise ValueError("No tile component")
    min_r = min(r for r, c in tile_comp)
    max_r = max(r for r, c in tile_comp)
    min_c = min(c for r, c in tile_comp)
    max_c = max(c for r, c in tile_comp)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    tile_sub = [[g[min_r + i][min_c + j] for j in range(w)] for i in range(h)]
    return min_r, min_c, h, w, tile_sub

def paste_tile(grid: List[List[int]], tile: List[List[int]], row_start: int, col_start: int) -> None:
    h_tile = len(tile)
    if h_tile == 0:
        return
    w_tile = len(tile[0])
    for i in range(h_tile):
        for j in range(w_tile):
            grid[row_start + i][col_start + j] = tile[i][j]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    bg = find_bg(g)
    components = find_components(g, bg)
    decoy_comp, tile_comp = identify_decoy_and_tile(g, components, bg)
    if decoy_comp is None or tile_comp is None:
        return [[bg]]  # fallback
    _, _, h_dec, w_dec, mask = get_decoy_info(g, decoy_comp, bg)
    _, _, h_tile, w_tile, tile_sub = get_tile_info(g, tile_comp)
    out_h = h_dec * h_tile
    out_w = w_dec * w_tile
    out = [[bg for _ in range(out_w)] for _ in range(out_h)]
    for i in range(h_dec):
        for j in range(w_dec):
            if mask[i][j]:
                paste_tile(out, tile_sub, i * h_tile, j * w_tile)
    return out
```