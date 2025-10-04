```python
from typing import List, Tuple

def get_small_blue(g: List[List[int]]) -> List[Tuple[int, int]]:
    H = len(g)
    W = len(g[0]) if H > 0 else 0
    return [(i, j) for i in range(H) for j in range(W) if g[i][j] == 1]

def get_large_blocks(g: List[List[int]]) -> List[Tuple[int, Tuple[int, int, int, int]]]:
    H = len(g)
    W = len(g[0]) if H > 0 else 0
    color_data = {}
    for i in range(H):
        for j in range(W):
            c = g[i][j]
            if c not in (0, 1):
                if c not in color_data:
                    color_data[c] = {'count': 0, 'minr': i, 'maxr': i, 'minc': j, 'maxc': j}
                d = color_data[c]
                d['count'] += 1
                d['minr'] = min(d['minr'], i)
                d['maxr'] = max(d['maxr'], i)
                d['minc'] = min(d['minc'], j)
                d['maxc'] = max(d['maxc'], j)
    large = []
    for c, d in color_data.items():
        span_r = d['maxr'] - d['minr'] + 1
        span_c = d['maxc'] - d['minc'] + 1
        if d['count'] > 20 and max(span_r, span_c) > 5:
            bbox = (d['minr'], d['minc'], d['maxr'], d['maxc'])
            large.append((c, bbox))
    return large

def expand_blocks(blocks: List[Tuple[int, Tuple[int, int, int, int]]], blues: List[Tuple[int, int]], H: int, W: int) -> List[Tuple[int, Tuple[int, int, int, int]]]:
    expanded = []
    for c, bbox in blocks:
        minr, minc, maxr, maxc = bbox
        for br, bc in blues:
            if minr <= br <= maxr and minc <= bc <= maxc:
                minr = max(0, minr - 1)
                maxr = min(H - 1, maxr + 1)
                minc = max(0, minc - 1)
                maxc = min(W - 1, maxc + 1)
        expanded.append((c, (minr, minc, maxr, maxc)))
    return expanded

def expand_green(g: List[List[int]], blues: List[Tuple[int, int]], H: int, W: int) -> Tuple[int, Tuple[int, int, int, int]]:
    green_pos = [(i, j) for i in range(H) for j in range(W) if g[i][j] == 3]
    if not green_pos:
        return (3, (0, 0, 0, 0))  # Dummy if no green
    minr = min(p[0] for p in green_pos)
    maxr = max(p[0] for p in green_pos)
    minc = min(p[1] for p in green_pos)
    maxc = max(p[1] for p in green_pos)
    # Expand based on proximity to blues (distance <=2 in chebyshev)
    for br, bc in blues:
        if max(abs(br - minr), abs(bc - minc)) <= 2 or max(abs(br - maxr), abs(bc - maxc)) <= 2:
            minr = max(0, min(minr, br) - 1)
            maxr = min(H - 1, max(maxr, br) + 1)
            minc = max(0, min(minc, bc) - 1)
            maxc = min(W - 1, max(maxc, bc) + 1)
    # Special: expand green to full height strip, width 3, positioned at average col
    avg_c = sum(p[1] for p in green_pos) / len(green_pos)
    minc = max(0, int(avg_c - 1))
    maxc = min(W - 1, minc + 3)
    minr = 0
    maxr = H - 1
    return (3, (minr, minc, maxr, maxc))

def expand_zero(g: List[List[int]], blues: List[Tuple[int, int]], H: int, W: int) -> Tuple[int, Tuple[int, int, int, int]]:
    zero_pos = [(i, j) for i in range(H) for j in range(W) if g[i][j] == 0]
    if not zero_pos:
        return (0, (0, 0, 0, 0))  # Dummy
    minr = min(p[0] for p in zero_pos)
    maxr = max(p[0] for p in zero_pos)
    minc = min(p[1] for p in zero_pos)
    maxc = max(p[1] for p in zero_pos)
    # Expand based on proximity to blues
    for br, bc in blues:
        if max(abs(br - minr), abs(bc - minc)) <= 2 or max(abs(br - maxr), abs(bc - maxc)) <= 2:
            minr = max(0, min(minr, br) - 1)
            maxr = min(H - 1, max(maxr, br) + 1)
            minc = max(0, min(minc, bc) - 1)
            maxc = min(W - 1, max(maxc, bc) + 1)
    # Special: expand to bottom-left block
    avg_r = sum(p[0] for p in zero_pos) / len(zero_pos)
    minr = max(0, int(avg_r))
    maxr = H - 1
    minc = 0
    maxc = W // 3
    return (0, (minr, minc, maxr, maxc))

def merge_overlapping(blocks: List[Tuple[int, Tuple[int, int, int, int]]]) -> List[Tuple[int, Tuple[int, int, int, int]]]:
    # Simple: no merging, return as is; overlaps resolved by fill order
    return blocks

def program(g: List[List[int]]) -> List[List[int]]:
    original_h = len(g)
    original_w = len(g[0]) if original_h > 0 else 0
    if original_h != original_w:
        g = [list(row) for row in zip(*g)]
    H = len(g)
    W = len(g[0]) if H > 0 else 0
    blues = get_small_blue(g)
    large_blocks = get_large_blocks(g)
    expanded_blocks = expand_blocks(large_blocks, blues, H, W)
    green_block = expand_green(g, blues, H, W)
    zero_block = expand_zero(g, blues, H, W)
    all_blocks = expanded_blocks[:]
    if green_block[3][2] > green_block[3][0]:  # Valid bbox
        all_blocks.append(green_block)
    if zero_block[3][2] > zero_block[3][0]:  # Valid bbox
        all_blocks.append(zero_block)
    merged_blocks = merge_overlapping(all_blocks)
    # Sort by area descending for fill priority
    merged_blocks.sort(key=lambda x: (x[1][2] - x[1][0] + 1) * (x[1][3] - x[1][1] + 1), reverse=True)
    out = [[0] * W for _ in range(H)]
    for c, (minr, minc, maxr, maxc) in merged_blocks:
        for i in range(max(0, minr), min(H, maxr + 1)):
            for j in range(max(0, minc), min(W, maxc + 1)):
                out[i][j] = c
    # Fill remaining with default (largest block color)
    if merged_blocks:
        default_c = merged_blocks[0][0]
        for i in range(H):
            for j in range(W):
                if out[i][j] == 0:
                    out[i][j] = default_c
    return out
```