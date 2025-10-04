```python
from typing import List, Dict, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    bg = g[0][0] if g else 0

    def find_solid_blocks(g: List[List[int]], b: int) -> List[Tuple[int, int, int]]:
        rows = len(g)
        if rows == 0:
            return []
        cols = len(g[0])
        blocks = []
        for r in range(rows - 4):
            for cc in range(cols - 4):
                sub = [g[r + dr][cc + dc] for dr in range(5) for dc in range(5)]
                color = sub[0]
                if color != b and all(x == color for x in sub):
                    blocks.append((r, cc, color))
        return blocks

    blocks = find_solid_blocks(g, bg)
    if not blocks:
        return [[bg] * len(g[0]) for _ in range(len(g))] if g else []

    def group_blocks(blocks: List[Tuple[int, int, int]]) -> List[List[Tuple[int, int, int]]]:
        if not blocks:
            return []
        sorted_blocks = sorted(blocks, key=lambda x: x[0])
        groups = []
        current_group = [sorted_blocks[0]]
        for blk in sorted_blocks[1:]:
            if blk[0] - current_group[-1][0] < 5:
                current_group.append(blk)
            else:
                groups.append(current_group)
                current_group = [blk]
        groups.append(current_group)
        return groups

    groups = group_blocks(blocks)
    for group in groups:
        group.sort(key=lambda x: x[1])

    num_layers = len(groups)
    max_m = max((len(group) for group in groups), default=0)
    h_out = 6 * num_layers + 1
    w_out = 6 * max_m + 1
    out = [[bg] * w_out for _ in range(h_out)]

    digit_masks: Dict[int, List[List[int]]] = {
        1: [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ],
        2: [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1]
        ],
        4: [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1]
        ],
        6: [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ],
        8: [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1]
        ],
        9: [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1]
        ]
    }

    def get_digit_pattern(c: int, b: int) -> List[List[int]]:
        mask = digit_masks.get(c, [[1] * 5 for _ in range(5)])
        return [[c if mask[i][j] else b for j in range(5)] for i in range(5)]

    for l_idx, group in enumerate(groups):
        r0 = 1 + l_idx * 6
        for pos, (_, _, colr) in enumerate(group):
            c0 = 1 + pos * 6
            pattern = get_digit_pattern(colr, bg)
            for di in range(5):
                for dj in range(5):
                    out[r0 + di][c0 + dj] = pattern[di][dj]

    return out
```