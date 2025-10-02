```python
import typing as tp

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g or not g[0]:
        return []
    bg = g[0][0]
    n = len(g)
    m = len(g[0]) if g else 0
    blocks = []
    for i in range(n - 4):
        for j in range(m - 4):
            c = g[i][j]
            if c == bg:
                continue
            is_solid = True
            for k in range(5):
                if not is_solid:
                    break
                for l in range(5):
                    if g[i + k][j + l] != c:
                        is_solid = False
                        break
            if is_solid:
                blocks.append((i, j, c))
    if not blocks:
        return [[bg]]
    blocks.sort(key=lambda x: x[0])
    groups = []
    current = [blocks[0]]
    for b in blocks[1:]:
        if b[0] <= current[-1][0] + 5:
            current.append(b)
        else:
            groups.append(current)
            current = [b]
    groups.append(current)
    num_groups = len(groups)
    num_b = len(groups[0])
    width = 6 * num_b + 1
    height = 6 * num_groups + 1
    out = [[bg for _ in range(width)] for _ in range(height)]
    patterns = {
        1: [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ],
        2: [
            [2, 2, 2, 2, 2],
            [2, 0, 2, 0, 2],
            [2, 0, 0, 2, 2],
            [2, 0, 2, 0, 2],
            [2, 2, 2, 2, 2]
        ],
        3: [
            [3, 3, 3, 3, 3],
            [3, 0, 3, 0, 3],
            [3, 0, 0, 0, 3],
            [3, 3, 0, 0, 3],
            [3, 3, 3, 3, 3]
        ],
        4: [
            [4, 4, 4, 4, 4],
            [4, 0, 4, 0, 4],
            [4, 0, 0, 0, 4],
            [4, 4, 0, 4, 4],
            [4, 4, 4, 4, 4]
        ],
        6: [
            [6, 6, 6, 6, 6],
            [6, 0, 6, 0, 6],
            [6, 0, 0, 6, 6],
            [6, 0, 6, 6, 6],
            [6, 6, 6, 6, 6]
        ],
        8: [
            [8, 8, 8, 8, 8],
            [8, 0, 0, 8, 8],
            [8, 0, 0, 8, 8],
            [8, 8, 8, 0, 8],
            [8, 8, 8, 8, 8]
        ],
        9: [
            [9, 9, 9, 9, 9],
            [9, 0, 9, 0, 9],
            [9, 0, 0, 9, 9],
            [9, 9, 0, 9, 9],
            [9, 9, 9, 9, 9]
        ]
    }
    current_row = 1
    for group in groups:
        group.sort(key=lambda x: x[1])
        col_offset = 1
        for b in group:
            _, _, colr = b
            if colr not in patterns:
                continue
            pat = patterns[colr]
            for pr in range(5):
                orow = current_row + pr
                for pc in range(5):
                    ocol = col_offset + pc
                    val = pat[pr][pc]
                    if val != 0:
                        out[orow][ocol] = val
            col_offset += 6
        current_row += 5
        if group != groups[-1]:
            current_row += 1
    return out
```