```python
from typing import List
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    h = len(g)
    if h == 0:
        w = 0
    else:
        w = len(g[0])
    counts = defaultdict(int)
    for i in range(h):
        for j in range(w):
            c = g[i][j]
            if c != 8:
                counts[c] += 1
    singletons = sorted([c for c in counts if counts[c] == 1])
    if len(singletons) != 3:
        return g  # Assume exactly 3, otherwise no change
    s1, s2, s3 = singletons
    # Process stems
    for j in range(w):
        i = 0
        while i < h:
            if g[i][j] == 8:
                i += 1
                continue
            c = g[i][j]
            r_start = i
            i += 1
            while i < h and g[i][j] == c:
                i += 1
            r_end = i - 1
            l = r_end - r_start + 1
            if (c == 1 or c == 2) and l >= 4:
                if c == 1:
                    offsets = [1, 3, 5]
                    order = [s1, s2, s3]
                else:
                    offsets = [0, 3, l - 2]
                    order = [s3, s2, s1]
                for k in range(len(offsets)):
                    off = offsets[k]
                    if off < l:
                        fr = r_start + off
                        fc = j
                        colr = order[k]
                        # Left run
                        if fc > 0 and g[fr][fc - 1] == 8:
                            le = fc - 1
                            while le > 0 and g[fr][le - 1] == 8:
                                le -= 1
                            ri = fc - 1
                            while ri < w - 1 and g[fr][ri + 1] == 8:
                                ri += 1
                            for p in range(le, ri + 1):
                                g[fr][p] = colr
                        # Right run
                        if fc < w - 1 and g[fr][fc + 1] == 8:
                            le = fc + 1
                            while le > 0 and g[fr][le - 1] == 8:
                                le -= 1
                            ri = fc + 1
                            while ri < w - 1 and g[fr][ri + 1] == 8:
                                ri += 1
                            for p in range(le, ri + 1):
                                g[fr][p] = colr
    # Find singleton positions
    pos_dict = {}
    for i in range(h):
        for jj in range(w):
            cc = g[i][jj]
            if cc != 8 and counts[cc] == 1:
                pos_dict[cc] = (i, jj)
    # Process each singleton
    for s in singletons:
        if s not in pos_dict:
            continue
        r, c = pos_dict[s]
        if r == h - 1:  # bottom vertical up ascending
            pattern_pos = [0, 1, 4]
            pattern_colors = [s1, s2, s3]
            idx = pattern_colors.index(s)
            offset = pattern_pos[idx]
            start_col = c - offset
            current_r = r
            while current_r >= 0:
                can_place = True
                for pp in range(3):
                    pos = start_col + pattern_pos[pp]
                    if not (0 <= pos < w):
                        can_place = False
                        break
                    intended = pattern_colors[pp]
                    if g[current_r][pos] != 8 and g[current_r][pos] != intended:
                        can_place = False
                        break
                if not can_place:
                    break
                for pp in range(3):
                    pos = start_col + pattern_pos[pp]
                    if 0 <= pos < w:
                        g[current_r][pos] = pattern_colors[pp]
                current_r -= 1
        elif r == 0:  # top horizontal down descending
            pattern_pos = [0, 2, 4]
            pattern_colors = [s3, s2, s1]
            idx = pattern_colors.index(s)
            offset = pattern_pos[idx]
            start_col = c - offset
            current_r = r
            while current_r < h:
                can_place = True
                for pp in range(3):
                    pos = start_col + pattern_pos[pp]
                    if not (0 <= pos < w):
                        can_place = False
                        break
                    intended = pattern_colors[pp]
                    if g[current_r][pos] != 8 and g[current_r][pos] != intended:
                        can_place = False
                        break
                if not can_place:
                    break
                for pp in range(3):
                    pos = start_col + pattern_pos[pp]
                    if 0 <= pos < w:
                        g[current_r][pos] = pattern_colors[pp]
                current_r += 1
        else:  # middle horizontal extend
            # left
            ii = c - 1
            while ii >= 0 and g[r][ii] == 8:
                g[r][ii] = s
                ii -= 1
            # right
            ii = c + 1
            while ii < w and g[r][ii] == 8:
                g[r][ii] = s
                ii += 1
    return g
```