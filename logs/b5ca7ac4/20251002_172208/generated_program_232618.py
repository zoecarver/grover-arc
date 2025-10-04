```python
from collections import Counter, deque
from typing import List, Dict, Set, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def extract_shapes(g: List[List[int]], frame_color: int, bg: int, n: int, excluded: Set[Tuple[int, int]] = None) -> Tuple[List[Dict[str, int]], Set[Tuple[int, int]]]:
    if excluded is None:
        excluded = set()
    visited = [[False] * n for _ in range(n)]
    shapes: List[Dict[str, int]] = []
    used: Set[Tuple[int, int]] = set()
    directions4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    directions8 = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if not (dx == 0 and dy == 0)]
    for i in range(n):
        for j in range(n):
            if g[i][j] == frame_color and not visited[i][j] and (i, j) not in excluded:
                frame_cells: List[Tuple[int, int]] = []
                q = deque([(i, j)])
                visited[i][j] = True
                frame_cells.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions4:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny] and g[nx][ny] == frame_color and (nx, ny) not in excluded:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            frame_cells.append((nx, ny))
                inner_seeds: Set[Tuple[int, int]] = set()
                for x, y in frame_cells:
                    for dx, dy in directions8:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in inner_seeds and g[nx][ny] != bg and g[nx][ny] != frame_color and (nx, ny) not in excluded:
                            inner_seeds.add((nx, ny))
                inner_cells: Set[Tuple[int, int]] = set()
                inner_visited: Set[Tuple[int, int]] = set()
                for sx, sy in inner_seeds:
                    if (sx, sy) not in inner_visited:
                        q = deque([(sx, sy)])
                        inner_visited.add((sx, sy))
                        inner_cells.add((sx, sy))
                        while q:
                            x, y = q.popleft()
                            for dx, dy in directions4:
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in inner_visited and g[nx][ny] != bg and g[nx][ny] != frame_color and (nx, ny) not in excluded:
                                    inner_visited.add((nx, ny))
                                    q.append((nx, ny))
                                    inner_cells.add((nx, ny))
                all_cells = frame_cells + list(inner_cells)
                if all_cells:
                    rs = [r for r, c in all_cells]
                    cs = [c for r, c in all_cells]
                    shapes.append({
                        'minr': min(rs),
                        'maxr': max(rs),
                        'minc': min(cs),
                        'maxc': max(cs),
                        'cells': all_cells
                    })
                    for pos in all_cells:
                        used.add(pos)
    return shapes, used

def group_blocks(shapes: List[Dict[str, int]]) -> List[List[Dict[str, int]]]:
    if not shapes:
        return []
    shapes = sorted(shapes, key=lambda s: s['minr'])
    blocks: List[List[Dict[str, int]]] = []
    curr_block = [shapes[0]]
    cur_maxr = shapes[0]['maxr']
    for s in shapes[1:]:
        if s['minr'] <= cur_maxr:
            curr_block.append(s)
            cur_maxr = max(cur_maxr, s['maxr'])
        else:
            blocks.append(curr_block)
            curr_block = [s]
            cur_maxr = s['maxr']
    blocks.append(curr_block)
    return blocks

def place_blocks(out: List[List[int]], g: List[List[int]], blocks: List[List[Dict[str, int]]], n: int, left: bool):
    for block in blocks:
        if not block:
            continue
        block = sorted(block, key=lambda s: s['minc'])
        widths = [s['maxc'] - s['minc'] + 1 for s in block]
        total_w = sum(widths)
        start_col = 0 if left else n - total_w
        cum = 0
        for idx, s in enumerate(block):
            delta = start_col + cum - s['minc']
            for r, c in s['cells']:
                new_c = c + delta
                if 0 <= new_c < n:
                    out[r][new_c] = g[r][c]
            cum += widths[idx]

def program(g: List[List[int]]) -> List[List[int]]:
    n = 22
    bg = get_background(g)
    left_shapes, used_left = extract_shapes(g, 8, bg, n)
    right_shapes, _ = extract_shapes(g, 2, bg, n, excluded=used_left)
    blocks_left = group_blocks(left_shapes)
    blocks_right = group_blocks(right_shapes)
    out = [[bg] * n for _ in range(n)]
    place_blocks(out, g, blocks_left, n, left=True)
    place_blocks(out, g, blocks_right, n, left=False)
    return out
```