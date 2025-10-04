```python
from typing import List, Tuple
import copy

def find_rect_components(grid: List[List[int]], target: int) -> List[Tuple[int, int, int, int]]:
    h = len(grid)
    if h == 0:
        return []
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if grid[i][j] == target and not visited[i][j]:
                minr, maxr, minc, maxc = i, i, j, j
                size = 0
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    size += 1
                    minr = min(minr, x)
                    maxr = max(maxr, x)
                    minc = min(minc, y)
                    maxc = max(maxc, y)
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == target and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                bb_h = maxr - minr + 1
                bb_w = maxc - minc + 1
                if size == bb_h * bb_w:
                    components.append((minr, maxr, minc, maxc))
    return components

def find_struct_bboxes(grid: List[List[int]], bg: int) -> List[Tuple[int, int, int, int]]:
    h = len(grid)
    if h == 0:
        return []
    w = len(grid[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if grid[i][j] != bg and grid[i][j] != 2 and not visited[i][j]:
                minr, maxr, minc, maxc = i, i, j, j
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    minr = min(minr, x)
                    maxr = max(maxr, x)
                    minc = min(minc, y)
                    maxc = max(maxc, y)
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] != bg and grid[nx][ny] != 2 and not visited[nx][ny]:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((minr, maxr, minc, maxc))
    return components

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return copy.deepcopy(g)
    height = len(g)
    width = len(g[0])
    bg = g[0][0]
    result = copy.deepcopy(g)
    two_comps = find_rect_components(result, 2)
    two_comps.sort(key=lambda x: (x[0], x[2]))
    struct_comps = find_struct_bboxes(result, bg)
    for comp in two_comps:
        min_r, max_r, min_c, max_c = comp
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        center_r = (min_r + max_r) / 2.0
        center_c = (min_c + max_c) / 2.0
        closest_str = None
        min_dist = float('inf')
        str_center_r = 0.0
        str_center_c = 0.0
        for s in struct_comps:
            s_min_r, s_max_r, s_min_c, s_max_c = s
            s_center_r = (s_min_r + s_max_r) / 2.0
            s_center_c = (s_min_c + s_max_c) / 2.0
            dist = abs(center_r - s_center_r) + abs(center_c - s_center_c)
            if dist < min_dist:
                min_dist = dist
                closest_str = s
                str_center_r = s_center_r
                str_center_c = s_center_c
        if closest_str is None:
            for rr in range(min_r, max_r + 1):
                for cc in range(min_c, max_c + 1):
                    result[rr][cc] = bg
            continue
        moved = False
        # Vertical move
        possible_v = []
        for p_min_r in range(height - h + 1):
            p_max_r = p_min_r + h - 1
            all_bg = all(all(result[rr][cc] == bg for cc in range(min_c, max_c + 1)) for rr in range(p_min_r, p_max_r + 1))
            if not all_bg:
                continue
            valid = True
            for p_r in range(p_min_r, p_max_r + 1):
                run_start = min_c
                while run_start > 0 and result[p_r][run_start - 1] == bg:
                    run_start -= 1
                run_end = max_c
                while run_end < width - 1 and result[p_r][run_end + 1] == bg:
                    run_end += 1
                if run_start > min_c or run_end < max_c:
                    valid = False
                    break
                left_struct = run_start > 0 and result[p_r][run_start - 1] != bg and result[p_r][run_start - 1] != 2
                right_struct = run_end < width - 1 and result[p_r][run_end + 1] != bg and result[p_r][run_end + 1] != 2
                if left_struct and right_struct:
                    continue
                if left_struct and not right_struct:
                    if min_c == run_start:
                        continue
                elif right_struct and not left_struct:
                    if max_c == run_end:
                        continue
                valid = False
                break
            if not valid:
                continue
            if p_min_r > max_r:
                gap_start = max_r + 1
                gap_end = p_min_r - 1
            elif p_max_r < min_r:
                gap_start = p_max_r + 1
                gap_end = min_r - 1
            else:
                continue
            if gap_start > gap_end:
                continue
            gap_len = gap_end - gap_start + 1
            if gap_len > 8:
                continue
            gap_bg = all(all(result[rr][cc] == bg for cc in range(min_c, max_c + 1)) for rr in range(gap_start, gap_end + 1))
            if not gap_bg:
                continue
            p_center_r = (p_min_r + p_max_r) / 2.0
            score_dist_str = abs(p_center_r - str_center_r)
            possible_v.append((p_min_r, gap_len, p_center_r, score_dist_str))
        if possible_v:
            possible_v.sort(key=lambda x: (x[3], x[1], abs(x[2] - center_r)))
            best_p_min_r = possible_v[0][0]
            p_max_r = best_p_min_r + h - 1
            for rr in range(best_p_min_r, p_max_r + 1):
                for cc in range(min_c, max_c + 1):
                    result[rr][cc] = 2
            for rr in range(min_r, max_r + 1):
                for cc in range(min_c, max_c + 1):
                    result[rr][cc] = 0
            if best_p_min_r > max_r:
                gap_start = max_r + 1
                gap_end = best_p_min_r - 1
            else:
                gap_start = p_max_r + 1
                gap_end = min_r - 1
            for rr in range(gap_start, gap_end + 1):
                for cc in range(min_c, max_c + 1):
                    result[rr][cc] = 0
            moved = True
        if not moved:
            # Horizontal move
            possible_h = []
            for p_min_c in range(width - w + 1):
                p_max_c = p_min_c + w - 1
                all_bg = all(all(result[rr][cc] == bg for cc in range(p_min_c, p_max_c + 1)) for rr in range(min_r, max_r + 1))
                if not all_bg:
                    continue
                valid = True
                for rr in range(min_r, max_r + 1):
                    run_start = p_min_c
                    while run_start > 0 and result[rr][run_start - 1] == bg:
                        run_start -= 1
                    run_end = p_max_c
                    while run_end < width - 1 and result[rr][run_end + 1] == bg:
                        run_end += 1
                    if run_start > p_min_c or run_end < p_max_c:
                        valid = False
                        break
                    left_struct = run_start > 0 and result[rr][run_start - 1] != bg and result[rr][run_start - 1] != 2
                    right_struct = run_end < width - 1 and result[rr][run_end + 1] != bg and result[rr][run_end + 1] != 2
                    if left_struct and right_struct:
                        continue
                    if left_struct and not right_struct:
                        if p_min_c == run_start:
                            continue
                    elif right_struct and not left_struct:
                        if p_max_c == run_end:
                            continue
                    valid = False
                    break
                if not valid:
                    continue
                if p_min_c > max_c:
                    gap_start = max_c + 1
                    gap_end = p_min_c - 1
                elif p_max_c < min_c:
                    gap_start = p_max_c + 1
                    gap_end = min_c - 1
                else:
                    continue
                if gap_start > gap_end:
                    continue
                gap_len = gap_end - gap_start + 1
                if gap_len > 8:
                    continue
                gap_bg = all(all(result[rr][cc] == bg for cc in range(gap_start, gap_end + 1)) for rr in range(min_r, max_r + 1))
                if not gap_bg:
                    continue
                p_center_c = (p_min_c + p_max_c) / 2.0
                score_dist_str = abs(p_center_c - str_center_c)
                possible_h.append((p_min_c, gap_len, p_center_c, score_dist_str))
            if possible_h:
                possible_h.sort(key=lambda x: (x[3], x[1], abs(x[2] - center_c)))
                best_p_min_c = possible_h[0][0]
                p_max_c = best_p_min_c + w - 1
                for rr in range(min_r, max_r + 1):
                    for cc in range(best_p_min_c, p_max_c + 1):
                        result[rr][cc] = 2
                for rr in range(min_r, max_r + 1):
                    for cc in range(min_c, max_c + 1):
                        result[rr][cc] = 0
                if best_p_min_c > max_c:
                    gap_start = max_c + 1
                    gap_end = best_p_min_c - 1
                else:
                    gap_start = p_max_c + 1
                    gap_end = min_c - 1
                for rr in range(min_r, max_r + 1):
                    for cc in range(gap_start, gap_end + 1):
                        result[rr][cc] = 0
                moved = True
        if not moved:
            for rr in range(min_r, max_r + 1):
                for cc in range(min_c, max_c + 1):
                    result[rr][cc] = bg
    return result
```