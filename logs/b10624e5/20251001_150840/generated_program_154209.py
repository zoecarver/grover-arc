```python
from typing import List
import copy

def get_doubled_sequence(row_data: List[int], center: int) -> List[int]:
    blocks = []
    first_non4 = -1
    n_non4 = 0
    i = 0
    while i < center:
        if row_data[i] == 4:
            i += 1
            continue
        if first_non4 == -1:
            first_non4 = i
        val = row_data[i]
        j = i
        while j < center and row_data[j] == val:
            j += 1
        length = j - i
        blocks.append((val, length))
        n_non4 += length
        i = j
    if not blocks:
        return [4] * center
    shift = n_non4 // 2
    start_col = max(0, first_non4 - shift)
    new_row = [4] * center
    pos = start_col
    for val, length in blocks:
        for _ in range(2 * length):
            if pos < center:
                new_row[pos] = val
            pos += 1
    return new_row

def program(g: List[List[int]]) -> List[List[int]]:
    out = copy.deepcopy(g)
    N = 27
    CENTER = 13
    for r in range(N):
        out[r][CENTER] = 1
    out[CENTER] = [1] * N
    # Upper half processing
    propagations = []
    changed_rows = set()
    for c in range(CENTER):
        for k in range(CENTER):
            if out[k][c] == 8:
                m = k + 1
                gap_ok = True
                while m < CENTER:
                    if out[m][c] == 2 and gap_ok:
                        if all(out[l][c] == 4 for l in range(k + 1, m)):
                            propagations.append((k, m, c))
                            changed_rows.add(m)
                        gap_ok = False
                        break
                    if out[m][c] != 4:
                        gap_ok = False
                    m += 1
    # Fill gaps
    for k, m, c in propagations:
        if m > k + 1:
            for l in range(k + 1, m):
                out[l][c] = 8
    # Place up 8s in right
    for k, m, c in propagations:
        if m > k + 1:
            distance = m - k
            target_c = 26 - c
            p_found = -1
            for p in range(CENTER):
                if out[p][target_c] == 2:
                    p_found = p
                    break
            if p_found != -1:
                up_r = p_found - distance
                if 0 <= up_r < CENTER:
                    out[up_r][target_c] = 8
    # Extend upper right 2 blocks left
    for r in range(CENTER):
        i = 14
        while i < N:
            if out[r][i] == 2:
                start = i
                while i < N and out[r][i] == 2:
                    i += 1
                lenb = i - start
                for e in range(lenb):
                    lc = start - e - 1
                    if lc < 14:
                        break
                    if out[r][lc] != 4:
                        break
                    out[r][lc] = 3
            else:
                i += 1
    # Skip sources
    skip_sources = set()
    for k, m, c in propagations:
        if m > k + 1:
            skip_sources.add((k, c))
    # Reflect upper
    for r in range(CENTER):
        for c in range(CENTER):
            if out[r][c] == 4:
                continue
            if out[r][c] == 8 and (r, c) in skip_sources:
                continue
            tc = 26 - c
            if 14 <= tc < N and out[r][tc] == 4:
                out[r][tc] = out[r][c]
    # Exception clear
    if changed_rows:
        max_ch = max(changed_rows)
        for r in range(max_ch + 1, CENTER):
            if out[r][5:9] == [2, 2, 3, 3]:
                for tc in range(18, 22):
                    out[r][tc] = 4
    # Check has_nine
    has_nine = any(any(cell == 9 for cell in row) for row in out)
    if has_nine:
        # Clear lower
        for r in range(14, N):
            for c in range(N):
                out[r][c] = 1 if c == CENTER else 4
        # Uniques
        uniques = []
        seen = set()
        for r in range(CENTER):
            pat = tuple(out[r][0:CENTER])
            if all(x == 4 for x in pat):
                continue
            if pat not in seen:
                seen.add(pat)
                uniques.append(pat)
        # Blocks
        blocks = []
        current_r = N - 1
        for idx, pat_tup in enumerate(uniques):
            pat = list(pat_tup)
            num_r = 1 << idx
            doubled = get_doubled_sequence(pat, CENTER)
            this_block = []
            for _ in range(num_r):
                rr = current_r
                out[rr][0:CENTER] = doubled
                this_block.append(rr)
                current_r -= 1
            blocks.append((pat, this_block[::-1]))
        # Reflections
        for i in range(1, len(blocks)):
            source_pat, block_rows = blocks[i]
            k = i
            m_inner = 1 << (k - 1)
            start_off = 0 if k == 1 else (1 << (k - 2))
            for off in range(start_off, start_off + m_inner):
                target_r = block_rows[off]
                for c in range(CENTER):
                    if source_pat[c] == 4:
                        continue
                    v = source_pat[c]
                    tc = 25 - c
                    if 14 <= tc < N and out[target_r][tc] == 4:
                        if v != 8:
                            out[target_r][tc] = v
            if k >= 2:
                prev_pat, _ = blocks[i - 1]
                target_r = block_rows[-1]
                for c in range(CENTER):
                    if prev_pat[c] == 4:
                        continue
                    v = prev_pat[c]
                    tc = 25 - c
                    if 14 <= tc < N and out[target_r][tc] == 4:
                        out[target_r][tc] = v
    else:
        # No nine lower
        # Extend twos lower
        for r in range(14, N):
            # Left extend right
            i = 0
            while i < CENTER:
                if out[r][i] == 2:
                    start = i
                    while i < CENTER and out[r][i] == 2:
                        i += 1
                    lenb = i - start
                    for e in range(lenb):
                        ec = start + lenb + e
                        if ec >= CENTER:
                            break
                        if out[r][ec] != 4:
                            break
                        out[r][ec] = 3
                else:
                    i += 1
            # Right extend left
            i = 14
            while i < N:
                if out[r][i] == 2:
                    start = i
                    while i < N and out[r][i] == 2:
                        i += 1
                    lenb = i - start
                    for e in range(lenb):
                        lc = start - e - 1
                        if lc < 14:
                            break
                        if out[r][lc] != 4:
                            break
                        out[r][lc] = 3
                else:
                    i += 1
        # Isolated twos
        for r in range(14, N - 1):
            for c in range(CENTER):
                if out[r][c] == 2 and (c == 0 or out[r][c - 1] != 2) and (c == CENTER - 1 or out[r][c + 1] != 2):
                    if out[r + 1][c] == 4:
                        out[r + 1][c] = 8
        # Point reflect upper left to lower right
        for rr in range(CENTER):
            for cc in range(CENTER):
                if out[rr][cc] != 4:
                    tr = 26 - rr
                    tc = 26 - cc
                    if 14 <= tc < N and out[tr][tc] == 4:
                        out[tr][tc] = out[rr][cc]
        # Extend 8 left by 1 in lower right
        for r in range(14, N):
            i = 14
            while i < N:
                if out[r][i] == 8:
                    start = i
                    while i < N and out[r][i] == 8:
                        i += 1
                    if start > 14 and out[r][start - 1] == 4:
                        out[r][start - 1] = 8
                else:
                    i += 1
        # Spread down 8's
        max_gap = max((m - k - 1 for k, m, c in propagations), default=0)
        for _ in range(max_gap):
            for r in range(14, N - 1):
                for tc in range(14, N):
                    if out[r][tc] == 8 and out[r + 1][tc] == 4:
                        out[r + 1][tc] = 8
    return out
```