```python
from typing import List, Tuple
from collections import Counter

def get_background_color(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_structures_bboxes(g: List[List[int]], bg: int, red: int = 2) -> List[Tuple[int, int, int, int]]:
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    bboxes = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and g[r][c] != bg and g[r][c] != red:
                min_r, max_r = r, r
                min_c, max_c = c, c
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] != bg and g[nr][nc] != red:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                bboxes.append((min_r, min_c, max_r, max_c))
    return bboxes

def is_inside_any_bbox(r: int, c: int, bboxes: List[Tuple[int, int, int, int]]) -> bool:
    for min_r, min_c, max_r, max_c in bboxes:
        if min_r <= r <= max_r and min_c <= c <= max_c:
            return True
    return False

def find_red_rects(g: List[List[int]], red: int = 2) -> List[Tuple[int, int, int, int]]:
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    rects = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == red and not visited[r][c]:
                component_size = 0
                min_r, max_r = r, r
                min_c, max_c = c, c
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    cr, cc = stack.pop()
                    component_size += 1
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == red and not visited[nr][nc]:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                h = max_r - min_r + 1
                w = max_c - min_c + 1
                if component_size == h * w:
                    all_filled = all(g[rr][cc] == red for rr in range(min_r, max_r + 1) for cc in range(min_c, max_c + 1))
                    if all_filled:
                        rects.append((min_r, min_c, max_r, max_c))
    return rects

def process_horizontal_moves(g: List[List[int]], bg: int, bboxes: List[Tuple[int, int, int, int]], red: int = 2) -> List[List[int]]:
    out = [row[:] for row in g]
    rows = len(out)
    cols = len(out[0])
    for r in range(rows):
        c = 0
        while c < cols:
            if out[r][c] != bg and out[r][c] != red:
                j = c
                while j < cols and out[r][j] != bg and out[r][j] != red:
                    j += 1
                c = j
                continue
            if out[r][c] == red:
                is_single = True
                if c > 0 and out[r][c - 1] == red:
                    is_single = False
                if c + 1 < cols and out[r][c + 1] == red:
                    is_single = False
                if is_single:
                    k = c - 1
                    while k >= 0 and out[r][k] == bg:
                        k -= 1
                    if k >= 0 and out[r][k] != bg and out[r][k] != red:
                        place = k + 1
                        if place < c and out[r][place] == bg and is_inside_any_bbox(r, place, bboxes):
                            out[r][place] = red
                            for jc in range(place + 1, c + 1):
                                out[r][jc] = 0
                c += 1
                continue
            c += 1
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background_color(g)
    bboxes = get_structures_bboxes(g, bg)
    red_rects = find_red_rects(g)
    out = [row[:] for row in g]
    rows = len(out)
    red = 2
    for rect in red_rects:
        min_r, min_c, max_r, max_c = rect
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        moved = False
        # Try move up
        structure_bottoms = [None] * w
        path_clear = True
        for idx, cc in enumerate(range(min_c, max_c + 1)):
            k = min_r - 1
            while k >= 0 and out[k][cc] == bg:
                k -= 1
            if k < 0 or out[k][cc] == red or out[k][cc] == bg:
                path_clear = False
                break
            sb = k
            while sb < rows and out[sb][cc] != bg and out[sb][cc] != red:
                sb += 1
            sb -= 1
            structure_bottoms[idx] = sb
        if path_clear and len(set(structure_bottoms)) == 1 and structure_bottoms[0] is not None:
            s = structure_bottoms[0]
            place_start = s + 1
            place_end = place_start + h - 1
            if place_end < min_r:
                can_place = True
                for pr in range(place_start, place_end + 1):
                    for pc in range(min_c, max_c + 1):
                        if out[pr][pc] != bg or not is_inside_any_bbox(pr, pc, bboxes):
                            can_place = False
                            break
                    if not can_place:
                        break
                if can_place:
                    for pr in range(place_start, place_end + 1):
                        for pc in range(min_c, max_c + 1):
                            out[pr][pc] = red
                    for fr in range(place_end + 1, max_r + 1):
                        for pc in range(min_c, max_c + 1):
                            out[fr][pc] = 0
                    moved = True
        if not moved:
            # Try move down
            structure_tops = [None] * w
            path_clear = True
            for idx, cc in enumerate(range(min_c, max_c + 1)):
                k = max_r + 1
                while k < rows and out[k][cc] == bg:
                    k += 1
                if k >= rows or out[k][cc] == red or out[k][cc] == bg:
                    path_clear = False
                    break
                st = k
                while st > 0 and out[st - 1][cc] != bg and out[st - 1][cc] != red:
                    st -= 1
                structure_tops[idx] = st
            if path_clear and len(set(structure_tops)) == 1 and structure_tops[0] is not None:
                t = structure_tops[0]
                place_end = t - 1
                place_start = place_end - h + 1
                if place_start > max_r:
                    can_place = True
                    for pr in range(place_start, place_end + 1):
                        for pc in range(min_c, max_c + 1):
                            if out[pr][pc] != bg or not is_inside_any_bbox(pr, pc, bboxes):
                                can_place = False
                                break
                        if not can_place:
                            break
                    if can_place:
                        for pr in range(place_start, place_end + 1):
                            for pc in range(min_c, max_c + 1):
                                out[pr][pc] = red
                        for fr in range(min_r, place_start):
                            for pc in range(min_c, max_c + 1):
                                out[fr][pc] = 0
                        moved = True
    # Process horizontal moves
    out = process_horizontal_moves(out, bg, bboxes)
    # Remove remaining reds not moved
    cols = len(out[0])
    for r in range(rows):
        for c in range(cols):
            if out[r][c] == red:
                out[r][c] = bg
    return out
```