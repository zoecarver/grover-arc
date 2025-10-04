```python
from typing import List

def render_block(c: int, is_solid: bool) -> List[List[int]]:
    if c == 0:
        return [[0, 0, 0, 0] for _ in range(4)]
    row_top = [c] * 4
    row_bottom = [c] * 4
    if is_solid:
        row_mid = [c] * 4
    else:
        row_mid = [c, 0, 0, c]
    return [row_top, row_mid, row_mid, row_bottom]

def find_blocks(g: List[List[int]]) -> List[tuple]:
    if not g:
        return []
    height = len(g)
    width = len(g[0])
    blocks = []
    for r in range(height - 3):
        for l in range(width - 3):
            c = g[r][l]
            if c == 0:
                continue
            # check top
            if not all(g[r][l + j] == c for j in range(4)):
                continue
            # check bottom
            if not all(g[r + 3][l + j] == c for j in range(4)):
                continue
            # check middles
            valid = True
            is_solid_flag = True
            is_frame_flag = True
            for i in [1, 2]:
                for j in range(4):
                    cell = g[r + i][l + j]
                    if cell != c and cell != 0:
                        valid = False
                    if cell != c:
                        is_solid_flag = False
                if not valid:
                    break
                # check frame pattern for this mid row
                if g[r + i][l] != c or g[r + i][l + 3] != c:
                    is_frame_flag = False
                if g[r + i][l + 1] != 0 or g[r + i][l + 2] != 0:
                    is_frame_flag = False
            if not valid:
                continue
            if not (is_solid_flag or is_frame_flag):
                continue
            blocks.append((r, c, is_solid_flag))
    return blocks

def program(g: List[List[int]]) -> List[List[int]]:
    blocks = find_blocks(g)
    frames = [b for b in blocks if not b[2]]
    solids = [b for b in blocks if b[2]]
    frames.sort(key=lambda x: x[0])
    solids.sort(key=lambda x: x[0])
    nf = len(frames)
    ns = len(solids)
    num_pairs = max(nf, ns)
    output = []
    for p in range(num_pairs):
        if p < nf:
            left_c = frames[p][1]
            left_is_solid = frames[p][2]
        else:
            left_c = 0
            left_is_solid = False  # irrelevant
        if p < ns:
            right_c = solids[p][1]
            right_is_solid = True
        else:
            right_c = 0
            right_is_solid = False  # irrelevant
        left_pat = render_block(left_c, left_is_solid)
        right_pat = render_block(right_c, right_is_solid)
        for k in range(4):
            output.append(left_pat[k] + right_pat[k])
    return output
```