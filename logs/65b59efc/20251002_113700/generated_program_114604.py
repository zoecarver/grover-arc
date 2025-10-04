```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    R = len(g)
    C = len(g[0])
    
    # Find sections from top row
    sections = []
    i = 0
    while i < C:
        if g[0][i] == 5:
            i += 1
            continue
        start = i
        while i < C and g[0][i] != 5:
            i += 1
        length = i - start
        if length > 0:
            sections.append((start, length))
    
    if not sections:
        return []
    s = sections[0][1]
    if any(l != s for _, l in sections):
        raise ValueError("Unequal section lengths")
    m = len(sections)
    starts = [st for st, _ in sections]
    
    # IDs and masks
    id_to_t = {}
    masks = []
    for ti in range(m):
        st = starts[ti]
        id_val = 0
        consistent = True
        mask = [[0] * s for _ in range(s)]
        for rr in range(s):
            for cc in range(s):
                val = g[rr][st + cc]
                if val != 0:
                    if id_val == 0:
                        id_val = val
                    elif val != id_val:
                        consistent = False
                    mask[rr][cc] = 1
        if not consistent or id_val == 0:
            raise ValueError("Inconsistent or empty section")
        ids_ti = id_val
        id_to_t[ids_ti] = ti
        masks.append(mask)
    
    # Colors from last row
    colors = [0] * m
    last_row = g[R - 1]
    for ti in range(m):
        center = starts[ti] + (s // 2)
        if center >= C:
            raise ValueError("Center out of bounds")
        colors[ti] = last_row[center]
        if colors[ti] == 0:
            raise ValueError("No color in center")
    
    # Place types: s x s grid of type or -1
    place_type = [[-1] * s for _ in range(s)]
    
    # Middle spec
    spec_start = s + 1
    for local_r in range(s):
        grow = spec_start + local_r
        if grow >= R:
            continue
        for sec in range(m):
            st = starts[sec]
            for local_c in range(s):
                icol = st + local_c
                if icol >= C:
                    continue
                v = g[grow][icol]
                if v != 0:
                    if v not in id_to_t:
                        raise ValueError("Unknown id")
                    t = id_to_t[v]
                    mc = local_c
                    if place_type[local_r][mc] == -1 or place_type[local_r][mc] == t:
                        place_type[local_r][mc] = t
                    else:
                        # Last wins
                        place_type[local_r][mc] = t
    
    # Build output
    n = s * s
    out = [[0] * n for _ in range(n)]
    for mr in range(s):
        for mc in range(s):
            t = place_type[mr][mc]
            if t == -1:
                continue
            color = colors[t]
            mask = masks[t]
            for lrr in range(s):
                orow = mr * s + lrr
                for lcc in range(s):
                    ocol = mc * s + lcc
                    if mask[lrr][lcc]:
                        out[orow][ocol] = color
    return out
```