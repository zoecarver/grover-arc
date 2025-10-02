```python
from typing import List, Tuple
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

def extract_uniques(g: List[List[int]]) -> Tuple[List[Tuple[List[int], int, int, List[int], int]], int]:
    seen = set()
    uniques = []
    num_non4_rows = 0
    for r in range(13):
        row_data = g[r][:13]
        t = tuple(row_data)
        has_non4 = any(v != 4 for v in row_data)
        if has_non4:
            num_non4_rows += 1
        if has_non4 and t not in seen:
            non4_pos = [i for i in range(13) if row_data[i] != 4]
            min_c = min(non4_pos)
            max_c = max(non4_pos)
            seq = [row_data[i] for i in range(min_c, max_c + 1)]
            rev_seq = seq[::-1]
            uniques.append((row_data, min_c, max_c, rev_seq, max_c - min_c + 1))
            seen.add(t)
    return uniques, num_non4_rows

def program(g: List[List[int]]) -> List[List[int]]:
    g = copy.deepcopy(g)
    N = 27
    CENTER = 13
    # set central cross
    for i in range(N):
        g[i][CENTER] = 1
    g[CENTER] = [1] * N
    # upper processing: horizontal reflection
    for r in range(CENTER):
        for c in range(CENTER):
            if g[r][c] != 4:
                tc = N - 1 - c
                if g[r][tc] == 4:
                    g[r][tc] = g[r][c]
    # upward 8 spread in right upper
    for r in range(CENTER - 1, -1, -1):
        for c in range(CENTER - 1):
            if (g[r + 1 if r + 1 < CENTER else r][c] == 8 and g[r + 1 if r + 1 < CENTER else r][c + 1] == 8 and
                g[r][c] == 4 and g[r][c + 1] == 4):
                tc1 = N - 1 - c
                tc2 = N - 1 - (c + 1)
                if g[r][tc1] == 4 and g[r][tc2] == 4:
                    g[r][tc1] = 8
                    g[r][tc2] = 8
    # horizontal 3 extension in upper right
    for r in range(CENTER):
        i = CENTER + 1
        while i < N:
            if g[r][i] != 2:
                i += 1
                continue
            j = i
            while j < N and g[r][j] == 2:
                j += 1
            L = j - i
            for kk in range(L):
                cc = i - 1 - kk
                if cc < CENTER + 1:
                    break
                if g[r][cc] == 4:
                    g[r][cc] = 3
            i = j
    # exception clear
    for r in range(CENTER):
        if g[r][5:9] == [2, 2, 3, 3]:
            below_all4 = (r + 1 == N or all(g[r + 1][cc] == 4 for cc in range(CENTER)))
            if below_all4:
                for cc in range(18, 22):
                    g[r][cc] = 4
    # now lower
    has_nine = any(9 in row for row in g)
    if has_nine:
        for r in range(CENTER + 1, N):
            for c in range(N):
                g[r][c] = 4 if c != CENTER else 1
        uniques, _ = extract_uniques(g)
        current_r = N - 1
        for idx in range(len(uniques)):
            u = uniques[idx]
            row_data = u[0]
            doubled = get_doubled_sequence(row_data, CENTER)
            num_rows = 1 << idx
            for ii in range(num_rows):
                r = current_r
                g[r][0:CENTER] = doubled[0:CENTER]
                is_even_k = (idx % 2 == 0)
                is_top = (ii == num_rows - 1)
                is_bottom = (ii == 0)
                place_this = False
                which_u = idx
                if is_even_k:
                    if idx > 0 and is_bottom:
                        place_this = True
                        which_u = idx - 1
                    elif 1 <= ii <= num_rows - 2:
                        place_this = True
                        which_u = idx
                else:
                    if idx > 0 and is_top:
                        place_this = True
                        which_u = idx - 1
                if place_this:
                    pu = uniques[which_u]
                    rev_seq = pu[3]
                    max_c = pu[2]
                    start_col = 26 - max_c - 1
                    for jj in range(len(rev_seq)):
                        cc = start_col + jj
                        if 14 <= cc < N:
                            g[r][cc] = rev_seq[jj]
                current_r -= 1
    else:
        changed_rows = set()
        changed_above = set()
        for r in range(1, CENTER):
            has_pair = any(g[r - 1][c] == 8 and g[r - 1][c + 1] == 8 and g[r][c] == 2 and g[r][c + 1] == 2 for c in range(CENTER - 1))
            if has_pair:
                changed_rows.add(r)
                changed_above.add(r - 1)
        special_lower_rows = {26 - rr for rr in changed_rows if 14 <= 26 - rr < N}
        saved_special = {sr: g[sr][0:CENTER][:] for sr in special_lower_rows}
        for r in range(14, N):
            for c in range(CENTER):
                g[r][c] = 4
        for r in range(14, N):
            i = 0
            while i < CENTER:
                if g[r][i] != 2:
                    i += 1
                    continue
                j = i
                while j < CENTER and g[r][j] == 2:
                    j += 1
                L = j - i
                for kk in range(L):
                    cc = j + kk
                    if cc >= CENTER:
                        break
                    if g[r][cc] == 4:
                        g[r][cc] = 3
                i = j
            i = 14
            while i < N:
                if g[r][i] != 2:
                    i += 1
                    continue
                j = i
                while j < N and g[r][j] == 2:
                    j += 1
                L = j - i
                for kk in range(L):
                    cc = i - 1 - kk
                    if cc < 14:
                        break
                    if g[r][cc] == 4:
                        g[r][cc] = 3
                i = j
        max_2_height = 0
        for c in range(CENTER):
            i = 0
            while i < CENTER:
                if g[i][c] != 2:
                    i += 1
                    continue
                j = i
                while j < CENTER and g[j][c] == 2:
                    j += 1
                max_2_height = max(max_2_height, j - i)
                i = j
        target_h = max_2_height * 2
        initial_h = 0
        for c in range(14, N):
            i = 14
            while i < N:
                if g[i][c] != 2:
                    i += 1
                    continue
                j = i
                while j < N and g[j][c] == 2:
                    j += 1
                initial_h = max(initial_h, j - i)
                i = j
        additional_up = max(0, target_h - initial_h)
        extension_count = 0
        changed = True
        while changed and extension_count < additional_up:
            changed = False
            for r in range(15, N):
                i = 14
                while i < N:
                    if g[r][i] != 2:
                        i += 1
                        continue
                    start_i = i
                    while start_i > 14 and g[r][start_i - 1] == 3:
                        start_i -= 1
                    j = i
                    while j < N and g[r][j] == 2:
                        j += 1
                    segment = list(range(start_i, j))
                    if r - 1 >= 14 and all(g[r - 1][cc] == 4 for cc in segment):
                        for cc in segment:
                            if cc < i:
                                g[r - 1][cc] = 3
                            else:
                                g[r - 1][cc] = 2
                        changed = True
                        extension_count += 1
                    i = j
        for rr in range(CENTER):
            for cc in range(CENTER):
                val = g[rr][cc]
                if val != 4:
                    tr = N - 1 - rr
                    tc = N - 1 - cc
                    if tr >= 14 and tc >= 14:
                        if (val == 8 and rr in changed_above) or g[tr][tc] == 4:
                            g[tr][tc] = val
        for r in range(14, N):
            i = 14
            while i < N:
                if g[r][i] != 8:
                    i += 1
                    continue
                j = i
                while j < N and g[r][j] == 8:
                    j += 1
                if i - 1 >= 14:
                    g[r][i - 1] = 8
                i = j
        for r in range(14, N - 1):
            i = 14
            while i < N:
                if g[r][i] != 8:
                    i += 1
                    continue
                j = i
                while j < N and g[r][j] == 8:
                    j += 1
                segment = range(i, j)
                tr = r + 1
                if all(g[tr][cc] == 4 for cc in segment):
                    for cc in segment:
                        g[tr][cc] = 8
                i = j
        for r in range(14, N):
            i = 14
            while i < N:
                if g[r][i] != 3:
                    i += 1
                    continue
                j = i
                while j < N and g[r][j] == 3:
                    j += 1
                if j < N and g[r][j] == 8:
                    for cc in range(i, j):
                        g[r][cc] = 4
                i = j
        for sr in special_lower_rows:
            if 14 <= sr < N:
                for c in range(CENTER):
                    g[sr][c] = saved_special[sr][c]
        for sr in list(special_lower_rows):
            if 14 <= sr < N - 1:
                i = 0
                while i < CENTER:
                    if g[sr][i] != 2:
                        i += 1
                        continue
                    j = i
                    while j < CENTER and g[sr][j] == 2:
                        j += 1
                    L = j - i
                    for kk in range(L):
                        cc = j + kk
                        if cc >= CENTER:
                            break
                        if g[sr][cc] == 4:
                            g[sr][cc] = 3
                    i = j
                for c in range(CENTER):
                    if g[sr][c] == 2:
                        isolated = (c == 0 or g[sr][c - 1] != 2) and (c + 1 == CENTER or g[sr][c + 1] != 2)
                        if isolated and g[sr + 1][c] == 4:
                            g[sr + 1][c] = 8
    return g
```