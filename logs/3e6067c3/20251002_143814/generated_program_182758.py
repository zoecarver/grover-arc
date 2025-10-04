```python
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
from copy import deepcopy

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    g_out = deepcopy(g)
    bg = g[0][0] if g and g[0] else 8
    blocks = find_blocks(g_out, bg)
    if not blocks:
        return g_out
    frame = detect_frame_color(g_out, blocks[0], bg)
    empty_color = bg if frame == 1 else frame
    all_inners = find_all_inners(g_out, blocks, bg)
    h = len(g_out)
    key_row = find_key_row(g_out, bg, h)
    seq = get_color_sequence(g_out, bg, key_row)
    assigned = assign_inners_to_sequence(all_inners, seq)
    for i in range(len(assigned) - 1):
        inn1 = assigned[i]
        inn2 = assigned[i + 1]
        fill_color = inn1['color']
        connect_horizontal(g_out, inn1, inn2, fill_color, empty_color)
        connect_vertical(g_out, inn1, inn2, fill_color, empty_color)
    return g_out

def find_blocks(g: List[List[int]], bg: int) -> List[Dict[str, int]]:
    h, w = len(g), len(g[0]) if g else 0
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
    y_start, y_end = block['y_start'], block['y_end']
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
    h, w = len(g), len(g[0]) if g else 0
    all_inners = []
    for block in blocks:
        frame = detect_frame_color(g, block, bg)
        y_start_b, y_end_b = block['y_start'], block['y_end']
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
            if not ys:
                continue
            ys.sort()
            curr_s, curr_e = ys[0], ys[0]
            for k in range(1, len(ys)):
                if ys[k] == curr_e + 1:
                    curr_e = ys[k]
                else:
                    if curr_e - curr_s + 1 >= 1:
                        all_inners.append({
                            'block': block, 'color': key[2], 'x_start': key[0], 'x_end': key[1],
                            'y_start': curr_s, 'y_end': curr_e
                        })
                    curr_s, curr_e = ys[k], ys[k]
            if curr_e - curr_s + 1 >= 1:
                all_inners.append({
                    'block': block, 'color': key[2], 'x_start': key[0], 'x_end': key[1],
                    'y_start': curr_s, 'y_end': curr_e
                })
    return all_inners

def find_key_row(g: List[List[int]], bg: int, h: int) -> int:
    for r in range(h - 1, -1, -1):
        row = g[r]
        w = len(row)
        runs, non_bg_count, in_run = 0, 0, False
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
    return h - 2

def get_color_sequence(g: List[List[int]], bg: int, key_row: int) -> List[int]:
    row = g[key_row]
    return [c for c in row if c != bg]

def assign_inners_to_sequence(inners: List[Dict[str, Any]], seq_colors: List[int]) -> List[Dict[str, Any]]:
    used = set()
    assigned = []
    for c in seq_colors:
        cands = [inn for inn in inners if inn['color'] == c and id(inn) not in used]
        if cands:
            cand = min(cands, key=lambda inn: (inn['y_start'], inn['x_start']))
            assigned.append(cand)
            used.add(id(cand))
    return assigned

def connect_horizontal(g: List[List[int]], inn1: Dict[str, Any], inn2: Dict[str, Any], fill_color: int, empty_color: int) -> None:
    y_os = max(inn1['y_start'], inn2['y_start'])
    y_oe = min(inn1['y_end'], inn2['y_end'])
    if y_os > y_oe:
        return
    x1s, x1e = inn1['x_start'], inn1['x_end']
    x2s, x2e = inn2['x_start'], inn2['x_end']
    if x1e < x2s:
        gsc = x1e + 1
        gec = x2s - 1
    elif x2e < x1s:
        gsc = x2e + 1
        gec = x1s - 1
    else:
        return
    if gsc > gec:
        return
    for r in range(y_os, y_oe + 1):
        for c in range(gsc, gec + 1):
            if g[r][c] == empty_color:
                g[r][c] = fill_color

def connect_vertical(g: List[List[int]], inn1: Dict[str, Any], inn2: Dict[str, Any], fill_color: int, empty_color: int) -> None:
    x_os = max(inn1['x_start'], inn2['x_start'])
    x_oe = min(inn1['x_end'], inn2['x_end'])
    if x_os > x_oe:
        return
    y1s, y1e = inn1['y_start'], inn1['y_end']
    y2s, y2e = inn2['y_start'], inn2['y_end']
    if y1e < y2s:
        gsr = y1e + 1
        ger = y2s - 1
    elif y2e < y1s:
        gsr = y2e + 1
        ger = y1s - 1
    else:
        return
    if gsr > ger:
        return
    for r in range(gsr, ger + 1):
        if all(g[r][c] == empty_color for c in range(x_os, x_oe + 1)):
            for c in range(x_os, x_oe + 1):
                g[r][c] = fill_color
```