```python
import collections

def find_components(g):
    h = len(g)
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != 1 and not visited[i][j]:
                color = g[i][j]
                pos = []
                queue = collections.deque([(i, j)])
                visited[i][j] = True
                pos.append((i, j))
                while queue:
                    x, y = queue.popleft()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            queue.append((nx, ny))
                            pos.append((nx, ny))
                components.append((color, pos))
    return components

def get_normalized_rel(pos):
    if not pos:
        return set()
    minr = min(r for r, c in pos)
    minc = min(c for r, c in pos)
    return {(r - minr, c - minc) for r, c in pos}

def get_missing_rel(pos):
    if not pos:
        return set()
    minr = min(r for r, c in pos)
    maxr = max(r for r, c in pos)
    minc = min(c for r, c in pos)
    maxc = max(c for r, c in pos)
    pos_set = set(pos)
    missing = set()
    for r in range(minr, maxr + 1):
        for c in range(minc, maxc + 1):
            if (r, c) not in pos_set:
                missing.add((r, c))
    if not missing:
        return set()
    minr_m = min(r for r, c in missing)
    minc_m = min(c for r, c in missing)
    return {(r - minr_m, c - minc_m) for r, c in missing}

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    w = len(g[0])
    components = find_components(g)
    
    # Check for filling pair
    host_idx = -1
    filler_idx = -1
    for i in range(len(components)):
        col_a, pos_a = components[i]
        missing_rel_a = get_missing_rel(pos_a)
        if len(missing_rel_a) == 0:
            continue
        for j in range(len(components)):
            if i == j:
                continue
            col_b, pos_b = components[j]
            b_rel = get_normalized_rel(pos_b)
            if len(pos_b) == len(missing_rel_a) and b_rel == missing_rel_a:
                host_idx = i
                filler_idx = j
                break
        if host_idx != -1:
            break
    
    out = [[1] * w for _ in range(h)]
    
    if host_idx != -1:
        # Filling case
        host_col, host_pos = components[host_idx]
        filler_col, filler_pos = components[filler_idx]
        
        # Get missing absolute min for translation
        minr_a = min(r for r, c in host_pos)
        maxr_a = max(r for r, c in host_pos)
        minc_a = min(c for r, c in host_pos)
        maxc_a = max(c for r, c in host_pos)
        missing_abs = set()
        host_set = set(host_pos)
        for r in range(minr_a, maxr_a + 1):
            for c in range(minc_a, maxc_a + 1):
                if (r, c) not in host_set:
                    missing_abs.add((r, c))
        minr_m = min(r for r, c in missing_abs)
        minc_m = min(c for r, c in missing_abs)
        
        # Translation for filler
        minr_b = min(r for r, c in filler_pos)
        minc_b = min(c for r, c in filler_pos)
        dr = minr_m - minr_b
        dc = minc_m - minc_b
        
        # Place host
        for r, c in host_pos:
            out[r][c] = host_col
        
        # Place translated filler
        for r, c in filler_pos:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < h and 0 <= nc < w:
                out[nr][nc] = filler_col
        
        # Place other components translated by same dr, dc
        for k in range(len(components)):
            if k == host_idx or k == filler_idx:
                continue
            col_k, pos_k = components[k]
            for r, c in pos_k:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    out[nr][nc] = col_k
    else:
        # Default: stack from middle, left aligned
        # Compute total height
        total_height = 0
        for col, pos in components:
            if pos:
                minr = min(r for r, c in pos)
                maxr = max(r for r, c in pos)
                total_height += maxr - minr + 1
        start_row = max(0, (h - total_height) // 2)
        
        # Sort components by color asc, then by minr asc
        sorted_comps = sorted(components, key=lambda comp: (comp[0], min(r for r, c in comp[1]) if comp[1] else 0))
        
        current_row = start_row
        for col, pos in sorted_comps:
            if not pos:
                continue
            minr = min(r for r, c in pos)
            maxr = max(r for r, c in pos)
            height = maxr - minr + 1
            dr = current_row - minr
            minc = min(c for r, c in pos)
            dc = 0 - minc
            for r, c in pos:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < h and 0 <= nc < w:
                    out[nr][nc] = col
            current_row += height
    
    return out
```