```python
from collections import Counter
from typing import List, Tuple, Dict

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_segments(row: List[int], bg: int) -> List[Tuple[int, int, List[int]]]:
    segments = []
    i = 0
    n = len(row)
    while i < n:
        if row[i] != bg:
            start = i
            seg = []
            while i < n and row[i] != bg:
                seg.append(row[i])
                i += 1
            segments.append((start, i - 1, seg))
        else:
            i += 1
    return segments

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background(g)
    structures: List[Dict] = []
    for r in range(22):
        segs = find_segments(g[r], bg)
        for start, end, seg in segs:
            left_c = seg[0]
            right_c = seg[-1]
            if left_c == right_c != bg and len(seg) >= 3:
                # check if new structure (no covering segment in prev row)
                is_new = True
                if r > 0:
                    prev_segs = find_segments(g[r - 1], bg)
                    for ps, pe, _ in prev_segs:
                        if ps <= start and pe >= end:
                            is_new = False
                            break
                if is_new:
                    border_c = left_c
                    struct_rows: List[Tuple[int, List[int]]] = [(r, seg[:])]
                    curr_r = r + 1
                    while curr_r < 22:
                        next_segs = find_segments(g[curr_r], bg)
                        found = None
                        for ns, ne, nseg in next_segs:
                            if ns == start and ne == end and nseg[0] == border_c and nseg[-1] == border_c:
                                found = nseg[:]
                                break
                        if found is None:
                            break
                        struct_rows.append((curr_r, found))
                        curr_r += 1
                    has_top_full = all(x == border_c for x in struct_rows[0][1])
                    structures.append({
                        'border': border_c,
                        'col_start': start,
                        'width': len(seg),
                        'rows': struct_rows,
                        'has_top_full': has_top_full
                    })
    # sort structures by min_row, then col_start
    structures.sort(key=lambda s: (s['rows'][0][0], s['col_start']))
    # separate
    border5 = [s for s in structures if s['border'] == 5]
    border4 = [s for s in structures if s['border'] == 4]
    # assign out_col
    for i, s in enumerate(border5):
        s['out_col'] = 0 if i % 2 == 0 else 5
    for i, s in enumerate(border4):
        s['out_col'] = 17 if i % 2 == 0 else 12
    # now build out
    out: List[List[int]] = [[bg] * 22 for _ in range(22)]
    all_structs = border5 + border4  # but already have in structures, but to place all
    for s in structures:
        out_col = s['out_col']
        width = s['width']
        struct_rows = s['rows']
        num_rows = len(struct_rows)
        # find bottom full group start idx
        bottom_start_idx = num_rows - 1
        while bottom_start_idx >= 0 and all(x == s['border'] for x in struct_rows[bottom_start_idx][1]):
            bottom_start_idx -= 1
        bottom_start_idx += 1
        include_bottom = False
        if bottom_start_idx < num_rows:
            include_bottom = (s['border'] == 5 and not s['has_top_full']) or (s['border'] == 4 and s['has_top_full'])
        # place
        for idx in range(num_rows):
            rr, seg = struct_rows[idx]
            is_full_row = all(x == s['border'] for x in seg)
            place_it = True
            if is_full_row and idx >= bottom_start_idx:
                if idx == bottom_start_idx and include_bottom:
                    place_it = True
                else:
                    place_it = False
            if place_it:
                for k in range(width):
                    out[rr][out_col + k] = seg[k]
    return out
```