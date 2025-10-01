```python
from typing import List, Tuple, Set, Dict
from collections import defaultdict

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

def is_touching_bg(positions: List[Tuple[int, int]], g: List[List[int]], bg: int, directions: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    for r, c in positions:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or g[nr][nc] == bg:
                return True
    return False

def get_adj_nums(positions: List[Tuple[int, int]], g: List[List[int]], bg: int, directions: List[Tuple[int, int]], rows: int, cols: int) -> Set[int]:
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

def blobs_adjacent(pos1: List[Tuple[int, int]], pos2: List[Tuple[int, int]], directions: List[Tuple[int, int]], rows: int, cols: int) -> bool:
    pos_set = set(pos2)
    for r, c in pos1:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in pos_set:
                return True
    return False

def get_discovery(pos: List[Tuple[int, int]]) -> Tuple[int, int]:
    if not pos:
        return (999, 999)
    min_r = min(r for r, c in pos)
    min_c = min(c for r, c in pos if r == min_r)
    return (min_r, min_c)

def build_objects(atomic_blobs: List[Dict], g: List[List[int]], bg: int, rows: int, cols: int) -> List[Dict]:
    outer_inners = defaultdict(list)
    standalone = []
    for i, blob in enumerate(atomic_blobs):
        positions = blob['positions']
        if is_touching_bg(positions, g, bg, directions, rows, cols):
            standalone.append(i)
        else:
            adj = get_adj_nums(positions, g, bg, directions, rows, cols)
            if len(adj) == 1:
                outer_num = next(iter(adj))
                found = False
                for j, ob in enumerate(atomic_blobs):
                    if ob['num'] == outer_num and j != i and blobs_adjacent(positions, ob['positions'], directions, rows, cols):
                        outer_inners[j].append(i)
                        found = True
                        break
                if not found:
                    standalone.append(i)
            else:
                standalone.append(i)
    objects = []
    used = set()
    for outer_i in list(outer_inners):
        obj = {'outer_pos': atomic_blobs[outer_i]['positions'], 'inners': [atomic_blobs[inner_i]['positions'] for inner_i in outer_inners[outer_i]]}
        objects.append(obj)
        used.update([outer_i] + outer_inners[outer_i])
    for i in standalone:
        if i not in used:
            obj = {'outer_pos': atomic_blobs[i]['positions'], 'inners': []}
            objects.append(obj)
    return objects

def get_relative_positions(obj: Dict, g: List[List[int]]) -> List[Tuple[int, int, int]]:
    outer_pos = obj['outer_pos']
    if not outer_pos:
        return []
    min_r = min(r for r, c in outer_pos)
    min_c = min(c for r, c in outer_pos if r == min_r)
    rel = [(r - min_r, c - min_c, g[r][c]) for r, c in outer_pos]
    for inner_pos in obj['inners']:
        for r, c in inner_pos:
            rel.append((r - min_r, c - min_c, g[r][c]))
    return rel

def can_place_at(out: List[List[int]], rel_pos: List[Tuple[int, int, int]], start_r: int, start_c: int, rows: int, cols: int, bg: int) -> bool:
    for dr, dc, num in rel_pos:
        tr = start_r + dr
        tc = start_c + dc
        if not (0 <= tr < rows and 0 <= tc < cols):
            return False
        if out[tr][tc] != bg and out[tr][tc] != num:
            return False
    return True

def place_object(out: List[List[int]], rel_pos: List[Tuple[int, int, int]], start_r: int, start_c: int):
    for dr, dc, num in rel_pos:
        tr = start_r + dr
        tc = start_c + dc
        out[tr][tc] = num

def compute_max_extent(rel_pos: List[Tuple[int, int, int]]) -> Tuple[int, int]:
    if not rel_pos:
        return 0, 0
    max_dr = max(dr for dr, _, _ in rel_pos)
    max_dc = max(dc for _, dc, _ in rel_pos)
    return max_dr + 1, max_dc + 1

def program(g: List[List[int]]) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    bg = g[0][0]
    atomic_blobs = extract_atomic_blobs(g, bg, rows, cols)
    objects = build_objects(atomic_blobs, g, bg, rows, cols)
    for obj in objects:
        obj['rel_pos'] = get_relative_positions(obj, g)
    objects.sort(key=lambda o: get_discovery(o['outer_pos']))
    out = [[bg] * cols for _ in range(rows)]
    current_r = 0
    for obj in objects:
        rel_pos = obj['rel_pos']
        if not rel_pos:
            continue
        height, width = compute_max_extent(rel_pos)
        placed = False
        for sr in range(current_r, rows - height + 1):
            placed_inner = False
            for sc in range(cols - width + 1):
                if can_place_at(out, rel_pos, sr, sc, rows, cols, bg):
                    place_object(out, rel_pos, sr, sc)
                    current_r = max(current_r, sr + height)
                    placed = True
                    placed_inner = True
                    break
            if placed_inner:
                break
        if not placed:
            # Fallback: place at bottom left if cannot fit
            sr = max(0, rows - height)
            sc = 0
            if can_place_at(out, rel_pos, sr, sc, rows, cols, bg):
                place_object(out, rel_pos, sr, sc)
    return out
```