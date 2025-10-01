```python
from typing import List, Dict, DefaultDict, Tuple
from collections import defaultdict

directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_bg(g: List[List[int]]) -> int:
    """Extract background value from top-left cell."""
    return g[0][0]

def extract_atomic_blobs(g: List[List[int]], bg: int) -> List[Dict]:
    """Extract 4-connected components of non-background numbers as atomic blobs with positions and bounds."""
    rows, cols = len(g), len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    blobs: List[Dict] = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                num = g[r][c]
                positions: List[Tuple[int, int]] = []
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

def touches_bg(positions: List[Tuple[int, int]], g: List[List[int]], bg: int, rows: int, cols: int) -> bool:
    """Check if any cell in positions or its neighbor touches background or grid edge."""
    for r, c in positions:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or g[nr][nc] == bg:
                return True
    return False

def get_adj_nums(positions: List[Tuple[int, int]], g: List[List[int]], bg: int, rows: int, cols: int) -> set[int]:
    """Get set of adjacent non-background, non-self numbers touching the positions."""
    adj: set[int] = set()
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

def blobs_adjacent(pos1: List[Tuple[int, int]], pos2: List[Tuple[int, int]]) -> bool:
    """Check if any position in pos1 is 4-adjacent to any in pos2."""
    pos_set = set(pos2)
    for r, c in pos1:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (nr, nc) in pos_set:
                return True
    return False

def find_inners(g: List[List[int]], bg: int, atomic_blobs: List[Dict]) -> DefaultDict[int, List[int]]:
    """Find inner blobs fully enclosed by exactly one outer (2 or 8) blob."""
    rows, cols = len(g), len(g[0])
    inners_for_outer: DefaultDict[int, List[int]] = defaultdict(list)
    for i, blob in enumerate(atomic_blobs):
        if blob['num'] == bg or blob['num'] in (2, 8):
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
    """Build composite objects from outer 2/8 blobs and their inners, excluding used inners as outers."""
    used_as_inner: set[int] = set()
    for inner_list in inners_for_outer.values():
        used_as_inner.update(inner_list)
    objects: List[Dict] = []
    for i, blob in enumerate(atomic_blobs):
        if blob['num'] not in (2, 8) or i in used_as_inner:
            continue
        obj: Dict = {
            'outer_i': i,
            'inner_is': inners_for_outer[i],
            'positions': blob['positions'],
            'min_r': blob['min_r'],
            'max_r': blob['max_r'],
            'min_c': blob['min_c'],
            'max_c': blob['max_c'],
            'outer_num': blob['num'],
            'original_min_c': blob['min_c']
        }
        objects.append(obj)
    return objects

def place_obj(out: List[List[int]], atomic_blobs: List[Dict], obj: Dict, shift_r: int, shift_c: int) -> None:
    """Place outer and all associated inners at shifted position, bounds-checked."""
    rows, cols = len(out), len(out[0])
    outer_num = obj['outer_num']
    for r, c in obj['positions']:
        nr = r + shift_r
        nc = c + shift_c
        if 0 <= nr < rows and 0 <= nc < cols:
            out[nr][nc] = outer_num
    for inner_i in obj['inner_is']:
        inner_blob = atomic_blobs[inner_i]
        inner_num = inner_blob['num']
        for r, c in inner_blob['positions']:
            nr = r + shift_r
            nc = c + shift_c
            if 0 <= nr < rows and 0 <= nc < cols:
                out[nr][nc] = inner_num

def is_solid_top(g: List[List[int]], obj: Dict, outer_num: int) -> bool:
    """Check if the top row of the object's bounding box is entirely outer_num in the input grid."""
    min_r = obj['min_r']
    min_c = obj['min_c']
    max_c = obj['max_c']
    cols = len(g[0])
    for c in range(min_c, max_c + 1):
        if 0 <= c < cols and g[min_r][c] != outer_num:
            return False
    return True

def place_group(out: List[List[int]], atomic_blobs: List[Dict], group: List[Dict], outer_num: int) -> None:
    """Place a group of objects for a specific outer_num, stacking horizontally if overlapping or touching in rows."""
    if not group:
        return
    rows, cols = len(out), len(out[0])
    def base_col(o: Dict) -> int:
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
        place_col = base_col(obj)
        if not new_stack:
            place_col = current_right + 1
            if place_col + width - 1 >= cols:
                new_stack = True
                place_col = base_col(obj)
        shift_c = place_col - obj_min_c
        shift_r = 0
        if is_touch and not new_stack:
            solid_top = is_solid_top(g, obj, outer_num)
            solid_bottom = all(out[current_max_r][c] == outer_num for c in range(current_stack_min_col, current_right + 1) if 0 <= c < cols)
            if solid_top and solid_bottom:
                shift_r = -1
        place_obj(out, atomic_blobs, obj, shift_r, shift_c)
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
    """Main program: extract blobs, build objects, place 8s then 2s with stacking rules."""
    bg = get_bg(g)
    out = [[bg] * len(g[0]) for _ in range(len(g))]
    atomic_blobs = extract_atomic_blobs(g, bg)
    inners_for_outer = find_inners(g, bg, atomic_blobs)
    all_objects = build_objects(atomic_blobs, inners_for_outer)
    eight_objects = [o for o in all_objects if o['outer_num'] == 8]
    two_objects = [o for o in all_objects if o['outer_num'] == 2]
    place_group(out, atomic_blobs, eight_objects, 8)
    place_group(out, atomic_blobs, two_objects, 2)
    return out
```