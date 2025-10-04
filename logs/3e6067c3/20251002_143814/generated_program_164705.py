```python
from typing import List, Dict, Any
from collections import Counter, defaultdict

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    """Copy the input grid."""
    return [row[:] for row in g]

def find_background_color(g: List[List[int]]) -> int:
    """Find the background color as the most frequent color in the grid."""
    flat = [cell for row in g for cell in row]
    cnt = Counter(flat)
    return cnt.most_common(1)[0][0]

def find_blocks(g: List[List[int]], bg: int) -> List[Dict[str, int]]:
    """Find blocks of consecutive non-background rows."""
    h = len(g)
    w = len(g[0])
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
    """Detect the frame color in a block as the common non-background color in uniform rows."""
    y_start = block['y_start']
    y_end = block['y_end']
    frame_cands = set()
    for y in range(y_start, y_end + 1):
        colors_in_row = {c for c in g[y] if c != bg}
        if len(colors_in_row) == 1:
            frame_cands.add(next(iter(colors_in_row)))
    if len(frame_cands) == 1:
        return next(iter(frame_cands))
    # Fallback to most frequent non-bg in block
    cnt = Counter()
    for y in range(y_start, y_end + 1):
        for c in g[y]:
            if c != bg:
                cnt[c] += 1
    return cnt.most_common(1)[0][0] if cnt else bg

def find_all_inners(g: List[List[int]], blocks: List[Dict[str, int]], bg: int) -> List[Dict[str, Any]]:
    """Find all inner regions within blocks."""
    h = len(g)
    w = len(g[0])
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
        # Group and merge consecutive y for same x and color
        groups = defaultdict(list)
        for ti in temp_inners:
            key = (ti['x_start'], ti['x_end'], ti['color'])
            groups[key].append(ti['temp_y'])
        for key, ys in groups.items():
            ys.sort()
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
    """Find the bottom key row with multiple isolated non-background cells."""
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
    """Extract colors from key row in left-to-right order."""
    row = g[key_row]
    w = len(row)
    seq = []
    j = 0
    while j < w:
        if row[j] != bg:
            seq.append(row[j])
            j += 1  # assume singles, skip one
        else:
            j += 1
    return seq

def assign_inners_to_sequence(inners: List[Dict[str, Any]], seq_colors: List[int]) -> List[Dict[str, Any]]:
    """Assign inners to sequence colors, leftmost unused for duplicates."""
    available = sorted(inners, key=lambda inn: inn['x_start'])
    used_ids = set()
    assigned = []
    for c in seq_colors:
        cands = [inn for inn in available if inn['color'] == c and id(inn) not in used_ids]
        if cands:
            cand = min(cands, key=lambda inn: inn['x_start'])
            assigned.append(cand)
            used_ids.add(id(cand))
    return assigned

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to solve the puzzle by connecting inners in sequence order."""
    out = copy_grid(g)
    bg = find_background_color(g)
    h = len(g)
    w = len(g[0])
    blocks = find_blocks(g, bg)
    blocks.sort(key=lambda b: b['y_start'])
    all_inners = find_all_inners(g, blocks, bg)
    key_row = find_key_row(g, bg, h)
    seq_colors = get_color_sequence(g, bg, key_row)
    inner_seq = assign_inners_to_sequence(all_inners, seq_colors)
    if len(inner_seq) < 2:
        return out
    # Plan connections
    horizontal_plans = []
    vertical_plans = []
    for i in range(len(inner_seq) - 1):
        curr = inner_seq[i]
        nxt = inner_seq[i + 1]
        color = curr['color']
        if curr['block'] is nxt['block']:
            # Horizontal plan
            y_s = curr['y_start']
            y_e = curr['y_end']
            left = curr if curr['x_start'] < nxt['x_start'] else nxt
            right = nxt if curr['x_start'] < nxt['x_start'] else curr
            gap_s = left['x_end'] + 1
            gap_e = right['x_start'] - 1
            if gap_s <= gap_e:
                horizontal_plans.append({'y_start': y_s, 'y_end': y_e, 'x_start': gap_s, 'x_end': gap_e, 'color': color})
        else:
            # Vertical plan
            b1 = curr['block']
            b2 = nxt['block']
            if b1['y_end'] < b2['y_start']:
                fy_s = b1['y_end'] + 1
                fy_e = b2['y_start'] - 1
            else:
                fy_s = b2['y_end'] + 1
                fy_e = b1['y_start'] - 1
            x_s = max(curr['x_start'], nxt['x_start'])
            x_e = min(curr['x_end'], nxt['x_end'])
            if fy_s <= fy_e and x_s <= x_e:
                vertical_plans.append({'y_start': fy_s, 'y_end': fy_e, 'x_start': x_s, 'x_end': x_e, 'color': color})
    # Fill horizontal immediately
    for plan in horizontal_plans:
        for y in range(plan['y_start'], plan['y_end'] + 1):
            for x in range(plan['x_start'], plan['x_end'] + 1):
                if out[y][x] == bg:
                    out[y][x] = plan['color']
    # Plan spaces for vertical
    spaces = []
    for kid in range(len(blocks) - 1):
        u_end = blocks[kid]['y_end']
        l_start = blocks[kid + 1]['y_start']
        s_start = u_end + 1
        s_end = l_start - 1
        if s_start <= s_end:
            conns = [p for p in vertical_plans if p['y_start'] == s_start and p['y_end'] == s_end]
            spaces.append({'id': kid, 'y_start': s_start, 'y_end': s_end, 'h': s_end - s_start + 1, 'conns': conns})
    # Process spaces bottom to top for shifts
    for sp in reversed(spaces):
        h = sp['h']
        conns = sp['conns']
        if h == 2 and len(conns) > 1:
            kid = sp['id']
            lower_start = blocks[kid + 1]['y_start']
            # Shift up
            for r in range(h - 1, lower_start - 1, -1):
                out[r - 1] = out[r][:]
            out[h - 1] = [bg] * w
            # Update lower blocks
            for b_id in range(kid + 1, len(blocks)):
                blocks[b_id]['y_start'] -= 1
                blocks[b_id]['y_end'] -= 1
            # Update key_row (not used further)
            global key_row
            if key_row >= lower_start:
                key_row -= 1
            # Update lower vertical plans
            for p in vertical_plans:
                if p['y_start'] > sp['y_end']:
                    p['y_start'] -= 1
                    p['y_end'] -= 1
            # Fill the single row for these conns
            fill_r = sp['y_start']
            for p in conns:
                c = p['color']
                xs = p['x_start']
                xe = p['x_end']
                for x in range(xs, xe + 1):
                    if out[fill_r][x] == bg:
                        out[fill_r][x] = c
            # Remove filled conns
            vertical_plans = [p for p in vertical_plans if p not in conns]
    # Fill remaining vertical plans
    for p in vertical_plans:
        for y in range(p['y_start'], p['y_end'] + 1):
            for x in range(p['x_start'], p['x_end'] + 1):
                if out[y][x] == bg:
                    out[y][x] = p['color']
    return out
```