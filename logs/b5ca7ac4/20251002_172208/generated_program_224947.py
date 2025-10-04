```python
from collections import Counter, deque
from typing import List, Dict, Tuple, Set

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_connected_frames(g: List[List[int]], frame_color: int, bg: int, excluded: Set[Tuple[int, int]] = None) -> Tuple[List[Dict], Set[Tuple[int, int]]]:
    n = 22
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
                all_cells = frame_cells + list(inner_cells)
                if all_cells:
                    rs = [r for r, c in all_cells]
                    cs = [c for r, c in all_cells]
                    minr = min(rs)
                    maxr = max(rs)
                    minc = min(cs)
                    maxc = max(cs)
                    shapes.append({
                        'minr': minr,
                        'maxr': maxr,
                        'minc': minc,
                        'maxc': maxc,
                        'all_cells': all_cells
                    })
                    for pos in all_cells:
                        used.add(pos)
    return shapes, used

def group_components(comps: List[Dict]) -> List[List[Dict]]:
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

def place_blocks(out: List[List[int]], g: List[List[int]], blocks: List[List[Dict]], is_left: bool):
    n = 22
    for block in blocks:
        if not block:
            continue
        block_comps = sorted(block, key=lambda d: d['minc'])
        widths = [d['maxc'] - d['minc'] + 1 for d in block_comps]
        total_w = sum(widths)
        b_start = 0 if is_left else n - total_w
        cum = 0
        for idx, comp in enumerate(block_comps):
            delta_c = b_start + cum - comp['minc']
            for r, c in comp['all_cells']:
                new_c = c + delta_c
                if 0 <= new_c < n:
                    out[r][new_c] = g[r][c]
            cum += widths[idx]

def program(g: List[List[int]]) -> List[List[int]]:
    n = 22
    bg = get_background(g)
    out = [[bg] * n for _ in range(n)]
    left_shapes, left_used = find_connected_frames(g, 8, bg)
    right_shapes, _ = find_connected_frames(g, 2, bg, left_used)
    left_blocks = group_components(left_shapes)
    place_blocks(out, g, left_blocks, is_left=True)
    right_blocks = group_components(right_shapes)
    place_blocks(out, g, right_blocks, is_left=False)
    return out
```