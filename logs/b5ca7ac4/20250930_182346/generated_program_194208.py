```python
from typing import List, Tuple, Dict
from collections import defaultdict

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def extract_atomic_blobs(g: List[List[int]], bg: int) -> List[Dict]:
    rows = len(g)
    cols = len(g[0])
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
                min_r = max_r = r
                min_c = max_c = c
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

def blobs_adjacent(pos1: List[Tuple[int, int]], pos2: List[Tuple[int, int]]) -> bool:
    pos_set = set(pos2)
    for r, c in pos1:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (nr, nc) in pos_set:
                return True
    return False

def build_objects(g: List[List[int]], atomic_blobs: List[Dict], bg: int) -> List[Dict]:
    rows = len(g)
    used = set()
    objects = []
    for i in range(len(atomic_blobs)):
        if i in used:
            continue
        blob = atomic_blobs[i]
        self_num = blob['num']
        if self_num == bg:
            continue
        positions = blob['positions']
        adj_count = defaultdict(int)
        for r, c in positions:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < len(g[0]):
                    nnum = g[nr][nc]
                    if nnum != bg and nnum != self_num:
                        adj_count[nnum] += 1
        candidates = {k: adj_count[k] for k in (2, 8) if k != self_num and adj_count[k] > 0}
        if not candidates:
            continue
        outer_num = max(candidates, key=candidates.get)
        touching_outer_is = [
            j for j in range(len(atomic_blobs))
            if j not in used and atomic_blobs[j]['num'] == outer_num
            and blobs_adjacent(positions, atomic_blobs[j]['positions'])
        ]
        if touching_outer_is:
            outer_pos = []
            for j in touching_outer_is:
                outer_pos += atomic_blobs[j]['positions']
                used.add(j)
            used.add(i)
            all_pos = outer_pos + positions
            min_r = min(r for r, _ in all_pos)
            max_r = max(r for r, _ in all_pos)
            min_c = min(c for _, c in all_pos)
            max_c = max(c for _, c in all_pos)
            inner_min_r = min(r for r, _ in positions)
            top_cols = {c for r, c in positions if r == inner_min_r}
            is_open_top = bg == 0 and top_cols and all(g[inner_min_r - 1][c] == bg for c in top_cols)
            obj = {
                'outer_pos': outer_pos,
                'inner_pos': positions,
                'outer_num': outer_num,
                'inner_num': self_num,
                'min_r': min_r,
                'max_r': max_r,
                'min_c': min_c,
                'max_c': max_c,
                'original_min_c': min_c,
                'is_open_top': is_open_top,
                'inner_min_r': inner_min_r if positions else None
            }
            objects.append(obj)
    for j in range(len(atomic_blobs)):
        if j not in used and atomic_blobs[j]['num'] in (2, 8):
            blob = atomic_blobs[j]
            obj = {
                'outer_pos': blob['positions'],
                'inner_pos': [],
                'outer_num': blob['num'],
                'inner_num': 0,
                'min_r': blob['min_r'],
                'max_r': blob['max_r'],
                'min_c': blob['min_c'],
                'max_c': blob['max_c'],
                'original_min_c': blob['min_c'],
                'is_open_top': False,
                'inner_min_r': None
            }
            objects.append(obj)
    return sorted(objects, key=lambda o: (o['min_r'], o['min_c']))

def is_solid_top(obj: Dict, g: List[List[int]], outer_num: int) -> bool:
    min_r = obj['min_r']
    min_c = obj['min_c']
    max_c = obj['max_c']
    if obj['inner_pos'] and obj['is_open_top'] and min_r == obj['inner_min_r']:
        return True
    for c in range(min_c, max_c + 1):
        if g[min_r][c] != outer_num:
            return False
    return True

def place_obj(out: List[List[int]], g: List[List[int]], obj: Dict, shift_r: int, shift_c: int):
    for r, c in obj['outer_pos']:
        nr = r + shift_r
        nc = c + shift_c
        if 0 <= nr < len(out) and 0 <= nc < len(out[0]):
            out[nr][nc] = obj['outer_num']
    if obj['inner_pos']:
        inner_min_r = obj['inner_min_r']
        for r, c in obj['inner_pos']:
            nr = r + shift_r
            nc = c + shift_c
            if 0 <= nr < len(out) and 0 <= nc < len(out[0]):
                place_num = obj['outer_num'] if obj['is_open_top'] and r == inner_min_r else obj['inner_num']
                out[nr][nc] = place_num

def place_group(out: List[List[int]], g: List[List[int]], group: List[Dict], outer_num: int):
    if not group:
        return
    def base_col(o: Dict) -> int:
        return 0 if outer_num == 8 else (12 if o['original_min_c'] < 9 else 17)
    group.sort(key=lambda o: (o['min_r'], o['min_c']))
    current_max_r = -100
    current_right = -1
    current_stack_min_col = 22
    rows = len(out)
    cols = len(out[0])
    for obj in group:
        obj_min_r = obj['min_r']
        obj_max_r = obj['max_r']
        obj_min_c = obj['min_c']
        obj_max_c = obj['max_c']
        width = obj_max_c - obj_min_c + 1
        is_touch = (obj_min_r == current_max_r + 1)
        is_overlap = (obj_min_r <= current_max_r)
        new_stack = not (is_overlap or is_touch)
        place_col = base_col(obj)
        if not new_stack:
            place_col = current_right + 1
            if place_col + width - 1 > cols - 1:
                new_stack = True
                place_col = base_col(obj)
        shift_c = place_col - obj_min_c
        shift_r = 0
        all_prev_bottom = False
        if current_max_r >= 0:
            all_prev_bottom = all(out[current_max_r][cc] == outer_num for cc in range(max(0, current_stack_min_col), min(cols, current_right + 1)))
        all_top_outer = is_solid_top(obj, g, outer_num)
        if (is_touch or is_overlap) and not new_stack and all_top_outer and all_prev_bottom:
            shift_r = -1
        place_obj(out, g, obj, shift_r, shift_c)
        if shift_r == 0 and is_touch and not new_stack:
            fill_left = current_right + 1
            fill_right = place_col + width - 1
            for cc in range(max(0, fill_left), min(cols, fill_right + 1)):
                out[current_max_r][cc] = outer_num
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
    atomic_blobs = extract_atomic_blobs(g, bg)
    objects = build_objects(g, atomic_blobs, bg)
    out = [[bg for _ in range(len(g[0]))] for _ in range(len(g))]
    groups = defaultdict(list)
    for obj in objects:
        groups[obj['outer_num']].append(obj)
    for outer_num in [8, 2]:
        place_group(out, g, groups[outer_num], outer_num)
    return out
```