```python
from typing import List
from collections import deque

def program(g: List[List[int]]) -> List[List[int]]:
    H = 30
    W = 30
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    output_grid = [row[:] for row in g]
    # Find 5 components
    comp_id = [[-1] * W for _ in range(H)]
    comp_positions = []
    cid = 0
    for r in range(H):
        for c in range(W):
            if g[r][c] == 5 and comp_id[r][c] == -1:
                positions = []
                q = deque([(r, c)])
                comp_id[r][c] = cid
                positions.append((r, c))
                while q:
                    cr, cc = q.popleft()
                    for dr, dc in dirs:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < H and 0 <= nc < W and g[nr][nc] == 5 and comp_id[nr][nc] == -1:
                            comp_id[nr][nc] = cid
                            positions.append((nr, nc))
                            q.append((nr, nc))
                comp_positions.append(positions)
                cid += 1
    num_comps = cid
    hole_counts = [0] * num_comps
    hole_pixels = [set() for _ in range(num_comps)]
    # Exterior flood for 0's
    bg_visited = [[False] * W for _ in range(H)]
    q = deque()
    for r in range(H):
        for c in (0, W - 1):
            if g[r][c] == 0 and not bg_visited[r][c]:
                q.append((r, c))
                bg_visited[r][c] = True
    for c in range(W):
        for r in (0, H - 1):
            if g[r][c] == 0 and not bg_visited[r][c]:
                q.append((r, c))
                bg_visited[r][c] = True
    while q:
        cr, cc = q.popleft()
        for dr, dc in dirs:
            nr, nc = cr + dr, cc + dc
            if 0 <= nr < H and 0 <= nc < W and g[nr][nc] == 0 and not bg_visited[nr][nc]:
                bg_visited[nr][nc] = True
                q.append((nr, nc))
    # Find internal 0 components
    internal_visited = [[False] * W for _ in range(H)]
    for r in range(H):
        for c in range(W):
            if g[r][c] == 0 and not bg_visited[r][c] and not internal_visited[r][c]:
                hole_pos = []
                q = deque([(r, c)])
                internal_visited[r][c] = True
                hole_pos.append((r, c))
                while q:
                    cr, cc = q.popleft()
                    for dr, dc in dirs:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < H and 0 <= nc < W and g[nr][nc] == 0 and not bg_visited[nr][nc] and not internal_visited[nr][nc]:
                            internal_visited[nr][nc] = True
                            hole_pos.append((nr, nc))
                            q.append((nr, nc))
                # Adjacent 5 comps
                adj_ids = set()
                for hr, hc in hole_pos:
                    for dr, dc in dirs:
                        nr, nc = hr + dr, hc + dc
                        if 0 <= nr < H and 0 <= nc < W and g[nr][nc] == 5:
                            adj_ids.add(comp_id[nr][nc])
                if len(adj_ids) == 1:
                    the_id = next(iter(adj_ids))
                    hole_counts[the_id] += 1
                    for pos in hole_pos:
                        hole_pixels[the_id].add(pos)
    # Build mapping from rows 1,2,3
    mapping = {}
    i = 0
    while i < W:
        if g[1][i] == 0 or g[1][i] == 5:
            i += 1
            continue
        c = g[1][i]
        start = i
        while i < W and g[1][i] == c:
            i += 1
        end = i
        l = end - start
        if l < 3:
            continue
        # Check row 3
        match = all(g[3][j] == c for j in range(start, end))
        if not match:
            continue
        # Count 0's in row 2
        num0 = sum(g[2][j] == 0 for j in range(start, end))
        mapping[num0] = c
    # Transform components
    for idx in range(num_comps):
        n = hole_counts[idx]
        if n in mapping:
            new_c = mapping[n]
            for r, c in comp_positions[idx]:
                output_grid[r][c] = new_c
            for r, c in hole_pixels[idx]:
                output_grid[r][c] = new_c
        else:
            for r, c in comp_positions[idx]:
                output_grid[r][c] = 0
    return output_grid
```