```python
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def get_nonbg_segments(line: List[int], bg: int) -> List[Tuple[int, int, int]]:
    segments = []
    n = len(line)
    i = 0
    while i < n:
        if line[i] != bg and line[i] != 2:
            start = i
            while i < n and line[i] != bg and line[i] != 2:
                i += 1
            end = i - 1
            length = end - start + 1
            segments.append((start, end, length))
        else:
            i += 1
    return segments

def get_nonbg_segments_col(grid: List[List[int]], col: int, bg: int) -> List[Tuple[int, int, int]]:
    segments = []
    rows = len(grid)
    i = 0
    while i < rows:
        if grid[i][col] != bg and grid[i][col] != 2:
            start = i
            while i < rows and grid[i][col] != bg and grid[i][col] != 2:
                i += 1
            end = i - 1
            length = end - start + 1
            segments.append((start, end, length))
        else:
            i += 1
    return segments

def find_components(grid: List[List[int]], bg: int) -> List[Tuple[List[Tuple[int, int]], int, int, int, int, int]]:
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2 and not visited[r][c]:
                component = []
                min_r = max_r = r
                min_c = max_c = c
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    min_r = min(min_r, x)
                    max_r = max(max_r, x)
                    min_c = min(min_c, y)
                    max_c = max(max_c, y)
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((component, min_r, max_r, min_c, max_c, len(component)))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    out = [row[:] for row in g]
    bg = get_background(g)
    components = find_components(g, bg)
    for comp_info in components:
        comp, min_r, max_r, min_c, max_c, comp_size = comp_info
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        if height * width != comp_size:
            for rr, cc in comp:
                out[rr][cc] = bg
            continue
        if height == 1:
            r = min_r
            line = g[r]
            segs = get_nonbg_segments(line, bg)
            qual_segs = [(s_left, s_right, ln) for s_left, s_right, ln in segs if ln > 1]
            # find best left
            max_targ_r = -float('inf')
            for s_left, s_right, _ in qual_segs:
                if s_right < min_c:
                    max_targ_r = max(max_targ_r, s_right)
            gap_l = min_c - max_targ_r - 1 if max_targ_r != -float('inf') else float('inf')
            # best right
            min_targ_l = float('inf')
            for s_left, s_right, _ in qual_segs:
                if s_left > max_c:
                    min_targ_l = min(min_targ_l, s_left)
            gap_r = min_targ_l - max_c - 1 if min_targ_l != float('inf') else float('inf')
            do_h = False
            dir_h = None
            targ_h = None
            if gap_l <= 8 and gap_l <= gap_r:
                do_h = True
                dir_h = 'left'
                targ_h = max_targ_r
            elif gap_r <= 8:
                do_h = True
                dir_h = 'right'
                targ_h = min_targ_l
            if do_h:
                if dir_h == 'left':
                    new_left = targ_h + 1 - (width - 1)
                    new_right = new_left + width - 1
                    for cc in range(new_left, new_right + 1):
                        if 0 <= cc < len(line):
                            out[r][cc] = 2
                    for cc in range(new_right + 1, max_c + 1):
                        out[r][cc] = 0
                else:
                    new_right = targ_h - 1
                    new_left = new_right - width + 1
                    for cc in range(new_left, new_right + 1):
                        if 0 <= cc < len(line):
                            out[r][cc] = 2
                    for cc in range(min_c, new_left):
                        out[r][cc] = 0
                continue
            # else vertical per position
            for c in range(min_c, max_c + 1):
                segs_v = get_nonbg_segments_col(g, c, bg)
                gap_v = float('inf')
                dir_v = None
                targ_v = None
                for s_start, s_end, ln in segs_v:
                    if ln >= 1:
                        if r > s_end:
                            gapp = r - s_end - 1
                            if gapp < gap_v:
                                gap_v = gapp
                                dir_v = 'up'
                                targ_v = s_end
                        if r < s_start:
                            gapp = s_start - r - 1
                            if gapp < gap_v:
                                gap_v = gapp
                                dir_v = 'down'
                                targ_v = s_start
                if gap_v <= 8:
                    if dir_v == 'up':
                        new_rr = targ_v + 1
                        out[new_rr][c] = 2
                        for rrr in range(new_rr + 1, r + 1):
                            out[rrr][c] = 0
                    else:
                        new_rr = targ_v - 1
                        out[new_rr][c] = 2
                        for rrr in range(r, new_rr):
                            out[rrr][c] = 0
                else:
                    out[r][c] = bg
            continue
        if width == 1:
            c = min_c
            segs_v = get_nonbg_segments_col(g, c, bg)
            gap_v = float('inf')
            dir_v = None
            targ_v = None
            for s_start, s_end, ln in segs_v:
                if ln >= height:
                    if max_r < s_start:
                        gapp = s_start - max_r - 1
                        if gapp < gap_v:
                            gap_v = gapp
                            dir_v = 'down'
                            targ_v = s_start
                    if min_r > s_end:
                        gapp = min_r - s_end - 1
                        if gapp < gap_v:
                            gap_v = gapp
                            dir_v = 'up'
                            targ_v = s_end
            if gap_v <= 8 and gap_v >= 0:
                if dir_v == 'down':
                    new_top = targ_v - height
                    for rr in range(new_top, new_top + height):
                        out[rr][c] = 2
                    for rr in range(min_r, new_top):
                        out[rr][c] = 0
                else:
                    new_top = targ_v + 1 - (height - 1)
                    new_bottom = new_top + height - 1
                    for rr in range(new_top, new_bottom + 1):
                        out[rr][c] = 2
                    for rr in range(new_bottom + 1, max_r + 1):
                        out[rr][c] = 0
                continue
            # else remove
            for rr in range(min_r, max_r + 1):
                out[rr][c] = bg
            continue
        # 2d
        # up
        common_bottoms = None
        can_up = True
        for cc in range(min_c, max_c + 1):
            segs = get_nonbg_segments_col(g, cc, bg)
            this_b = set()
            for s_s, s_e, ln in segs:
                if ln >= height and s_e < min_r:
                    this_b.add(s_e)
            if not this_b:
                can_up = False
                break
            if common_bottoms is None:
                common_bottoms = this_b
            else:
                common_bottoms.intersection_update(this_b)
        up_gap = float('inf')
        up_targ = -1
        if can_up and common_bottoms:
            up_targ = max(common_bottoms)
            up_gap = min_r - up_targ - 1
        # down
        common_tops = None
        can_down = True
        for cc in range(min_c, max_c + 1):
            segs = get_nonbg_segments_col(g, cc, bg)
            this_t = set()
            for s_s, s_e, ln in segs:
                if ln >= height and s_s > max_r:
                    this_t.add(s_s)
            if not this_t:
                can_down = False
                break
            if common_tops is None:
                common_tops = this_t
            else:
                common_tops.intersection_update(this_t)
        down_gap = float('inf')
        down_targ = float('inf')
        if can_down and common_tops:
            down_targ = min(common_tops)
            down_gap = down_targ - max_r - 1
        # choose
        do_v = False
        dir_v = None
        targ_vv = None
        if up_gap <= 8 and up_gap < down_gap:
            do_v = True
            dir_v = 'up'
            targ_vv = up_targ
        elif down_gap <= 8:
            do_v = True
            dir_v = 'down'
            targ_vv = down_targ
        if do_v:
            if dir_v == 'up':
                new_top = targ_vv + 1 - (height - 1)
                new_bottom = new_top + height - 1
                for rr in range(new_top, new_bottom + 1):
                    for cc in range(min_c, max_c + 1):
                        out[rr][cc] = 2
                for rr in range(new_bottom + 1, max_r + 1):
                    for cc in range(min_c, max_c + 1):
                        out[rr][cc] = 0
            else:
                new_top = targ_vv - height
                new_bottom = targ_vv - 1
                for rr in range(new_top, new_bottom + 1):
                    for cc in range(min_c, max_c + 1):
                        out[rr][cc] = 2
                for rr in range(min_r, new_top):
                    for cc in range(min_c, max_c + 1):
                        out[rr][cc] = 0
            continue
        # check has possible line
        has_p = False
        for cc in range(min_c, max_c + 1):
            segs = get_nonbg_segments_col(g, cc, bg)
            for s_s, s_e, ln in segs:
                if ln >= 1:
                    gapp = 0
                    if min_r > s_e:
                        gapp = min_r - s_e - 1
                    elif max_r < s_s:
                        gapp = s_s - max_r - 1
                    if gapp <= 8 and gapp >= 0:
                        has_p = True
                        break
            if has_p:
                break
        if has_p:
            for rr, cc in comp:
                out[rr][cc] = bg
        # else stay
    return out
```