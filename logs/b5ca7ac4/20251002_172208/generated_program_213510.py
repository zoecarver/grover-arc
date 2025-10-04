```python
from collections import Counter
from typing import List, Set, Dict, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    flat = [cell for row in g for cell in row]
    bg = Counter(flat).most_common(1)[0][0]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    visited: Set[Tuple[int, int]] = set()
    left_shapes: List[Dict] = []
    
    # Extract left shapes: flood from 8 cells, including all non-bg
    for r in range(n):
        for c in range(n):
            if g[r][c] == 8 and (r, c) not in visited:
                shape_cells: Set[Tuple[int, int]] = set()
                stack: List[Tuple[int, int]] = [(r, c)]
                visited.add((r, c))
                shape_cells.add((r, c))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited and g[nx][ny] != bg:
                            visited.add((nx, ny))
                            stack.append((nx, ny))
                            shape_cells.add((nx, ny))
                rs = [rr for rr, _ in shape_cells]
                cs = [cc for _, cc in shape_cells]
                min_r, max_r = min(rs), max(rs)
                min_c, max_c = min(cs), max(cs)
                left_shapes.append({
                    'cells': shape_cells,
                    'minr': min_r,
                    'maxr': max_r,
                    'minc': min_c,
                    'maxc': max_c
                })
    
    right_shapes: List[Dict] = []
    
    # Extract right shapes: flood from 2 cells not visited, including non-bg non-8
    for r in range(n):
        for c in range(n):
            if g[r][c] == 2 and (r, c) not in visited:
                shape_cells: Set[Tuple[int, int]] = set()
                stack: List[Tuple[int, int]] = [(r, c)]
                visited.add((r, c))
                shape_cells.add((r, c))
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in visited and g[nx][ny] != bg and g[nx][ny] != 8:
                            visited.add((nx, ny))
                            stack.append((nx, ny))
                            shape_cells.add((nx, ny))
                if len(shape_cells) > 0:
                    rs = [rr for rr, _ in shape_cells]
                    cs = [cc for _, cc in shape_cells]
                    min_r, max_r = min(rs), max(rs)
                    min_c, max_c = min(cs), max(cs)
                    right_shapes.append({
                        'cells': shape_cells,
                        'minr': min_r,
                        'maxr': max_r,
                        'minc': min_c,
                        'maxc': max_c
                    })
    
    out: List[List[int]] = [[bg for _ in range(n)] for _ in range(n)]
    
    def group_and_place(shapes_list: List[Dict], is_left: bool):
        if not shapes_list:
            return
        shapes_list.sort(key=lambda s: s['minr'])
        blocks = []
        current_block = [shapes_list[0]]
        cur_max_r = shapes_list[0]['maxr']
        i = 1
        while i < len(shapes_list):
            s = shapes_list[i]
            if s['minr'] <= cur_max_r:
                current_block.append(s)
                cur_max_r = max(cur_max_r, s['maxr'])
            else:
                blocks.append(current_block)
                current_block = [s]
                cur_max_r = s['maxr']
            i += 1
        blocks.append(current_block)
        
        for block in blocks:
            block.sort(key=lambda s: s['minc'])
            total_width = sum(s['maxc'] - s['minc'] + 1 for s in block)
            if is_left:
                current_col = 0
            else:
                current_col = n - total_width
            for s in block:
                min_r = s['minr']
                min_c = s['minc']
                delta_col = current_col - min_c
                for rr, cc in s['cells']:
                    new_col = cc + delta_col
                    if 0 <= new_col < n:
                        out[rr][new_col] = g[rr][cc]
                current_col += (s['maxc'] - min_c + 1)
    
    group_and_place(left_shapes, True)
    group_and_place(right_shapes, False)
    
    return out
```