```python
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    result = [row[:] for row in g]
    rows = len(g)
    if rows == 0:
        return result
    cols = len(g[0])
    candidates = []
    for j in range(cols):
        non_zeros = {g[r][j] for r in range(rows) if g[r][j] != 0}
        if len(non_zeros) == 1:
            candidates.append(j)
    if not candidates:
        return result
    wall = candidates[0]
    for ri in range(rows):
        row = result[ri]
        for j in range(wall + 1, cols):
            row[j] = 0
        if wall == 0 or row[wall - 1] == 0:
            continue
        end = wall - 1
        start = end
        while start > 0 and row[start - 1] != 0:
            start -= 1
        blocks: List[Tuple[int, int]] = []
        i = start
        while i <= end:
            c = row[i]
            n = 0
            while i <= end and row[i] == c:
                n += 1
                i += 1
            blocks.append((c, n))
        right_start = wall + 1
        right_len = cols - right_start
        if right_len <= 0 or not blocks:
            continue
        def generate(blk: List[Tuple[int, int]], ln: int, off: int) -> List[int]:
            if not blk:
                return [0] * ln
            lc, ln_n = blk[-1]
            p = [0] * ln
            prev = blk[:-1]
            for ii in range(ln):
                if (ii + off) % ln_n == 0:
                    p[ii] = lc
            gap_idx = [ii for ii in range(ln) if (ii + off) % ln_n != 0]
            if prev:
                num_g = len(gap_idx)
                sub_off = off + ln_n
                sub_p = generate(prev, num_g, sub_off)
                for jj, gii in enumerate(gap_idx):
                    if jj < len(sub_p):
                        p[gii] = sub_p[jj]
            return p
        pat = generate(blocks, right_len, 0)
        for ii in range(right_len):
            row[right_start + ii] = pat[ii]
    return result
```