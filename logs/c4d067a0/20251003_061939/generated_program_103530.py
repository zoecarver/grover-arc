```python
from typing import List, Tuple
from collections import Counter

def is_subsequence(sub: List[int], full: List[int]) -> bool:
    if not sub:
        return True
    i = 0
    for val in full:
        if i < len(sub) and val == sub[i]:
            i += 1
            if i == len(sub):
                return True
    return i == len(sub)

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    bg = Counter([c for row in g for c in row]).most_common(1)[0][0]

    def get_tracks(g: List[List[int]], bg: int, n: int) -> List[int]:
        tracks = []
        for c in range(1, n, 2):
            has_signal = False
            max_consec = 0
            consec = 0
            for r in range(n):
                if g[r][c] != bg:
                    has_signal = True
                    consec += 1
                    max_consec = max(max_consec, consec)
                else:
                    consec = 0
            if has_signal and max_consec == 1:
                tracks.append(c)
        return tracks

    tracks = get_tracks(g, bg, n)

    def get_valid_srows_and_colors(g: List[List[int]], tracks: List[int], bg: int, n: int, srows: List[int]) -> Tuple[List[int], List[List[int]]]:
        valid_srows = []
        colors = []
        for r in srows:
            row_colors = [g[r][c] for c in tracks if g[r][c] != bg and g[r][c] != 8]
            if row_colors:
                valid_srows.append(r)
                colors.append(row_colors)
        return valid_srows, colors

    raw_srows_set = set()
    for r in range(n):
        for c in tracks:
            if g[r][c] != bg:
                raw_srows_set.add(r)
                break
    raw_srows = sorted(raw_srows_set)
    srows, sig_colors = get_valid_srows_and_colors(g, tracks, bg, n, raw_srows)
    m = len(sig_colors)
    if m == 0:
        return [row[:] for row in g]

    def find_runs(row: List[int], bg: int, n: int) -> List[Tuple[int, int, int]]:
        runs = []
        i = 0
        while i < n:
            if row[i] == bg:
                i += 1
                continue
            start = i
            colr = row[i]
            while i < n and row[i] == colr:
                i += 1
            leng = i - start
            if leng >= 2:
                runs.append((start, leng, colr))
        return runs

    found = False
    h = 0
    s = 0
    kk = 0
    template_starts: List[int] = []
    w = 0
    horiz_diff = 0
    for ph in range(n, 1, -1):
        found_inner = False
        for sr in range(n - ph + 1):
            first_runs = find_runs(g[sr], bg, n)
            if not first_runs:
                continue
            ws = {run[1] for run in first_runs}
            if len(ws) != 1:
                continue
            this_w = next(iter(ws))
            run_struct = [(run[0], run[1]) for run in first_runs]
            consistent = True
            block_cols = []
            for j in range(len(first_runs)):
                st, le, cl = first_runs[j]
                uniform = True
                for r_off in range(ph):
                    rr = sr + r_off
                    for cc in range(st, st + le):
                        if g[rr][cc] != cl:
                            uniform = False
                            break
                    if not uniform:
                        break
                if not uniform:
                    consistent = False
                    break
                block_cols.append(cl)
            if not consistent:
                continue
            matched_kk = -1
            for kkk in range(m):
                if is_subsequence(block_cols, sig_colors[kkk]):
                    matched_kk = kkk
                    break
            if matched_kk != -1:
                found = True
                h = ph
                s = sr
                kk = matched_kk
                template_starts = [rs[0] for rs in run_struct]
                w = this_w
                horiz_diff = 2 * w - 1
                found_inner = True
                break
        if found_inner:
            break

    out = [row[:] for row in g]

    if found:
        step_f = 2 * h - 1
        step_b = 2 * h + 1
        gap = horiz_diff - w
        current_len = len(template_starts)
        # backward
        current_s = s
        for ii in range(kk - 1, -1, -1):
            colors = sig_colors[ii]
            num_b = len(colors)
            temp_starts = template_starts[:]
            if num_b > current_len:
                last_end = temp_starts[-1] + w - 1
                for _ in range(num_b - current_len):
                    new_start = last_end + 1 + gap
                    if new_start + w > n:
                        break
                    temp_starts.append(new_start)
                    last_end = new_start + w - 1
            else:
                temp_starts = temp_starts[:num_b]
            next_len = len(sig_colors[ii + 1]) if ii + 1 < m else current_len
            if num_b > next_len:
                d_step = h
            else:
                d_step = step_b
            current_s -= d_step
            if current_s < 0 or current_s + h > n:
                continue
            for j in range(min(num_b, len(temp_starts))):
                st = temp_starts[j]
                cl = colors[j]
                for rr in range(h):
                    r = current_s + rr
                    if r >= n:
                        break
                    for cc in range(w):
                        c = st + cc
                        if c >= n:
                            break
                        if out[r][c] == bg:
                            out[r][c] = cl
            current_len = num_b
        # forward
        current_s = s
        current_len = len(template_starts)
        for ii in range(kk + 1, m):
            colors = sig_colors[ii]
            num_b = len(colors)
            temp_starts = template_starts[:]
            if num_b > current_len:
                last_end = temp_starts[-1] + w - 1
                for _ in range(num_b - current_len):
                    new_start = last_end + 1 + gap
                    if new_start + w > n:
                        break
                    temp_starts.append(new_start)
                    last_end = new_start + w - 1
            else:
                temp_starts = temp_starts[:num_b]
            prev_len = len(sig_colors[ii - 1])
            if num_b > prev_len:
                d_step = h
            else:
                d_step = step_f
            current_s += d_step
            if current_s + h > n:
                continue
            for j in range(min(num_b, len(temp_starts))):
                st = temp_starts[j]
                cl = colors[j]
                for rr in range(h):
                    r = current_s + rr
                    if r >= n:
                        break
                    for cc in range(w):
                        c = st + cc
                        if c >= n:
                            break
                        if out[r][c] == bg:
                            out[r][c] = cl
            current_len = num_b
        # extra forward
        if m > kk and all(len(sig_colors[j]) == len(sig_colors[m - 1]) for j in range(kk, m)):
            d_step = step_f
            current_s += d_step
            if current_s + h - 1 < n:
                colors = sig_colors[-1]
                num_b = len(colors)
                temp_starts = template_starts[:]
                if num_b > len(template_starts):
                    last_end = temp_starts[-1] + w - 1
                    for _ in range(num_b - len(template_starts)):
                        new_start = last_end + 1 + gap
                        if new_start + w > n:
                            break
                        temp_starts.append(new_start)
                        last_end = new_start + w - 1
                for j in range(min(num_b, len(temp_starts))):
                    st = temp_starts[j]
                    cl = colors[j]
                    for rr in range(h):
                        r = current_s + rr
                        if r >= n:
                            break
                        for cc in range(w):
                            c = st + cc
                            if c >= n:
                                break
                            if out[r][c] == bg:
                                out[r][c] = cl
    else:
        # fallback
        h = 2
        w = 2
        horiz_diff = 2 * w + 1  # 5
        step_f = 2 * h + 1  # 5
        first_start = n // 2
        template_starts = [first_start]
        second_start = first_start + horiz_diff
        if second_start + w - 1 < n:
            template_starts.append(second_start)
        s = min(8, n) + h  # 10
        current_s = s
        gap = horiz_diff - w  # 3
        for ii in range(m):
            colors = sig_colors[ii]
            num_b = len(colors)
            if num_b == 0:
                current_s += step_f
                continue
            temp_starts = template_starts[:]
            if num_b > len(template_starts):
                last_end = temp_starts[-1] + w - 1
                for _ in range(num_b - len(template_starts)):
                    new_start = last_end + 1 + gap
                    if new_start + w > n:
                        break
                    temp_starts.append(new_start)
                    last_end = new_start + w - 1
            else:
                temp_starts = temp_starts[:num_b]
            if current_s + h - 1 >= n:
                break
            for j in range(min(num_b, len(temp_starts))):
                st = temp_starts[j]
                cl = colors[j]
                for rr in range(h):
                    r = current_s + rr
                    if r >= n:
                        break
                    for cc in range(w):
                        c = st + cc
                        if c >= n:
                            break
                        if out[r][c] == bg:
                            out[r][c] = cl
            current_s += step_f
        # extra forward fallback
        if m > 0 and all(len(sc) == len(sig_colors[0]) for sc in sig_colors):
            current_s += step_f
            if current_s + h - 1 < n:
                colors = sig_colors[-1]
                num_b = len(colors)
                temp_starts = template_starts[:]
                if num_b > len(template_starts):
                    last_end = temp_starts[-1] + w - 1
                    for _ in range(num_b - len(template_starts)):
                        new_start = last_end + 1 + gap
                        if new_start + w > n:
                            break
                        temp_starts.append(new_start)
                        last_end = new_start + w - 1
                for j in range(min(num_b, len(temp_starts))):
                    st = temp_starts[j]
                    cl = colors[j]
                    for rr in range(h):
                        r = current_s + rr
                        if r >= n:
                            break
                        for cc in range(w):
                            c = st + cc
                            if c >= n:
                                break
                            if out[r][c] == bg:
                                out[r][c] = cl
    return out
```