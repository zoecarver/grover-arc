```python
def get_background(g):
    return g[0][0]

def get_instruction_rows(g, bg, n):
    left_cols = [1, 3, 5]
    instruction_rows = []
    for r in range(1, n, 2):
        has_non_bg = False
        for c in left_cols:
            if c < n and g[r][c] != bg:
                has_non_bg = True
                break
        if has_non_bg:
            instruction_rows.append(r)
    return instruction_rows

def get_sequence(g, bg, instruction_rows, left_cols, k):
    sequence = [[] for _ in left_cols]
    for i in range(k):
        r = instruction_rows[i]
        for j in range(len(left_cols)):
            c = left_cols[j]
            color = g[r][c] if c < len(g[0]) else bg
            sequence[j].append(color)
    return sequence

def get_existing_slot(g, bg, n):
    min_r = n
    max_r = -1
    for r in range(n):
        has_non_bg = False
        for c in range(7, n):
            if g[r][c] != bg:
                has_non_bg = True
                break
        if has_non_bg:
            min_r = min(min_r, r)
            max_r = max(max_r, r)
    if max_r < 0:
        h = 0
        start_s = n
    else:
        h = max_r - min_r + 1
        start_s = min_r
    groups = []
    if h > 0:
        row = g[start_s]
        i = 7
        while i < n:
            if row[i] != bg:
                color = row[i]
                start_c = i
                while i < n and row[i] == color:
                    i += 1
                width = i - start_c
                groups.append((color, start_c, width))
            else:
                i += 1
    m = len(groups)
    first_start = groups[0][1] if m > 0 else 7
    w = groups[0][2] if m > 0 else 0
    s_gap = groups[1][1] - groups[0][1] - groups[0][2] if m > 1 else 1
    return start_s, h, first_start, w, s_gap, groups, m

def find_stage(sequence, groups, m):
    k = len(sequence[0])
    if m == 0:
        return 1, 2
    first_color = groups[0][0]
    second_color = groups[1][0] if m > 1 else None
    for i in range(k):
        if sequence[0][i] == first_color:
            if m <= 1:
                return i + 1, 2
            if sequence[1][i] == second_color:
                return i + 1, 2
            if sequence[2][i] == second_color:
                return i + 1, 3
    return 1, 2

def place_group(g_out, start_r, h, start_c, width, color, bg, n):
    for rr in range(start_r, min(start_r + h, n)):
        for cc in range(start_c, min(start_c + width, n)):
            if g_out[rr][cc] == bg:
                g_out[rr][cc] = color

def program(g):
    n = len(g)
    g_out = [row[:] for row in g]
    bg = get_background(g)
    instr_rows = get_instruction_rows(g, bg, n)
    k = len(instr_rows)
    if k == 0:
        return g_out
    left_cols = [1, 3, 5]
    seq = get_sequence(g, bg, instr_rows, left_cols, k)
    start_s, h, first_start, w, s_gap, groups, m = get_existing_slot(g, bg, n)
    if h == 0 or m == 0:
        return g_out
    step = h + s_gap
    stage, second_channel = find_stage(seq, groups, m)
    skipped_i = stage - 1
    for i in range(k):
        if i == skipped_i:
            continue
        start_r = start_s + (i - skipped_i) * step
        if start_r < 0 or start_r + h > n:
            continue
        ch0 = seq[0][i]
        if second_channel == 2:
            ch_sec = seq[1][i]
            ch_ter = seq[2][i]
        else:
            ch_sec = seq[2][i]
            ch_ter = seq[1][i]
        c_pos = first_start
        if ch0 != bg:
            place_group(g_out, start_r, h, c_pos, w, ch0, bg, n)
            c_pos += w + s_gap
        if ch_sec != bg:
            place_group(g_out, start_r, h, c_pos, w, ch_sec, bg, n)
            c_pos += w + s_gap
        if ch_ter != bg:
            place_group(g_out, start_r, h, c_pos, w, ch_ter, bg, n)
    return g_out
```