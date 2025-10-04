```python
import typing as tp

def get_blocks(g: tp.List[tp.List[int]], vertical: bool) -> tp.Tuple[int, int, int, int]:
    if vertical:
        blocks: tp.List[tp.Tuple[int, int]] = []
        i = 0
        hh = len(g)
        while i < hh:
            row = g[i]
            if len(set(row)) != 1 or row[0] == 0 or row[0] == 1:
                i += 1
                continue
            cc = row[0]
            start = i
            i += 1
            while i < hh and g[i] == row:
                i += 1
            length = i - start
            if length >= 3:
                blocks.append((length, cc))
        return blocks[-2][0], blocks[-2][1], blocks[-1][0], blocks[-1][1]
    else:
        hh = len(g)
        ww = len(g[0]) if hh > 0 else 0
        blocks: tp.List[tp.Tuple[int, int]] = []
        j = 0
        while j < ww:
            col = [g[r][j] for r in range(hh)]
            if len(set(col)) != 1 or col[0] == 0 or col[0] == 1:
                j += 1
                continue
            cc = col[0]
            start = j
            j += 1
            while j < ww:
                next_col = [g[r][j] for r in range(hh)]
                if next_col == col:
                    j += 1
                else:
                    break
            length = j - start
            if length >= 3:
                blocks.append((length, cc))
        return blocks[-2][0], blocks[-2][1], blocks[-1][0], blocks[-1][1]

def get_mixed_pattern(kk: int, jj: int, c1: int, c2: int) -> tp.List[int]:
    if kk == 4:
        o = jj % 4
        if o == 0:
            return [c1, c1, c1, c2]
        elif o == 1:
            return [c1, c2, c1, c1]
        elif o == 2:
            return [c2, c2, c1, c2]
        else:
            return [c2, c2, c2, c2]
    else:
        return [c1 if (ii < 1 or ii > kk - 2) else c2 for ii in range(kk)]

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g:
        return []
    hh = len(g)
    ww = len(g[0]) if hh > 0 else 0
    vertical = hh > ww
    aa, c1, bb, c2 = get_blocks(g, vertical)
    if vertical:
        out_hh = aa + bb - 2
        out_ww = 2
        full_c1_nn = aa - 2
        full_c2_nn = bb - 2
        left_nn = (full_c1_nn + 1) // 2
        right_nn = full_c1_nn - left_nn
        types = (['full_c1'] * left_nn + ['mixed'] + ['full_c2'] * full_c2_nn + ['full_c1'] * right_nn + ['mixed'])
        out = []
        for tt in types:
            if tt == 'full_c1':
                rr = [c1] * out_ww
            elif tt == 'full_c2':
                rr = [c2] * out_ww
            else:
                rr = [c1, c2]
            out.append(rr)
        return out
    else:
        kk = hh - 2
        out_hh = kk
        if aa > bb:
            full_c1_nn = bb
        elif aa == bb:
            full_c1_nn = 0
        else:
            full_c1_nn = aa
        full_c2_nn = kk - 1
        out_ww = 4 * kk - 1
        full_c2_pos = [3 + 4 * mm for mm in range(full_c2_nn)]
        if kk % 2 == 1:
            full_c1_pos = [1 + 4 * mm for mm in range(full_c1_nn)]
        else:
            full_c1_pos = [2 * mm for mm in range(full_c1_nn)]
        full_c1_set = set(full_c1_pos)
        full_c2_set = set(full_c2_pos)
        out = [[0] * out_ww for _ in range(out_hh)]
        for jj in range(out_ww):
            if jj in full_c1_set:
                for ii in range(out_hh):
                    out[ii][jj] = c1
            elif jj in full_c2_set:
                for ii in range(out_hh):
                    out[ii][jj] = c2
            else:
                pat = get_mixed_pattern(kk, jj, c1, c2)
                for ii in range(out_hh):
                    out[ii][jj] = pat[ii]
        return out
```