```python
from typing import List
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def find_runs(row: List[int], bg: int, n: int) -> List[tuple]:
    runs = []
    i = 0
    while i < n:
        if row[i] == bg:
            i += 1
            continue
        start = i
        col = row[i]
        while i < n and row[i] == col:
            i += 1
        leng = i - start
        if leng >= 2:
            runs.append((start, leng, col))
    return runs

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    n = len(g)
    if n == 0:
        return out
    bg = get_background(g)
    # Find best stack (max h uniform multi-block)
    best_s = -1
    best_h = 0
    best_w = 0
    best_starts = []
    best_colors = []
    for hh in range(n, 1, -1):
        found = False
        for ss in range(n - hh + 1):
            runs0 = find_runs(g[ss], bg, n)
            if not runs0:
                continue
            ws = {r[1] for r in runs0}
            if len(ws) != 1 or next(iter(ws)) < 2:
                continue
            ww = next(iter(ws))
            numb = len(runs0)
            cons = True
            bcolors = [0] * numb
            for bb in range(numb):
                st, le, cl = runs0[bb]
                if le != ww:
                    cons = False
                    break
                bcolors[bb] = cl
                for rrr in range(ss + 1, ss + hh):
                    for jjj in range(st, st + ww):
                        if g[rrr][jjj] != cl:
                            cons = False
                            break
                    if not cons:
                        break
                if not cons:
                    break
            if cons:
                best_s = ss
                best_h = hh
                best_w = ww
                best_starts = [r[0] for r in runs0]
                best_colors = bcolors
                found = True
                break
        if found:
            break
    if best_s == -1:
        return out
    # Tracks (odd cols with isolated non-bg)
    tracks = []
    for cc in range(1, n, 2):
        has_sig = False
        maxcon = 0
        con = 0
        for rr in range(n):
            if g[rr][cc] != bg:
                has_sig = True
                con += 1
                maxcon = max(maxcon, con)
            else:
                con = 0
        if has_sig and maxcon == 1:
            tracks.append(cc)
    if not tracks:
        return out
    # Signal rows
    sig_rows = sorted({rr for rr in range(n) for cc in tracks if g[rr][cc] != bg})
    # Signal colors (exclude 8)
    sig_colors = []
    for rr in sig_rows:
        sc = [g[rr][cc] for cc in tracks if g[rr][cc] != bg and g[rr][cc] != 8]
        if sc:
            sig_colors.append(sc)
    m = len(sig_colors)
    if m == 0:
        return out
    # Find kk (best match)
    kk = -1
    max_matched = -1
    for k in range(m):
        sc = sig_colors[k]
        matched = 0
        jj = 0
        for col in best_colors:
            found = False
            while jj < len(sc):
                if sc[jj] == col:
                    matched += 1
                    jj += 1
                    found = True
                    break
                jj += 1
            if not found:
                break
        if matched > max_matched:
            max_matched = matched
            kk = k
    if kk == -1 or max_matched == 0:
        return out
    # step_v = diff_starts
    if len(best_starts) >= 2:
        step_v = best_starts[1] - best_starts[0]
    else:
        step_v = best_w + 1
    gap_h = step_v - best_w
    # Place for each i != kk
    for i in range(m):
        if i == kk:
            continue
        delta = i - kk
        pos = best_s + delta * step_v
        if pos < 0 or pos + best_h > n:
            continue
        colors = sig_colors[i]
        num = len(colors)
        temp_starts = best_starts[:]
        last_end = best_starts[-1] + best_w - 1 if best_starts else 0
        while len(temp_starts) < num:
            ns = last_end + 1 + gap_h
            if ns + best_w > n:
                break
            temp_starts.append(ns)
            last_end = ns + best_w - 1
        for b in range(min(num, len(temp_starts))):
            sc = temp_starts[b]
            col = colors[b]
            for rr in range(pos, min(pos + best_h, n)):
                for cc in range(sc, min(sc + best_w, n)):
                    if out[rr][cc] == bg:
                        out[rr][cc] = col
    # Extra forward if all same length
    if m > 0 and len(set(len(sc) for sc in sig_colors)) == 1:
        max_pos = best_s
        for i in range(m):
            if i == kk:
                continue
            delta = i - kk
            p = best_s + delta * step_v
            if 0 <= p and p + best_h <= n:
                max_pos = max(max_pos, p)
        last_colors = sig_colors[-1]
        L = len(last_colors)
        while True:
            next_pos = max_pos + step_v
            if next_pos + best_h > n:
                break
            temp_starts = best_starts[:]
            last_end = best_starts[-1] + best_w - 1 if best_starts else 0
            while len(temp_starts) < L:
                ns = last_end + 1 + gap_h
                if ns + best_w > n:
                    break
                temp_starts.append(ns)
                last_end = ns + best_w - 1
            for b in range(min(L, len(temp_starts))):
                sc = temp_starts[b]
                col = last_colors[b]
                for rr in range(next_pos, min(next_pos + best_h, n)):
                    for cc in range(sc, min(sc + best_w, n)):
                        if out[rr][cc] == bg:
                            out[rr][cc] = col
            max_pos = next_pos
    return out
```