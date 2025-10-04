```python
from collections import Counter, deque
from typing import List, Set, Tuple, Dict

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_connected_frames(g: List[List[int]], frame_color: int, bg: int, excluded: Set[Tuple[int, int]] = None, n: int = 22) -> Tuple[List[Dict], Set[Tuple[int, int]]]:
    visited = [[False] * n for _ in range(n)]
    shapes: List[Dict] = []
    used: Set[Tuple[int, int]] = set()
    directions4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    directions8 = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == frame_color and not visited[i][j] and (excluded is None or (i, j) not in excluded):
                frame_cells: List[Tuple[int, int]] = []
                q = deque([(i, j)])
                visited[i][j] = True
                frame_cells.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions4:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == frame_color and (excluded is None or (nx, ny) not in excluded):
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            frame_cells.append((nx, ny))
                inner_seeds: Set[Tuple[int, int]] = set()
                for x, y in frame_cells:
                    for dx, dy in directions8:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] != bg and g[nx][ny] != frame_color and (nx, ny) not in inner_seeds and (excluded is None or (nx, ny) not in excluded):
                            inner_seeds.add((nx, ny))
                inner_visited: Set[Tuple[int, int]] = set()
                inner_cells: Set[Tuple[int, int]] = set()
                for sx, sy in inner_seeds:
                    if (sx, sy) not in inner_visited:
                        q = deque([(sx, sy)])
                        inner_visited.add((sx, sy))
                        inner_cells.add((sx, sy))
                        while q:
                            x, y = q.popleft()
                            for dx, dy in directions4:
                                nx = x + dx
                                ny = y + dy
                                if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in inner_visited and g[nx][ny] != bg and g[nx][ny] != frame_color and (excluded is None or (nx, ny) not in excluded):
                                    inner_visited.add((nx, ny))
                                    q.append((nx, ny))
                                    inner_cells.add((nx, ny))
                all_cells_list = frame_cells + list(inner_cells)
                if all_cells_list:
                    rs = [r for r, _ in all_cells_list]
                    cs = [c for _, c in all_cells_list]
                    minr = min(rs)
                    maxr = max(rs)
                    minc = min(cs)
                    maxc = max(cs)
                    shapes.append({
                        'minr': minr,
                        'maxr': maxr,
                        'minc': minc,
                        'maxc': maxc,
                        'all_cells': all_cells_list
                    })
                    for pos in all_cells_list:
                        used.add(pos)
    return shapes, used

def group_into_blocks(comps: List[Dict]) -> List[List[Dict]]:
    if not comps:
        return []
    comps = sorted(comps, key=lambda d: d['minr'])
    blocks: List[List[Dict]] = []
    current_block = [comps[0]]
    cur_max_r = comps[0]['maxr']
    for comp in comps[1:]:
        if comp['minr'] <= cur_max_r:
            current_block.append(comp)
            cur_max_r = max(cur_max_r, comp['maxr'])
        else:
            blocks.append(current_block)
            current_block = [comp]
            cur_max_r = comp['maxr']
    blocks.append(current_block)
    return blocks

def place_block(out: List[List[int]], g: List[List[int]], block: List[Dict], b_start: int, n: int):
    if not block:
        return
    block = sorted(block, key=lambda s: s['minc'])
    curr_col = b_start
    for comp in block:
        min_c = comp['minc']
        max_c = comp['maxc']
        proposed_delta = curr_col - min_c
        if max_c + proposed_delta > n - 1:
            proposed_delta = (n - 1) - max_c
        for r, c in comp['all_cells']:
            new_c = c + proposed_delta
            if 0 <= new_c < n:
                out[r][new_c] = g[r][c]
        width = max_c - min_c + 1
        curr_col = max(curr_col + width, max_c + proposed_delta + 1)

def program(g: List[List[int]]) -> List[List[int]]:
    n = 22
    bg = get_background(g)
    out = [[bg] * n for _ in range(n)]
    left_shapes, left_used = find_connected_frames(g, 8, bg)
    right_shapes, _ = find_connected_frames(g, 2, bg, left_used)
    left_blocks = group_into_blocks(left_shapes)
    right_blocks = group_into_blocks(right_shapes)
    for block in left_blocks:
        place_block(out, g, block, 0, n)
    for block in right_blocks:
        if not block:
            continue
        min_minc = min(s['minc'] for s in block)
        total_w = sum(s['maxc'] - s['minc'] + 1 for s in block)
        if min_minc <= 8:
            b_start = 12
        else:
            b_start = n - total_w
        place_block(out, g, block, b_start, n)
    return out
```