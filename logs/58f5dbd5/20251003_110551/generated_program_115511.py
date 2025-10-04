```python
from typing import List, Tuple

def get_bg(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def find_blocks(g: List[List[int]], bg: int) -> List[Tuple[int, int, int]]:
    rows, cols = len(g), len(g[0]) if g else 0
    blocks = []
    for r in range(rows - 4):
        for c in range(cols - 4):
            sub = [row[c:c+5] for row in g[r:r+5]]
            non_bg_colors = set()
            non_bg_count = 0
            for subrow in sub:
                for val in subrow:
                    if val != bg:
                        non_bg_colors.add(val)
                        non_bg_count += 1
            if len(non_bg_colors) == 1 and non_bg_count > 0:
                color = next(iter(non_bg_colors))
                blocks.append((r, c, color))
    return blocks

def group_blocks(blocks: List[Tuple[int, int, int]]) -> List[List[Tuple[int, int, int]]]:
    if not blocks:
        return []
    sorted_blocks = sorted(blocks, key=lambda x: (x[0], x[1]))
    groups = []
    current_group = [sorted_blocks[0]]
    for blk in sorted_blocks[1:]:
        if blk[0] - current_group[-1][0] < 5:
            current_group.append(blk)
        else:
            groups.append(current_group)
            current_group = [blk]
    groups.append(current_group)
    for group in groups:
        group.sort(key=lambda x: x[1])
    return groups

def compute_output_dimensions(num_layers: int, max_per_layer: int, bg: int) -> Tuple[List[List[int]], int, int]:
    height = 6 * num_layers + 1
    width = 6 * max_per_layer + 1
    out = [[bg for _ in range(width)] for _ in range(height)]
    return out, height, width

def place_pattern(out: List[List[int]], group: List[Tuple[int, int, int]], l_idx: int, g: List[List[int]]):
    r0 = 1 + l_idx * 6
    for pos, (s_r, s_c, _) in enumerate(group):
        c0 = 1 + pos * 6
        for di in range(5):
            src_row = g[s_r + di]
            dst_row = out[r0 + di]
            for dj in range(5):
                dst_row[c0 + dj] = src_row[s_c + dj]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    bg = get_bg(g)
    blocks = find_blocks(g, bg)
    groups = group_blocks(blocks)
    if not groups:
        h, w = len(g), len(g[0]) if g else 0
        return [[bg for _ in range(w)] for _ in range(h)]
    num_layers = len(groups)
    max_per_layer = max((len(group) for group in groups), default=0)
    out, height, width = compute_output_dimensions(num_layers, max_per_layer, bg)
    for l_idx, group in enumerate(groups):
        place_pattern(out, group, l_idx, g)
    return out
```