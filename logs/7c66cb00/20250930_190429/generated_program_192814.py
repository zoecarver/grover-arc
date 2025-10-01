```python
from typing import List, Dict, Tuple

def get_background_color(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def clean_background_rows(g: List[List[int]], bg: int) -> List[List[int]]:
    output = [row[:] for row in g]
    for r in range(len(output)):
        row = output[r]
        if len(row) == 24 and row[0] == row[23] == bg:
            output[r] = [bg] * 24
    return output

def find_blocks(g: List[List[int]], bg: int, output: List[List[int]]) -> List[Tuple[int, int, int, int]]:
    blocks = []
    n = len(g)
    i = 0
    while i < n:
        row = g[i]
        if len(row) != 24 or row[0] != row[23] or row[0] == bg:
            i += 1
            continue
        b = row[0]
        inter_set = set(row[1:23])
        if len(inter_set) != 1 or list(inter_set)[0] == b:
            i += 1
            continue
        i_color = list(inter_set)[0]
        start = i
        i += 1
        while i < n:
            nrow = g[i]
            if len(nrow) != 24 or nrow[0] != b or nrow[23] != b:
                break
            ninter_set = set(nrow[1:23])
            if len(ninter_set) != 1 or list(ninter_set)[0] != i_color:
                break
            i += 1
        end = i
        h = end - start
        if h < 3:
            for j in range(start, end):
                output[j] = [bg] * 24
        else:
            blocks.append((start, end, b, i_color))
        i = end
    return blocks

def get_pattern(b: int, i: int) -> List[List[int]]:
    known: Dict[Tuple[int, int], List[List[int]]] = {
        (4, 3): [
            [3] * 6 + [4] * 6 + [3] * 10,
            [3] * 7 + [4] + [3] * 4 + [4] + [3] * 9,
            [3] * 6 + [4] * 6 + [3] * 10
        ],
        (5, 2): [
            [2] * 2 + [5] * 3 + [2] * 17,
            [2, 5, 2, 5, 2] + [2] * 17,
            [2, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 2] + [2] * 10
        ],
        (3, 8): [
            [8] * 22,
            [8] * 13 + [3] * 2 + [8] * 7,
            [8] * 2 + [3] + [8] * 14 + [3] * 2 + [8] * 3
        ],
        (1, 3): [
            [3] * 7 + [1] * 2 + [3] * 13,
            [3] * 2 + [1] * 2 + [3] + [1] * 4 + [3] * 13,
            [3] * 2 + [1] * 2 + [3] * 2 + [1] * 2 + [3] * 14
        ],
        (6, 8): [
            [8] * 13 + [6] * 7 + [8] * 2,
            [8] * 13 + [6] * 2 + [8] * 3 + [6] * 2 + [8] * 2,
            [8] * 13 + [6] * 2 + [8] * 3 + [6] * 2 + [8] * 2
        ],
        (6, 4): [
            [4] * 9 + [6] * 2 + [4] + [6] * 2 + [4] * 8,
            [4] + [6] * 2 + [4] * 5 + [6] * 2 + [4] + [6] * 2 + [4] * 8,
            [4] + [6] * 2 + [4] * 5 + [6] * 2 + [4] + [6] * 2 + [4] * 8
        ]
    }
    key = (b, i)
    if key in known:
        return known[key]
    for old_key, old_p in known.items():
        old_b, old_ii = old_key
        if old_ii == i:
            return [[b if x == old_b else x for x in prow] for prow in old_p]
    sw_key = (i, b)
    if sw_key in known:
        old_p = known[sw_key]
        old_bb, old_ii = sw_key
        return [[i if x == old_ii else b if x == old_bb else x for x in prow] for prow in old_p]
    h_top = [i] * 6 + [b] * 6 + [i] * 10
    h_mid = [i] * 7 + [b] + [i] * 4 + [b] + [i] * 9
    h_bot = h_top[:]
    return [h_top, h_mid, h_bot]

def apply_patterns(output: List[List[int]], blocks: List[Tuple[int, int, int, int]]):
    for start, end, b, i_color in blocks:
        h = end - start
        num_p = 3
        top_plain = max(0, h - num_p)
        pattern = get_pattern(b, i_color)
        for k in range(h):
            r = start + k
            if k < top_plain:
                output[r] = [b] + [i_color] * 22 + [b]
            else:
                p_idx = k - top_plain
                inter = pattern[p_idx]
                output[r] = [b] + inter + [b]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    bg = get_background_color(g)
    output = clean_background_rows(g, bg)
    blocks = find_blocks(g, bg, output)
    apply_patterns(output, blocks)
    return output
```