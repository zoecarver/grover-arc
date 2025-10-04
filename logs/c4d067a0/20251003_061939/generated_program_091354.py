```python
from collections import Counter
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [c for row in g for c in row]
    return Counter(flat).most_common(1)[0][0]

def find_singles(g: List[List[int]], b: int, n: int) -> List[Tuple[int, int]]:
    singles = []
    for i in range(n):
        row = g[i]
        nonb_pos = [j for j in range(n) if row[j] != b]
        if len(nonb_pos) == 2 and nonb_pos == [1, 3]:
            color = row[1]
            if row[3] == color:
                singles.append((i, color))
    return singles

def get_subblocks(pos: List[int]) -> List[List[int]]:
    if not pos:
        return []
    pos = sorted(pos)
    sub = [pos[0]]
    subs = []
    for p in pos[1:]:
        if p == sub[-1] + 1:
            sub.append(p)
        else:
            subs.append(sub)
            sub = [p]
    subs.append(sub)
    return subs

def find_block(g: List[List[int]], b: int, n: int) -> Tuple[int, int, List[int], int] | None:
    for start in range(n):
        length = 1
        block_pos = None
        color = None
        for l in range(1, n - start + 1):
            rows = g[start:start + l]
            if block_pos is None:
                first = rows[0]
                block_pos_cand = [j for j in range(7, n) if first[j] != b]
                if len(block_pos_cand) < 4:
                    break
                c_set = set(first[j] for j in block_pos_cand)
                if len(c_set) != 1:
                    break
                color = list(c_set)[0]
                block_pos = block_pos_cand
            consistent = True
            for r in rows[1:]:
                pos_cand = [j for j in range(7, n) if r[j] != b]
                if set(pos_cand) != set(block_pos):
                    consistent = False
                    break
                c_set = set(r[j] for j in block_pos)
                if len(c_set) != 1 or list(c_set)[0] != color:
                    consistent = False
                    break
            if not consistent:
                break
            length = l
        if length >= 2:
            return start, length, block_pos, color
    return None

def find_evolution_block(g: List[List[int]], b: int, n: int) -> Tuple[int, int, List[int], List[int], int, int] | None:
    for start in range(n):
        length = 1
        left_pos = None
        right_pos = None
        left_color = None
        right_color = None
        for l in range(1, n - start + 1):
            rows = g[start:start + l]
            if left_pos is None:
                first = rows[0]
                all_pos = [j for j in range(7, n) if first[j] != b]
                if len(all_pos) < 4:
                    break
                subs = get_subblocks(all_pos)
                if len(subs) != 2:
                    break
                w0 = len(subs[0])
                w1 = len(subs[1])
                if w0 != w1 or w0 < 2:
                    break
                l_set = set(first[j] for j in subs[0])
                r_set = set(first[j] for j in subs[1])
                if len(l_set) != 1 or len(r_set) != 1 or list(l_set)[0] == list(r_set)[0]:
                    break
                left_pos = subs[0]
                right_pos = subs[1]
                left_color = list(l_set)[0]
                right_color = list(r_set)[0]
            consistent = True
            for r in rows[1:]:
                l_pos_cand = [j for j in range(7, n) if r[j] != b and j in set(left_pos)]
                r_pos_cand = [j for j in range(7, n) if r[j] != b and j in set(right_pos)]
                if set(l_pos_cand) != set(left_pos) or set(r_pos_cand) != set(right_pos) or \
                   set([j for j in range(7, n) if r[j] != b]) != set(left_pos + right_pos):
                    consistent = False
                    break
                l_cset = set(r[j] for j in left_pos)
                r_cset = set(r[j] for j in right_pos)
                if len(l_cset) != 1 or list(l_cset)[0] != left_color or \
                   len(r_cset) != 1 or list(r_cset)[0] != right_color:
                    consistent = False
                    break
            if not consistent:
                break
            length = l
        if length >= 2:
            return start, length, left_pos, right_pos, left_color, right_color
    return None

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    b = get_background(g)
    out = [row[:] for row in g]
    uniform_block = find_block(g, b, n)
    if uniform_block:
        start, h, block_pos, _ = uniform_block
        singles = find_singles(g, b, n)
        num = len(singles)
        if num < 1:
            return out
        step = 2 * h - 1
        single_rows_set = set(s[0] for s in singles)
        ext_dict = {i: g[i][5] for i in range(n) if i in single_rows_set and g[i][5] != b}
        first_ext_k = num
        for k in range(num):
            if singles[k][0] in ext_dict:
                first_ext_k = k
                break
        subs = get_subblocks(block_pos)
        if not subs:
            return out
        w = len(subs[0])
        gap = 0
        if len(subs) > 1:
            gap = subs[1][0] - subs[0][-1] - 1
        for k in range(1, num):
            new_start = start + k * step
            if new_start >= n or new_start + h > n:
                continue
            main_color = singles[k][1]
            has_ext = k >= first_ext_k and singles[k][0] in ext_dict
            new_sub = []
            if has_ext:
                last_end = max(block_pos)
                new_sub_start = last_end + 1 + gap
                new_sub = list(range(new_sub_start, new_sub_start + w))
                ext_color = ext_dict[singles[k][0]]
            for rr in range(new_start, new_start + h):
                row = out[rr]
                for j in block_pos:
                    if row[j] == b:
                        row[j] = main_color
                if has_ext:
                    for j in new_sub:
                        if row[j] == b:
                            row[j] = ext_color
        return out
    evo_block = find_evolution_block(g, b, n)
    if evo_block:
        start, h, left_pos, right_pos, left_c, right_c = evo_block
        avail_above = start
        full_back_dist = 5 * h
        if avail_above >= full_back_dist:
            # full above, input is stage 3
            # stage 2
            cl, cr = left_c, right_c
            if cl > cr:
                s2l = cl - 1
                s2r = cr
            elif cr > cl:
                s2l = cl
                s2r = cr - 1
            else:
                s2l = cl - 1
                s2r = cr
            s2_start = start - 3 * h
            for rr in range(s2_start, s2_start + h):
                row = out[rr]
                for j in left_pos:
                    if row[j] == b:
                        row[j] = s2l
                for j in right_pos:
                    if row[j] == b:
                        row[j] = s2r
            # stage 1
            cl, cr = s2l, s2r
            if cl > cr:
                s1l = cl - 1
                s1r = cr
            elif cr > cl:
                s1l = cl
                s1r = cr - 1
            else:
                s1l = cl - 1
                s1r = cr
            s1_start = s2_start - 2 * h
            for rr in range(s1_start, s1_start + h):
                row = out[rr]
                for j in left_pos:
                    if row[j] == b:
                        row[j] = s1l
                for j in right_pos:
                    if row[j] == b:
                        row[j] = s1r
        else:
            # assume stage 2, add stage 1 above, stage 3 below
            # stage 1 above
            s1_start = start - 2 * h
            if s1_start >= 0:
                cl, cr = left_c, right_c
                if cl > cr:
                    s1l = cl - 1
                    s1r = cr
                elif cr > cl:
                    s1l = cl
                    s1r = cr - 1
                else:
                    s1l = cl - 1
                    s1r = cr
                for rr in range(s1_start, s1_start + h):
                    row = out[rr]
                    for j in left_pos:
                        if row[j] == b:
                            row[j] = s1l
                    for j in right_pos:
                        if row[j] == b:
                            row[j] = s1r
            # stage 3 below
            gap2 = 2 * h
            s3_start = start + h + gap2
            if s3_start + h <= n:
                cl, cr = left_c, right_c
                if cl < cr:
                    s3l = cl + 1
                    s3r = cr
                elif cr < cl:
                    s3l = cl
                    s3r = cr + 1
                else:
                    s3l = cl
                    s3r = cr + 1
                for rr in range(s3_start, s3_start + h):
                    row = out[rr]
                    for j in left_pos:
                        if row[j] == b:
                            row[j] = s3l
                    for j in right_pos:
                        if row[j] == b:
                            row[j] = s3r
    return out
```