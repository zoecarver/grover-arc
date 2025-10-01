```python
def program(g):
    rows = 22
    cols = 22
    bg_num = g[0][0]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def extract_atomic_blobs(g, bg_num):
        visited = [[False] * cols for _ in range(rows)]
        blobs = []
        for r in range(rows):
            for c in range(cols):
                if g[r][c] != bg_num and not visited[r][c]:
                    num = g[r][c]
                    positions = []
                    stack = [(r, c)]
                    visited[r][c] = True
                    positions.append((r, c))
                    while stack:
                        cr, cc = stack.pop()
                        for dr, dc in directions:
                            nr = cr + dr
                            nc = cc + dc
                            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == num:
                                visited[nr][nc] = True
                                stack.append((nr, nc))
                                positions.append((nr, nc))
                    blobs.append({'num': num, 'positions': positions, 'discovery': (r, c)})
        return blobs

    def is_touching_bg(g, blob, bg_num, directions):
        for r, c in blob['positions']:
            for dr, dc in directions:
                nr = r + dr
                nc = c + dc
                if not (0 <= nr < rows and 0 <= nc < cols) or g[nr][nc] == bg_num:
                    return True
        return False

    def get_adjacent_outer_pos(g, blob, bg_num, outer_num, directions):
        adj_pos = set()
        for r, c in blob['positions']:
            for dr, dc in directions:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == outer_num:
                    adj_pos.add((nr, nc))
        return adj_pos

    blobs = extract_atomic_blobs(g, bg_num)
    objects = []
    used = set()
    for i in range(len(blobs)):
        if i in used:
            continue
        blob = blobs[i]
        if is_touching_bg(g, blob, bg_num, directions):
            values = [(rr, cc, g[rr][cc]) for rr, cc in blob['positions']]
            objects.append({'positions': blob['positions'], 'values': values, 'discovery': blob['discovery']})
            used.add(i)
            continue
        adj_nums = set()
        for rr, cc in blob['positions']:
            for dr, dc in directions:
                nr = rr + dr
                nc = cc + dc
                if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] != bg_num and g[nr][nc] != blob['num']:
                    adj_nums.add(g[nr][nc])
        if len(adj_nums) == 1:
            outer_num = next(iter(adj_nums))
            adj_pos = get_adjacent_outer_pos(g, blob, bg_num, outer_num, directions)
            found_outer = None
            for j in range(len(blobs)):
                if j in used:
                    continue
                o_blob = blobs[j]
                if o_blob['num'] == outer_num and all(p in set(o_blob['positions']) for p in adj_pos):
                    found_outer = j
                    break
            if found_outer is not None:
                outer_pos = blobs[found_outer]['positions']
                inner_pos = blob['positions']
                all_pos = outer_pos + inner_pos
                all_values = [(rr, cc, g[rr][cc]) for rr, cc in all_pos]
                objects.append({'positions': all_pos, 'values': all_values, 'discovery': blobs[found_outer]['discovery']})
                used.add(i)
                used.add(found_outer)
                continue
        values = [(rr, cc, g[rr][cc]) for rr, cc in blob['positions']]
        objects.append({'positions': blob['positions'], 'values': values, 'discovery': blob['discovery']})
        used.add(i)

    def discovery_key(obj):
        dr, dc = obj['discovery']
        return (dr, dc)

    objects.sort(key=discovery_key)

    out = [[bg_num] * cols for _ in range(rows)]
    for obj in objects:
        if not obj['positions']:
            continue
        min_r = min(r for r, _ in obj['positions'])
        min_c = min(c for _, c in obj['positions'])
        placed = False
        for top_r in range(rows):
            if placed:
                break
            for left_c in range(cols):
                dr = top_r - min_r
                dc = left_c - min_c
                valid = True
                for r, c in obj['positions']:
                    nr = r + dr
                    nc = c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols) or out[nr][nc] != bg_num:
                        valid = False
                        break
                if valid:
                    for idx in range(len(obj['values'])):
                        rr, cc, val = obj['values'][idx]
                        nr = rr + dr
                        nc = cc + dc
                        out[nr][nc] = val
                    placed = True
                    break
    return out
```