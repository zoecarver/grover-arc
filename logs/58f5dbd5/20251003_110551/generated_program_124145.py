```python
from typing import List, Dict, Tuple
import sys

def get_background_color(g: List[List[int]]) -> int:
    """Identify the background color as the border color."""
    return g[0][0]

def find_large_blocks(g: List[List[int]], B: int) -> List[Tuple[int, int, int]]:
    """Find all 5x5 solid non-background blocks: (color, start_row_0idx, start_col_0idx)."""
    n = len(g)
    m = len(g[0])
    large_blocks = []
    for i in range(n - 4):
        for j in range(m - 4):
            color = g[i][j]
            if color == B:
                continue
            is_large = all(g[i + di][j + dj] == color for di in range(5) for dj in range(5))
            if is_large:
                large_blocks.append((color, i, j))
    return large_blocks

def get_group_starts(large_blocks: List[Tuple[int, int, int]]) -> Tuple[List[int], List[int]]:
    """Get sorted unique row starts and col starts from large blocks."""
    r_set = set(rs for _, rs, _ in large_blocks)
    c_set = set(cs for _, _, cs in large_blocks)
    return sorted(list(r_set)), sorted(list(c_set))

def build_block_map(large_blocks: List[Tuple[int, int, int]], r_groups: List[int], c_groups: List[int]) -> Dict[Tuple[int, int], int]:
    """Map (row_group_idx, col_group_idx) to color."""
    block_map: Dict[Tuple[int, int], int] = {}
    for color, rs, cs in large_blocks:
        k = r_groups.index(rs)
        mm = c_groups.index(cs)  # renamed to avoid conflict with built-in
        block_map[(k, mm)] = color
    return block_map

def get_hole_pattern(g: List[List[int]], C: int, rs: int, cs: int, n: int, m: int) -> List[List[int]]:
    """Compute the 3x3 hole pattern (1=hole, 0=keep C) for color C's large at (rs, cs)."""
    small_pos = [(i, j) for i in range(n) for j in range(m)
                 if g[i][j] == C and not (rs <= i < rs + 5 and cs <= j < cs + 5)]
    if not small_pos:
        return [[0, 0, 0] for _ in range(3)]
    small_row_set = set(i for i, _ in small_pos)
    small_rows = sorted(small_row_set)
    h = len(small_rows)
    if h > 3:
        small_rows = small_rows[:3]
        h = 3
    small_col_set = set(j for _, j in small_pos)
    minc = min(small_col_set)
    maxc = max(small_col_set)
    # Assume maxc - minc == 2
    code_cols = list(range(minc, minc + 3))
    code_pattern = []
    for rr in range(h):
        ri = small_rows[rr]
        pat = [1 if g[ri][code_cols[cc]] == C else 0 for cc in range(3)]
        code_pattern.append(pat)
    if h == 3:
        full = code_pattern
    elif h == 2:
        full = [code_pattern[0], code_pattern[0], code_pattern[1]]
    elif h == 1:
        full = [code_pattern[0]] * 3
    else:
        full = [[0, 0, 0]] * 3
    return full

def compute_hole_patterns(g: List[List[int]], large_blocks: List[Tuple[int, int, int]]) -> Dict[int, List[List[int]]]:
    """Compute hole patterns for each color with a large block."""
    n = len(g)
    m = len(g[0])
    color_to_pos: Dict[int, Tuple[int, int]] = {}
    for color, rs, cs in large_blocks:
        color_to_pos[color] = (rs, cs)
    hole_patterns: Dict[int, List[List[int]]] = {}
    for C, (rs, cs) in color_to_pos.items():
        pat = get_hole_pattern(g, C, rs, cs, n, m)
        hole_patterns[C] = pat
    return hole_patterns

def program(g: List[List[int]]) -> List[List[int]]:
    """Main program to transform the input grid according to the puzzle rules."""
    B = get_background_color(g)
    large_blocks = find_large_blocks(g, B)
    if not large_blocks:
        n, m = len(g), len(g[0])
        return [[B] * m for _ in range(n)]  # fallback
    r_groups, c_groups = get_group_starts(large_blocks)
    num_r = len(r_groups)
    num_c = len(c_groups)
    out_h = 5 * num_r + num_r + 1
    out_w = 5 * num_c + num_c + 1
    out_grid = [[B for _ in range(out_w)] for _ in range(out_h)]
    block_map = build_block_map(large_blocks, r_groups, c_groups)
    hole_patterns = compute_hole_patterns(g, large_blocks)
    for k in range(num_r):
        out_r_base = 1 + k * 6
        input_r_base = r_groups[k]
        for mm in range(num_c):  # renamed
            out_c_base = 1 + mm * 6
            key = (k, mm)
            if key in block_map:
                C = block_map[key]
                pat = hole_patterns[C]
                for rel_ri in range(5):
                    out_i = out_r_base + rel_ri
                    for rel_ci in range(5):
                        out_j = out_c_base + rel_ci
                        if rel_ri == 0 or rel_ri == 4 or rel_ci == 0 or rel_ci == 4:
                            out_grid[out_i][out_j] = C
                        else:
                            p_ri = rel_ri - 1
                            p_ci = rel_ci - 1
                            if pat[p_ri][p_ci] == 1:
                                out_grid[out_i][out_j] = B
                            else:
                                out_grid[out_i][out_j] = C
    return out_grid
```