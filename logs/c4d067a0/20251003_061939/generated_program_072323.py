```python
import typing as tp

def is_subsequence(a: tp.List[int], b: tp.List[int]) -> bool:
    if not a:
        return True
    i = 0
    for val in b:
        if i < len(a) and val == a[i]:
            i += 1
            if i == len(a):
                return True
    return False

def place(out: tp.List[tp.List[int]], start_r: int, h: int, c_list: tp.List[int], block_ranges: tp.List[tp.Tuple[int, int]], size: int):
    if start_r < 0 or start_r + h > size:
        return
    num = min(len(c_list), len(block_ranges))
    for bb in range(num):
        cs, ce = block_ranges[bb]
        c = c_list[bb]
        for r in range(start_r, start_r + h):
            for cc in range(cs, ce + 1):
                out[r][cc] = c

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    size = len(g)
    # Get background
    bg = g[0][0]
    for row in g:
        if len(set(row)) == 1:
            bg = row[0]
            break
    # Get tracks: odd columns with isolated single non-bg
    tracks = []
    for j in range(1, size, 2):
        has_signal = False
        max_consec = 0
        consec = 0
        for i in range(size):
            if g[i][j] != bg:
                has_signal = True
                consec += 1
                max_consec = max(max_consec, consec)
            else:
                consec = 0
        if has_signal and max_consec == 1:
            tracks.append(j)
    # Get signal_rows
    signal_set = set()
    for i in range(size):
        for j in tracks:
            if g[i][j] != bg:
                signal_set.add(i)
                break
    signal_rows = sorted(list(signal_set))
    n = len(signal_rows)
    if n == 0:
        return [row[:] for row in g]
    # Get block_ranges
    ranges_set = set()
    for i in range(size):
        j = 0
        while j < size:
            if g[i][j] == bg:
                j += 1
                continue
            start = j
            c = g[i][j]
            while j < size and g[i][j] == c:
                j += 1
            end = j - 1
            if end - start + 1 >= 2:
                ranges_set.add((start, end))
    block_ranges = sorted(list(ranges_set))
    m = len(block_ranges)
    if m == 0:
        return [row[:] for row in g]
    h = block_ranges[0][1] - block_ranges[0][0] + 1
    # Find s_filled and k_filled
    s_filled = -1
    k_filled = -1
    for s in range(size - h + 1):
        block_colors_cand = []
        valid = True
        for b in range(m):
            cs, ce = block_ranges[b]
            c = g[s][cs]
            if c == bg:
                valid = False
                break
            same = True
            for rr in range(s, s + h):
                for cc in range(cs, ce + 1):
                    if g[rr][cc] != c:
                        same = False
                        break
                if not same:
                    break
            if not same:
                valid = False
                break
            block_colors_cand.append(c)
        if valid:
            for kk in range(n):
                c_list_k = [g[signal_rows[kk]][j] for j in tracks if g[signal_rows[kk]][j] != bg]
                if is_subsequence(block_colors_cand, c_list_k):
                    s_filled = s
                    k_filled = kk
                    break
            if s_filled != -1:
                break
    if s_filled == -1:
        return [row[:] for row in g]
    # Extend block_ranges
    max_needed = 0
    for kk in range(n):
        c_list_k = [g[signal_rows[kk]][j] for j in tracks if g[signal_rows[kk]][j] != bg]
        max_needed = max(max_needed, len(c_list_k))
    while len(block_ranges) < max_needed:
        last_end = block_ranges[-1][1]
        new_start = last_end + 1 + (h - 1)
        new_end = new_start + h - 1
        if new_end >= size:
            break
        block_ranges.append((new_start, new_end))
    # Output grid
    out = [row[:] for row in g]
    d = 2 * h - 1
    # Forward
    for i in range(1, n - k_filled):
        kk = k_filled + i
        start_r = s_filled + i * d
        if start_r + h > size:
            continue
        c_list = [g[signal_rows[kk]][j] for j in tracks if g[signal_rows[kk]][j] != bg]
        place(out, start_r, h, c_list, block_ranges, size)
    # Backward
    if k_filled > 0:
        max_s = signal_rows[-1]
        use_special = (max_s < s_filled)
        if use_special:
            p = k_filled
            d_internal = 2 * h
            temp = s_filled + max_s + 1 - h - (p - 1) * d_internal
            start0 = temp // 2
            last_start = start0 + (p - 1) * d_internal
            last_end = last_start + h - 1 if p > 0 else -1
            if start0 >= 0 and last_end < s_filled:
                current = start0
                for i in range(p):
                    kk = i
                    start_r = current
                    if start_r + h > size:
                        break
                    c_list = [g[signal_rows[kk]][j] for j in tracks if g[signal_rows[kk]][j] != bg]
                    place(out, start_r, h, c_list, block_ranges, size)
                    current += d_internal
            else:
                d_back = 2 * h + 1
                for i in range(1, k_filled + 1):
                    start_r = s_filled - i * d_back
                    if start_r < 0:
                        continue
                    kk = k_filled - i
                    c_list = [g[signal_rows[kk]][j] for j in tracks if g[signal_rows[kk]][j] != bg]
                    place(out, start_r, h, c_list, block_ranges, size)
        else:
            d_back = 2 * h + 1
            for i in range(1, k_filled + 1):
                start_r = s_filled - i * d_back
                if start_r < 0:
                    continue
                kk = k_filled - i
                c_list = [g[signal_rows[kk]][j] for j in tracks if g[signal_rows[kk]][j] != bg]
                place(out, start_r, h, c_list, block_ranges, size)
    return out
```