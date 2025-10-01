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
    pos_set = set(positions)
    for r, c in pos_set:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or g[nr][nc] == bg:
                return True
    return False

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
        if blob['num'] == bg or blob['num'] in (2, 8):
            continue
        if touches_bg(blob['positions'], g, bg, rows, cols):
            continue
        adj_nums = set()
        self_num = blob['num']
        for r, c in blob['positions']:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    nnum = g[nr][nc]
                    if nnum != bg and nnum != self_num:
                        adj_nums.add(nnum)
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
    objects = []
    for outer_i in range(len(atomic_blobs)):
        if atomic_blobs[outer_i]['num'] not in (2, 8):
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
    # place outer
    for r, c in obj['positions']:
        nr = r + shift_r
        nc = c + shift_c
        if 0 <= nr < len(out) and 0 <= nc < len(out[0]):
            out[nr][nc] = outer_num
    # place inners
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
    base_func = lambda o: 0 if outer_num == 8 else (12 if o['original_min_c'] < 9 else 17)
    group.sort(key=lambda o: (o['min_r'], o['min_c']))
    current_max_r = -100
    current_right = -1
    current_stack_min_col = 22
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
            if place_col + width - 1 > 21:
                new_stack = True
                is_touch = False
                is_overlap = False
                place_col = base_func(obj)
        shift_c = place_col - obj_min_c
        shift_r = 0
        if is_touch and not new_stack:
            # check all_top_outer
            all_top_outer = all(g[obj_min_r][c] == outer_num for c in range(obj_min_c, obj_max_c + 1))
            # check all_prev_bottom
            all_prev_bottom = all(out[current_max_r][c] == outer_num for c in range(current_stack_min_col, current_right + 1))
            if all_top_outer and all_prev_bottom:
                shift_r = -1
        # place
        place_obj(out, atomic, obj, shift_r, shift_c)
        # fill if applicable
        if shift_r == 0 and is_touch and not new_stack:
            fill_left = current_right + 1
            fill_right = place_col + width - 1
            for cc in range(fill_left, fill_right + 1):
                out[current_max_r][cc] = outer_num
        # update
        placed_min_r = obj_min_r + shift_r
        placed_max_r = obj_max_r + shift_r
        placed_min_c = obj_min_c + shift_c
        placed_max_c = obj_max_c + shift_c
        current_max_r = max(current_max_r, placed_max_r)
        current_right = max(current_right, placed_max_c)
        if new_stack:
            current_stack_min_col = placed_min_c
        else:
            current_stack_min_col = min(current_stack_min_col, placed_min_c)

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_bg(g)
    atomic = extract_atomic_blobs(g, bg)
    inners_dict = find_inners(g, bg, atomic)
    all_objects = build_objects(atomic, inners_dict)
    eight_objects = [o for o in all_objects if o['outer_num'] == 8]
    two_objects = [o for o in all_objects if o['outer_num'] == 2]
    out = [[bg] * 22 for _ in range(22)]
    place_group(out, atomic, eight_objects, 8)
    place_group(out, atomic, two_objects, 2)
    return out
```