```python
from typing import List, Tuple, Dict, Any
from collections import Counter, defaultdict
from copy import deepcopy

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def find_background_color(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 8
    return g[0][0]

def find_blocks(g: List[List[int]], bg: int) -> List[Dict[str, int]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    blocks = []
    i = 0
    while i < h:
        while i < h and all(c == bg for c in g[i]):
            i += 1
        if i == h:
            break
        start = i
        while i < h and not all(c == bg for c in g[i]):
            i += 1
        end = i - 1
        if end - start + 1 >= 2:
            blocks.append({'y_start': start, 'y_end': end})
    return blocks

def detect_frame_color(g: List[List[int]], block: Dict[str, int], bg: int) -> int:
    y_start = block['y_start']
    y_end = block['y_end']
    frame_cands = set()
    for y in range(y_start, y_end + 1):
        colors_in_row = {c for c in g[y] if c != bg}
        if len(colors_in_row) == 1:
            frame_cands.add(next(iter(colors_in_row)))
    if len(frame_cands) == 1:
        return next(iter(frame_cands))
    cnt = Counter()
    for y in range(y_start, y_end + 1):
        for c in g[y]:
            if c != bg:
                cnt[c] += 1
    return cnt.most_common(1)[0][0] if cnt else bg

def find_all_inners(g: List[List[int]], blocks: List[Dict[str, int]], bg: int) -> List[Dict[str, Any]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    all_inners = []
    for block in blocks:
        frame = detect_frame_color(g, block, bg)
        y_start_b = block['y_start']
        y_end_b = block['y_end']
        temp_inners = []
        for y in range(y_start_b, y_end_b + 1):
            j = 0
            while j < w:
                if g[y][j] != bg and g[y][j] != frame:
                    c = g[y][j]
                    start_x = j
                    while j < w and g[y][j] == c:
                        j += 1
                    end_x = j - 1
                    temp_inners.append({'temp_y': y, 'x_start': start_x, 'x_end': end_x, 'color': c})
                else:
                    j += 1
        groups = defaultdict(list)
        for ti in temp_inners:
            key = (ti['x_start'], ti['x_end'], ti['color'])
            groups[key].append(ti['temp_y'])
        for key, ys in groups.items():
            ys.sort()
            if not ys:
                continue
            curr_s = ys[0]
            curr_e = ys[0]
            for k in range(1, len(ys)):
                if ys[k] == curr_e + 1:
                    curr_e = ys[k]
                else:
                    if curr_e - curr_s + 1 >= 1:
                        all_inners.append({
                            'block': block,
                            'color': key[2],
                            'x_start': key[0],
                            'x_end': key[1],
                            'y_start': curr_s,
                            'y_end': curr_e
                        })
                    curr_s = ys[k]
                    curr_e = ys[k]
            if curr_e - curr_s + 1 >= 1:
                all_inners.append({
                    'block': block,
                    'color': key[2],
                    'x_start': key[0],
                    'x_end': key[1],
                    'y_start': curr_s,
                    'y_end': curr_e
                })
    return all_inners

def find_key_row(g: List[List[int]], bg: int, h: int) -> int:
    for r in range(h - 1, -1, -1):
        row = g[r]
        w = len(row)
        runs = 0
        non_bg_count = 0
        in_run = False
        j = 0
        while j < w:
            if row[j] != bg:
                non_bg_count += 1
                if not in_run:
                    runs += 1
                    in_run = True
                j += 1
            else:
                in_run = False
                j += 1
        if 3 <= runs <= 12 and non_bg_count <= 15:
            return r
    return h - 2  # fallback

def get_color_sequence(g: List[List[int]], bg: int, key_row: int) -> List[int]:
    row = g[key_row]
    w = len(row)
    seq = []
    j = 0
    while j < w:
        if row[j] != bg:
            seq.append(row[j])
            j += 1
        else:
            j += 1
    return seq

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    g_out = deepcopy(g)
    bg = find_background_color(g)
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    blocks = find_blocks(g, bg)
    all_inners = find_all_inners(g, blocks, bg)
    key_row = find_key_row(g, bg, h)
    seq_colors = get_color_sequence(g, bg, key_row)
    available = sorted(all_inners, key=lambda inn: (inn['y_start'], inn['x_start']))
    used_ids = set()
    assigned = []
    for c in seq_colors:
        cands = [inn for inn in available if inn['color'] == c and id(inn) not in used_ids]
        if cands:
            cand_key = lambda inn: (inn['y_start'], inn['x_start'])
            cand = min(cands, key=cand_key)
            assigned.append(cand)
            used_ids.add(id(cand))
    for ii in range(len(assigned) - 1):
        inn1 = assigned[ii]
        inn2 = assigned[ii + 1]
        y1s = inn1['y_start']
        y1e = inn1['y_end']
        x1s = inn1['x_start']
        x1e = inn1['x_end']
        y2s = inn2['y_start']
        y2e = inn2['y_end']
        x2s = inn2['x_start']
        x2e = inn2['x_end']
        c_fill = inn1['color']
        # horizontal connection
        olap_rs = max(y1s, y2s)
        olap_re = min(y1e, y2e)
        if olap_rs <= olap_re:
            if x1e < x2s:
                gcs = x1e + 1
                gce = x2s - 1
                if gcs <= gce:
                    for r in range(olap_rs, olap_re + 1):
                        for cc in range(gcs, gce + 1):
                            if 0 <= cc < w and 0 <= r < h and g_out[r][cc] == bg:
                                g_out[r][cc] = c_fill
            elif x2e < x1s:
                gcs = x2e + 1
                gce = x1s - 1
                if gcs <= gce:
                    for r in range(olap_rs, olap_re + 1):
                        for cc in range(gcs, gce + 1):
                            if 0 <= cc < w and 0 <= r < h and g_out[r][cc] == bg:
                                g_out[r][cc] = c_fill
        # vertical connection
        olap_cs = max(x1s, x2s)
        olap_ce = min(x1e, x2e)
        if olap_cs <= olap_ce:
            if y1e < y2s:
                grs = y1e + 1
                gre = y2s - 1
                if grs <= gre:
                    empty_rows = [rr for rr in range(grs, gre + 1) if all(0 <= cc < w and g_out[rr][cc] == bg for cc in range(olap_cs, olap_ce + 1))]
                    num = len(empty_rows)
                    if num > 0:
                        fill_rs = empty_rows if num > 2 else [empty_rows[-1]]
                        for rr in fill_rs:
                            for cc in range(olap_cs, olap_ce + 1):
                                if 0 <= rr < h and 0 <= cc < w and g_out[rr][cc] == bg:
                                    g_out[rr][cc] = c_fill
            elif y2e < y1s:
                grs = y2e + 1
                gre = y1s - 1
                if grs <= gre:
                    empty_rows = [rr for rr in range(grs, gre + 1) if all(0 <= cc < w and g_out[rr][cc] == bg for cc in range(olap_cs, olap_ce + 1))]
                    num = len(empty_rows)
                    if num > 0:
                        fill_rs = empty_rows if num > 2 else [empty_rows[-1]]
                        for rr in fill_rs:
                            for cc in range(olap_cs, olap_ce + 1):
                                if 0 <= rr < h and 0 <= cc < w and g_out[rr][cc] == bg:
                                    g_out[rr][cc] = c_fill
    return g_out
```