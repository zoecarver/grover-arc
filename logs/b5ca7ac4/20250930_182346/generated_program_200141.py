```python
from typing import List, Dict, DefaultDict, Tuple
from collections import defaultdict

directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_bg(g: List[List[int]]) -> int:
    return g[0][0]

def extract_atomic_blobs(g: List[List[int]], bg: int) -> List[Dict]:
    rows: int = len(g)
    cols: int = len(g[0])
    visited: List[List[bool]] = [[False] * cols for _ in range(rows)]
    blobs: List[Dict] = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                num: int = g[r][c]
                positions: List[Tuple[int, int]] = []
                stack: List[Tuple[int, int]] = [(r, c)]
                visited[r][c] = True
                positions.append((r, c))
                min_r: int = r
                max_r: int = r
                min_c: int = c
                max_c: int = c
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in directions:
                        nr: int = cr + dr
                        nc: int = cc + dc
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
    for r, c in positions:
        for dr, dc in directions:
            nr: int = r + dr
            nc: int = c + dc
            if not (0 <= nr < rows and 0 <= nc < cols) or g[nr][nc] == bg:
                return True
    return False

def get_adj_nums(positions: List[Tuple[int, int]], g: List[List[int]], bg: int, rows: int, cols: int) -> set[int]:
    adj: set[int] = set()
    if not positions:
        return adj
    self_num: int = g[positions[0][0]][positions[0][1]]
    for r, c in positions:
        for dr, dc in directions:
            nr: int = r + dr
            nc: int = c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nnum: int = g[nr][nc]
                if nnum != bg and nnum != self_num:
                    adj.add(nnum)
    return adj

def blobs_adjacent(pos1: List[Tuple[int, int]], pos2: List[Tuple[int, int]]) -> bool:
    pos_set: set[Tuple[int, int]] = set(pos2)
    for r, c in pos1:
        for dr, dc in directions:
            nr: int = r + dr
            nc: int = c + dc
            if (nr, nc) in pos_set:
                return True
    return False

def find_inners(g: List[List[int]], bg: int, atomic_blobs: List[Dict]) -> DefaultDict[int, List[int]]:
    rows: int = len(g)
    cols: int = len(g[0])
    inners_for_outer: DefaultDict[int, List[int]] = defaultdict(list)
    for i, blob in enumerate(atomic_blobs):
        if blob['num'] == bg:
            continue
        if touches_bg(blob['positions'], g, bg, rows, cols):
            continue
        adj_nums: set[int] = get_adj_nums(blob['positions'], g, bg, rows, cols)
        if len(adj_nums) != 1:
            continue
        outer_num: int = next(iter(adj_nums))
        if outer_num not in (2, 8):
            continue
        found_outer: int | None = None
        for j, ob in enumerate(atomic_blobs):
            if ob['num'] == outer_num and blobs_adjacent(blob['positions'], ob['positions']):
                found_outer = j
                break
        if found_outer is not None:
            inners_for_outer[found_outer].append(i)
    return inners_for_outer

def build_objects(atomic_blobs: List[Dict], inners_for_outer: DefaultDict[int, List[int]]) -> List[Dict]:
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

def is_solid_top(g: List[List[int]], obj: Dict, outer_num: int) -> bool:
    min_r: int = obj['min_r']
    min_c: int = obj['min_c']
    max_c: int = obj['max_c']
    cols: int = len(g[0])
    for c in range(min_c, max_c + 1):
        if 0 <= c < cols and g[min_r][c] != outer_num:
            return False
    return True

def place_obj(out: List[List[int]], atomic: List[Dict], obj: Dict, shift_r: int, shift_c: int) -> None:
    outer_num: int = obj['outer_num']
    rows: int = len(out)
    cols: int = len(out[0])
    for r, c in obj['positions']:
        nr: int = r + shift_r
        nc: int = c + shift_c
        if 0 <= nr < rows and 0 <= nc < cols:
            out[nr][nc] = outer_num
    for inner_i in obj['inner_is']:
        inner_num: int = atomic[inner_i]['num']
        for r, c in atomic[inner_i]['positions']:
            nr: int = r + shift_r
            nc: int = c + shift_c
            if 0 <= nr < rows and 0 <= nc < cols:
                out[nr][nc] = inner_num

def place_group(out: List[List[int]], atomic: List[Dict], group: List[Dict], outer_num: int, g: List[List[int]], bg: int) -> None:
    if not group:
        return
    rows: int = len(out)
    cols: int = len(out[0])
    def base_col(o: Dict) -> int:
        if outer_num == 8:
            return 0
        return 12 if o['original_min_c'] < 9 else 17
    group.sort(key=lambda o: (o['min_r'], o['min_c']))
    current_max_r: int = -100
    current_right: int = -1
    current_stack_min_col: int = cols
    for obj in group:
        obj_min_r: int = obj['min_r']
        obj_max_r: int = obj['max_r']
        obj_min_c: int = obj['min_c']
        obj_max_c: int = obj['max_c']
        width: int = obj_max_c - obj_min_c + 1
        is_touch: bool = (obj_min_r == current_max_r + 1)
        is_overlap: bool = (obj_min_r <= current_max_r)
        new_stack: bool = not (is_overlap or is_touch)
        place_col: int = base_col(obj)
        if not new_stack:
            place_col = current_right + 1
            if place_col + width - 1 >= cols:
                new_stack = True
                is_touch = False
                is_overlap = False
                place_col = base_col(obj)
        shift_c: int = place_col - obj_min_c
        shift_r: int = 0
        if is_touch and not new_stack:
            solid_top: bool = is_solid_top(g, obj, outer_num)
            solid_bottom: bool = all(out[current_max_r][c] == outer_num for c in range(current_stack_min_col, current_right + 1) if 0 <= c < cols)
            if solid_top and solid_bottom:
                shift_r = -1
        place_obj(out, atomic, obj, shift_r, shift_c)
        placed_min_r: int = obj_min_r + shift_r
        placed_max_r: int = obj_max_r + shift_r
        placed_min_c: int = obj_min_c + shift_c
        placed_max_c: int = obj_max_c + shift_c
        # Fill above if top not solid
        if placed_min_r > 0:
            top_solid: bool = all(out[placed_min_r][c] == outer_num for c in range(placed_min_c, placed_max_c + 1))
            if not top_solid:
                fill_row: int = placed_min_r - 1
                for c in range(placed_min_c, placed_max_c + 1):
                    if 0 <= c < cols and out[fill_row][c] == bg:
                        out[fill_row][c] = outer_num
        # Original gap fill for touch no shift
        if shift_r == 0 and is_touch and not new_stack:
            fill_left: int = current_right + 1
            fill_right: int = placed_min_c + width - 1
            for cc in range(max(0, fill_left), min(cols, fill_right + 1)):
                out[current_max_r][cc] = outer_num
        current_max_r = max(current_max_r, placed_max_r)
        current_right = max(current_right, placed_max_c)
        if new_stack:
            current_stack_min_col = placed_min_c
        else:
            current_stack_min_col = min(current_stack_min_col, placed_min_c)

def program(g: List[List[int]]) -> List[List[int]]:
    bg: int = get_bg(g)
    atomic_blobs: List[Dict] = extract_atomic_blobs(g, bg)
    inners_for_outer: DefaultDict[int, List[int]] = find_inners(g, bg, atomic_blobs)
    objects: List[Dict] = build_objects(atomic_blobs, inners_for_outer)
    out: List[List[int]] = [[bg] * len(g[0]) for _ in range(len(g))]
    groups: DefaultDict[int, List[Dict]] = defaultdict(list)
    for obj in objects:
        groups[obj['outer_num']].append(obj)
    if 8 in groups:
        place_group(out, atomic_blobs, groups[8], 8, g, bg)
    if 2 in groups:
        place_group(out, atomic_blobs, groups[2], 2, g, bg)
    return out
```