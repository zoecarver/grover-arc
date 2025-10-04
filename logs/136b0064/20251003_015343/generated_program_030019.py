```python
from typing import List, Tuple

def extract_five_positions(g: List[List[int]]) -> List[Tuple[int, int]]:
    positions = []
    H = len(g)
    if H == 0:
        return positions
    W = len(g[0])
    for i in range(H):
        for j in range(W):
            if g[i][j] == 5:
                out_col = j - 8
                if 0 <= out_col < 7:
                    positions.append((i, out_col))
    return positions

def place_fives(grid: List[List[int]], positions: List[Tuple[int, int]]):
    for i, col in positions:
        if 0 <= i < len(grid) and 0 <= col < 7:
            grid[i][col] = 5

def find_blocks(g: List[List[int]]) -> List[int]:
    blocks = []
    H = len(g)
    i = 0
    while i < H - 2:
        row_sum = sum(g[i][0:7])
        if row_sum > 0:
            blocks.append(i)
            i += 3
        else:
            i += 1
    return blocks

def extract_colors(g: List[List[int]], blocks: List[int]) -> Tuple[List[int], List[int]]:
    left_colors = []
    right_colors = []
    H = len(g)
    for start in blocks:
        if start + 2 >= H:
            continue
        left_c = 0
        found_left = False
        for r in range(start, start + 3):
            for c in range(3):
                v = g[r][c]
                if v != 0:
                    left_c = v
                    found_left = True
                    break
            if found_left:
                break
        right_c = 0
        found_right = False
        for r in range(start, start + 3):
            for c in range(4, 7):
                v = g[r][c]
                if v != 0:
                    right_c = v
                    found_right = True
                    break
            if found_right:
                break
        left_colors.append(left_c)
        right_colors.append(right_c)
    return left_colors, right_colors

def place_representations(grid: List[List[int]], left_colors: List[int], right_colors: List[int], s: int, H: int):
    current_row = 1
    current_align = s
    all_colors = left_colors + right_colors
    bar_lengths = {1: 3, 2: 2, 3: 4}
    for color in all_colors:
        if color == 0 or current_row >= H:
            continue
        h = 2 if color == 6 else 1
        if color == 6:
            col_pos = current_align
            for rr in range(h):
                row_idx = current_row + rr
                if row_idx < H and 0 <= col_pos < 7:
                    grid[row_idx][col_pos] = color
        else:
            length = bar_lengths[color]
            if color == 1:
                start_col = current_align
                end_col = min(6, start_col + length - 1)
                for cc in range(start_col, end_col + 1):
                    if cc < 7:
                        grid[current_row][cc] = color
                current_align = end_col
            else:
                end_col = current_align
                start_col = max(0, end_col - length + 1)
                for cc in range(start_col, end_col + 1):
                    grid[current_row][cc] = color
                current_align = start_col
        current_row += h

def program(g: List[List[int]]) -> List[List[int]]:
    H = len(g)
    output = [[0] * 7 for _ in range(H)]
    positions = extract_five_positions(g)
    s = positions[0][1] if positions else 0
    place_fives(output, positions)
    blocks = find_blocks(g)
    left_colors, right_colors = extract_colors(g, blocks)
    place_representations(output, left_colors, right_colors, s, H)
    return output
```