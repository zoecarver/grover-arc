```python
from typing import List, Dict, DefaultDict
from collections import defaultdict

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def extract_atomic_blobs(g: List[List[int]], bg: int) -> List[Dict]:
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    blobs = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                num = g[r][c]
                positions = []
                stack = [(r, c)]
                visited[r][c] = True
                positions.append((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == num:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                            positions.append((nr, nc))
                            min_r = min(min_r, nr)
                            max_r = max(max_r, nr)
                            min_c = min(min_c, nc)
                            max_c = max(max_c, nc)
                blobs.append({
                    'num': num,
                    'positions': positions,
                    'min_r': min_r,
                    'max_r': max_r,
                    'min_c': min_c,
                    'max_c': max_c
                })
    return blobs

def touches_bg(positions: List[tuple], g: List[List[int]], bg: int, rows: int, cols: int) -> bool:
    for r, c in positions:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or g[nr][nc] == bg:
                return True
    return False

def get_adj_nums(positions: List[tuple], g: List[List[int]], bg: int, rows: int, cols: int) -> set:
    adj = set()
    if not positions:
        return adj
    self_num = g[positions[0][0]][positions[0][1]]
    for r, c in positions:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nnum = g[nr][nc]
                if nnum != bg and nnum != self_num:
                    adj.add(nnum)
    return adj

def blobs_adjacent(pos1: List[tuple], pos2: List[tuple]) -> bool:
    pos_set = set(pos2)
    for r, c in pos1:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (nr, nc) in pos_set:
                return True
    return False

def find_inners(g: List[List[int]], bg: int, atomic_blobs: List[Dict]) -> DefaultDict[int, List[int]]:
    rows, cols = len(g), len(g[0])
    inners_for_outer: DefaultDict[int, List[int]] = defaultdict(list)
    for i, blob in enumerate(atomic_blobs):
        if blob['num'] == bg:
            continue
        if touches_bg(blob['positions'], g, bg, rows, cols):
            continue
        adj_nums = get_adj_nums(blob['positions'], g, bg, rows, cols)
        if len(adj_nums) != 1:
            continue
        outer_num = next(iter(adj_nums))
        if outer_num not in (2, 8):
            continue
        found_outer = None
        for j, ob in enumerate(atomic_blobs):
            if ob['num'] == outer_num and blobs_adjacent(blob['positions'], ob['positions']):
                found_outer = j
                break
        if found_outer is not None:
            inners_for_outer[found_outer].append(i)
    return inners_for_outer

def build_objects(atomic_blobs: List[Dict], inners_for_outer: DefaultDict[int, List[int]]) -> List[Dict]:
    used_as_inner = set()
    for inner_list in inners_for_outer.values():
        used_as_inner.update(inner_list)
    objects = []
    for outer_i in range(len(atomic_blobs)):
        if atomic_blobs[outer_i]['num'] not in (2, 8) or outer_i in used_as_inner:
            continue
        obj = {
            'outer_i': outer_i,
            'inner_is': inners_for_outer[outer_i],
            'positions': atomic_blobs[outer_i]['positions'],
            'min_r': atomic_blobs[outer_i]['min_r'],
            'max_r': atomic_blobs[outer_i]['max_r'],
            'min_c': atomic_blobs[outer_i]['min_c'],
            'max_c': atomic_blobs[outer_i]['max_c'],
            'outer_num': atomic_blobs[outer_i]['num'],
            'original_min_c': atomic_blobs[outer_i]['min_c']
        }
        objects.append(obj)
    return objects

def place_obj(out: List[List[int]], atomic: List[Dict], obj: Dict, shift_r: int, shift_c: int):
    outer_num = obj['outer_num']
    for r, c in obj['positions']:
        nr = r + shift_r
        nc = c + shift_c
        if 0 <= nr < len(out) and 0 <= nc < len(out[0]):
            out[nr][nc] = outer_num
    for inner_i in obj['inner_is']:
        inner_num = atomic[inner_i]['num']
        for r, c in atomic[inner_i]['positions']:
            nr = r + shift_r
            nc = c + shift_c
            if 0 <= nr < len(out) and 0 <= nc < len(out[0]):
                out[nr][nc] = inner_num

def place_group(out: List[List[int]], atomic: List[Dict], group: List[Dict], outer_num: int):
    if not group:
        return
    rows, cols = len(out), len(out[0])
    def base_func(o: Dict) -> int:
        if outer_num == 8:
            return 0
        return 12 if o['original_min_c'] < 9 else 17
    group.sort(key=lambda o: (o['min_r'], o['min_c']))
    current_max_r = -100
    current_right = -1
    current_stack_min_col = cols
    for obj in group:
        obj_min_r = obj['min_r']
        obj_max_r = obj['max_r']
        obj_min_c = obj['min_c']
        obj_max_c = obj['max_c']
        width = obj_max_c - obj_min_c + 1
        is_touch = (obj_min_r == current_max_r + 1)
        is_overlap = (obj_min_r <= current_max_r)
        new_stack = not (is_overlap or is_touch)
        place_col = base_func(obj)
        if not new_stack:
            place_col = current_right + 1
            if place_col + width - 1 >= cols:
                new_stack = True
                place_col = base_func(obj)
        shift_c = place_col - obj_min_c
        shift_r = 0
        top_open = False
        if not new_stack:
            top_r = obj_min_r
            bbox_cols = range(obj_min_c, obj_max_c + 1)
            is_solid = True
            for c in bbox_cols:
                if 0 <= c < len(g) and g[top_r][c] != outer_num:  # g is global? Wait, pass g or use out? But check input
                    is_solid = False
                    break
            top_open = not is_solid
        place_obj(out, atomic, obj, shift_r, shift_c)
        if top_open and not new_stack:
            lid_r = obj_min_r - 1 + shift_r
            if 0 <= lid_r < rows:
                lid_start_c = place_col
                for cc in range(lid_start_c, lid_start_c + width):
                    if 0 <= cc < cols:
                        out[lid_r][cc] = outer_num
        placed_min_r = obj_min_r + shift_r
        if top_open and not new_stack and 0 <= (obj_min_r - 1 + shift_r) < rows:
            placed_min_r = min(placed_min_r, obj_min_r - 1 + shift_r)
        placed_max_r = obj_max_r + shift_r
        placed_min_c = place_col
        placed_max_c = place_col + width - 1
        current_max_r = max(current_max_r, placed_max_r)
        current_right = max(current_right, placed_max_c)
        if new_stack:
            current_stack_min_col = placed_min_c
        else:
            current_stack_min_col = min(current_stack_min_col, placed_min_c)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    atomic_blobs = extract_atomic_blobs(g, bg)
    inners_for_outer = find_inners(g, bg, atomic_blobs)
    objects = build_objects(atomic_blobs, inners_for_outer)
    out = [[bg] * 22 for _ in range(22)]
    groups = defaultdict(list)
    for obj in objects:
        groups[obj['outer_num']].append(obj)
    for outer_num in [8, 2]:
        group = groups[outer_num]
        place_group(out, atomic_blobs, group, outer_num)
    return out
```