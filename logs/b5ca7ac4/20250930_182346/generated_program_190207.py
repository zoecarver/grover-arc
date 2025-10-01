```python
from typing import List, Tuple, Set, Dict
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    bg = g[0][0]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def extract_atomic_blobs(g: List[List[int]], bg: int, rows: int, cols: int) -> List[Dict]:
        visited = [[False] * cols for _ in range(rows)]
        atomic_blobs = []
        for r in range(rows):
            for c in range(cols):
                if g[r][c] != bg and not visited[r][c]:
                    num = g[r][c]
                    positions = []
                    stack = [(r, c)]
                    visited[r][c] = True
                    positions.append((r, c))
                    while stack:
                        cr, cc = stack.pop()
                        for dr, dc in directions:
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == num:
                                visited[nr][nc] = True
                                stack.append((nr, nc))
                                positions.append((nr, nc))
                    atomic_blobs.append({'num': num, 'positions': positions})
        return atomic_blobs

    def get_adj_nums(positions: List[Tuple[int, int]], g: List[List[int]], bg: int, directions, rows: int, cols: int) -> Set[int]:
        adj = set()
        self_num = g[positions[0][0]][positions[0][1]]
        for r, c in positions:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    nnum = g[nr][nc]
                    if nnum != bg and nnum != self_num:
                        adj.add(nnum)
        return adj

    def blobs_adjacent(pos1: List[Tuple[int, int]], pos2: List[Tuple[int, int]], directions, rows: int, cols: int) -> bool:
        pos_set = set(pos2)
        for r, c in pos1:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in pos_set:
                    return True
        return False

    def get_discovery(pos: List[Tuple[int, int]]) -> Tuple[int, int]:
        if not pos:
            return (rows, cols)
        min_r = min(r for r, c in pos)
        min_c = min(c for r, c in pos if r == min_r)
        return (min_r, min_c)

    def is_touching_bg(positions: List[Tuple[int, int]], g: List[List[int]], bg: int, directions, rows: int, cols: int) -> bool:
        for r, c in positions:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < rows and 0 <= nc < cols) or g[nr][nc] == bg:
                    return True
        return False

    atomic_blobs = extract_atomic_blobs(g, bg, rows, cols)
    n = len(atomic_blobs)

    merged = set()
    objects = []
    for i in range(n):
        if i in merged:
            continue
        blob = atomic_blobs[i]
        self_num = blob['num']
        adj_nums = get_adj_nums(blob['positions'], g, bg, directions, rows, cols)
        all_cells = [(r, c, self_num) for r, c in blob['positions']]
        if len(adj_nums) == 1:
            outer_num = next(iter(adj_nums))
            for j in range(n):
                if j != i and j not in merged and atomic_blobs[j]['num'] == outer_num and blobs_adjacent(blob['positions'], atomic_blobs[j]['positions'], directions, rows, cols) and not is_touching_bg(atomic_blobs[j]['positions'], g, bg, directions, rows, cols):
                    inner_blob = atomic_blobs[j]
                    inner_num = inner_blob['num']
                    inner_pos = inner_blob['positions']
                    merged.add(j)
                    inner_cells = [(r, c, inner_num) for r, c in inner_pos]
                    if bg == 0:
                        inner_min_r = min(r for r, c in inner_pos)
                        top_cs = set(c for r, c in inner_pos if r == inner_min_r)
                        for c in top_cs:
                            nr = inner_min_r - 1
                            if 0 <= nr < rows and g[nr][c] == bg:
                                inner_cells.append((nr, c, self_num))
                    all_cells += inner_cells
        disc = get_discovery(blob['positions'])
        objects.append({'cells': all_cells, 'discovery': disc, 'outer_num': self_num, 'original_min_c': min(c for r, c in blob['positions']) if blob['positions'] else 0})

    objects.sort(key=lambda o: o['discovery'])

    out = [[bg for _ in range(cols)] for _ in range(rows)]

    current_r = 0
    for o in objects:
        cells = o['cells']
        if not cells:
            continue
        min_r_obj = min(r for r, _, _ in cells)
        min_c_obj = min(c for _, c, _ in cells)
        height = max(r for r, _, _ in cells) - min_r_obj + 1
        width = max(c for _, c, _ in cells) - min_c_obj + 1
        placed = False
        for try_r in range(current_r, rows - height + 1):
            for try_c in range(0, cols - width + 1):
                can_place = True
                for r, c, num in cells:
                    nr = try_r + (r - min_r_obj)
                    nc = try_c + (c - min_c_obj)
                    if nr >= rows or nc >= cols or (out[nr][nc] != bg and out[nr][nc] != num):
                        can_place = False
                        break
                if can_place:
                    for r, c, num in cells:
                        nr = try_r + (r - min_r_obj)
                        nc = try_c + (c - min_c_obj)
                        out[nr][nc] = num
                    current_r = max(current_r, max(nr for r, _, _ in cells with nr = try_r + (r - min_r_obj)) + 1)
                    placed = True
                    break
            if placed:
                break

    return out
```