```python
import math
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    size = len(g)
    total_cells = sum(sum(1 for cell in row if cell > 0) for row in g)
    n = int(math.sqrt(total_cells))
    if n * n != total_cells:
        raise ValueError("Total cells must form a perfect square")

    visited = [[False] * size for _ in range(size)]
    comps = []  # list of (color, list of (r, c))

    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for i in range(size):
        for j in range(size):
            if g[i][j] > 0 and not visited[i][j]:
                color = g[i][j]
                component: List[Tuple[int, int]] = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in dirs:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < size and 0 <= ny < size and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                comps.append((color, component))

    # Sort components by decreasing max row, tie by decreasing color
    comps.sort(key=lambda p: (-max(r for r, c in p[1]), -p[0]))

    output_grid = [[0] * n for _ in range(n)]

    def get_best_placement(rel_pos: List[Tuple[int, int]], h: int, w: int, color: int) -> Tuple[int, int, List[Tuple[int, int]]]:
        best_pr = n + 1
        best_pc = n + 1
        best_rel = []
        for pr in range(n - h + 1):
            found_pc = False
            for pc in range(n - w + 1):
                if all(output_grid[pr + dr][pc + dc] == 0 for dr, dc in rel_pos):
                    best_pr = pr
                    best_pc = pc
                    best_rel = rel_pos[:]
                    found_pc = True
                    break
            if found_pc:
                break
        return best_pr, best_pc, best_rel

    for color, orig_pos in comps:
        if not orig_pos:
            continue
        min_r = min(r for r, c in orig_pos)
        max_r = max(r for r, c in orig_pos)
        min_c = min(c for r, c in orig_pos)
        max_c = max(c for r, c in orig_pos)
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        rel_pos = [(r - min_r, c - min_c) for r, c in orig_pos]

        candidates = []
        current_rel = rel_pos[:]
        current_h = h
        current_w = w
        for k in range(4):
            pr, pc, this_rel = get_best_placement(current_rel, current_h, current_w, color)
            if pr <= n:
                candidates.append((pr, pc, k, this_rel))
            if k < 3:
                # Rotate 90 CW
                new_pos = [(cc, current_h - 1 - rr) for rr, cc in current_rel]
                nr_min = min(nr for nr, nc in new_pos)
                nc_min = min(nc for nr, nc in new_pos)
                current_rel = [(nr - nr_min, nc - nc_min) for nr, nc in new_pos]
                current_h = max(nr - nr_min for nr, nc in new_pos) + 1 if new_pos else 0
                current_w = max(nc - nc_min for nr, nc in new_pos) + 1 if new_pos else 0

        if not candidates:
            raise ValueError("No placement found")
        # Choose best: min pr, then min pc, then min k
        candidates.sort(key=lambda x: (x[0], x[1], x[2]))
        _, best_pc, _, best_rel = candidates[0]
        best_pr = candidates[0][0]
        # Place
        for dr, dc in best_rel:
            output_grid[best_pr + dr][best_pc + dc] = color

    return output_grid
```