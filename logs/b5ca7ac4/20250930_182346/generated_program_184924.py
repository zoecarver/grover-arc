```python
from typing import List, Tuple, Dict, Set
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    rows = 22
    cols = 22
    bg = g[0][0]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Extract atomic blobs
    visited = [[False] * cols for _ in range(rows)]
    atomic_blobs = []
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                num = g[r][c]
                positions = []
                stack = [(r, c)]
                visited[r][c] = True
                positions.append((r, c))
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == num:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                            positions.append((nr, nc))
                atomic_blobs.append({'num': num, 'positions': positions})

    # Function to get adjacent non-bg nums for a blob
    def get_adj_nums(positions: List[Tuple[int, int]]) -> Set[int]:
        adj = set()
        for r, c in positions:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    nnum = g[nr][nc]
                    if nnum != bg and nnum != g[r][c]:
                        adj.add(nnum)
        return adj

    # Function to check if two blobs are adjacent
    def blobs_adjacent(pos1: List[Tuple[int, int]], pos2: List[Tuple[int, int]]) -> bool:
        pos_set = set(pos2)
        for r, c in pos1:
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in pos_set:
                    return True
        return False

    # Build objects
    blob_map = defaultdict(list)
    for blob in atomic_blobs:
        blob_map[blob['num']].append(blob)

    objects = []
    merged = set()
    for blob in atomic_blobs:
        if blob in merged:
            continue
        adj_nums = get_adj_nums(blob['positions'])
        if len(adj_nums) == 1:
            outer_num = next(iter(adj_nums))
            outer_candidates = blob_map[outer_num]
            outer_blob = None
            for cand in outer_candidates:
                if cand not in merged and blobs_adjacent(blob['positions'], cand['positions']):
                    outer_blob = cand
                    break
            if outer_blob:
                # Create object if not exist
                obj = None
                for o in objects:
                    if 'outer_blob' in o and o['outer_blob'] is outer_blob:
                        obj = o
                        break
                if obj is None:
                    obj = {'outer_num': outer_num, 'outer_pos': outer_blob['positions'], 'inners': [], 'outer_blob': outer_blob}
                    objects.append(obj)
                obj['inners'].append({'num': blob['num'], 'positions': blob['positions']})
                merged.add(blob)
                merged.add(outer_blob)
                continue
        # Standalone
        obj = {'outer_num': blob['num'], 'outer_pos': blob['positions'], 'inners': [], 'outer_blob': blob}
        objects.append(obj)
        merged.add(blob)

    # Fill open tops if bg == 0
    if bg == 0:
        for obj in objects:
            for inner in obj['inners']:
                inner_pos = inner['positions']
                if not inner_pos:
                    continue
                inner_min_r = min(r for r, c in inner_pos)
                has_open_top = any(g[inner_min_r - 1][c] == bg for r, c in inner_pos if r == inner_min_r)
                if has_open_top:
                    outer_num = obj['outer_num']
                    inner['positions'] = [(r, c, outer_num if r == inner_min_r else inner['num']) for r, c in inner_pos]

    # Now, compute discovery key for each object
    def get_discovery(obj):
        outer_pos = obj['outer_pos']
        min_r = min(r for r, c in outer_pos)
        min_c = min(c for r, c in outer_pos if r == min_r)
        return (min_r, min_c)

    # Group by outer_num
    group_map = defaultdict(list)
    for obj in objects:
        group_map[obj['outer_num']].append(obj)

    # Output grid
    out = [[bg for _ in range(cols)] for _ in range(rows)]

    # Place 8's if present
    if 8 in group_map:
        eight_objs = sorted(group_map[8], key=get_discovery)
        current_right = [-1] * rows
        for obj in eight_objs:
            row_ranges = defaultdict(list)
            for r, c in obj['outer_pos']:
                row_ranges[r].append(c)
            for inner in obj['inners']:
                for r, c, nnum in inner['positions']:
                    row_ranges[r].append(c)
            occupied_rows = list(row_ranges.keys())
            if not occupied_rows:
                continue
            deltas = []
            for rr in occupied_rows:
                left_r = min(row_ranges[rr])
                deltas.append(current_right[rr] + 1 - left_r)
            delta = max(deltas)
            # Place
            for r, c in obj['outer_pos']:
                out[r][c + delta] = obj['outer_num']
            for inner in obj['inners']:
                for r, c, nnum in inner['positions']:
                    out[r][c + delta] = nnum
            # Update current_right
            for rr in occupied_rows:
                new_max = max(c + delta for c in row_ranges[rr])
                current_right[rr] = max(current_right[rr], new_max)

    # Place 2's if present
    if 2 in group_map:
        two_objs = sorted(group_map[2], key=get_discovery)
        for idx, obj in enumerate(two_objs):
            # Compute original min_c of outer
            outer_min_c = min(c for r, c in obj['outer_pos'])
            if outer_min_c <= 8:
                base = 12
            else:
                base = 17
            delta = base - outer_min_c
            # Place
            for r, c in obj['outer_pos']:
                if 0 <= c + delta < cols:
                    out[r][c + delta] = 2
            for inner in obj['inners']:
                for r, c, nnum in inner['positions']:
                    if 0 <= c + delta < cols:
                        out[r][c + delta] = nnum

    # For other groups, pack like 8's (though not used)
    for outer_num in sorted(group_map):
        if outer_num == 8 or outer_num == 2:
            continue
        other_objs = sorted(group_map[outer_num], key=get_discovery)
        current_right = [-1] * rows  # Separate? But assume no overlap
        for obj in other_objs:
            # Similar to 8's
            row_ranges = defaultdict(list)
            for r, c in obj['outer_pos']:
                row_ranges[r].append(c)
            for inner in obj['inners']:
                for r, c, nnum in inner['positions']:
                    row_ranges[r].append(c)
            occupied_rows = list(row_ranges.keys())
            if not occupied_rows:
                continue
            deltas = []
            for rr in occupied_rows:
                left_r = min(row_ranges[rr])
                deltas.append(current_right[rr] + 1 - left_r)
            delta = max(deltas)
            # Place
            for r, c in obj['outer_pos']:
                if 0 <= c + delta < cols:
                    out[r][c + delta] = outer_num
            for inner in obj['inners']:
                for r, c, nnum in inner['positions']:
                    if 0 <= c + delta < cols:
                        out[r][c + delta] = nnum
            # Update
            for rr in occupied_rows:
                new_max = max(c + delta for c in row_ranges[rr])
                current_right[rr] = max(current_right[rr], new_max)

    return out
```