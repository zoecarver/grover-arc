```python
from typing import List, Tuple

def get_main_canvas(g: List[List[int]]) -> List[List[int]]:
    canvas = [row[:] for row in g[5:]]
    background = canvas[0][0] if canvas else 0
    for row in canvas:
        for j in range(len(row)):
            if row[j] == 5:
                row[j] = background
    return canvas

def get_background(canvas: List[List[int]]) -> int:
    return canvas[0][0] if canvas else 0

def find_seed(canvas: List[List[int]], background: int) -> Tuple[int, int]:
    for i in range(len(canvas)):
        for j in range(len(canvas[0])):
            if canvas[i][j] == 8:
                return i, j
    return 0, 0

def get_blocks(canvas: List[List[int]], background: int) -> List[Tuple[int, int, int, int, int]]:
    height = len(canvas)
    width = len(canvas[0]) if height > 0 else 0
    visited = [[False] * width for _ in range(height)]
    blocks = []
    for i in range(height):
        for j in range(width):
            if not visited[i][j] and canvas[i][j] != background and canvas[i][j] != 8:
                color = canvas[i][j]
                min_i = max_i = i
                min_j = max_j = j
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    min_i = min(min_i, x)
                    max_i = max(max_i, x)
                    min_j = min(min_j, y)
                    max_j = max(max_j, y)
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and canvas[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                blocks.append((min_i, max_i, min_j, max_j, color))
    return blocks

def extend_upper_blocks(canvas: List[List[int]], background: int, blocks: List[Tuple[int, int, int, int, int]], seed_i: int):
    upper_blocks = [b for b in blocks if (b[0] + b[1]) / 2 < seed_i]
    left_upper = None
    if upper_blocks:
        left_upper = min(upper_blocks, key=lambda b: (b[2] + b[3]) / 2)
    for b in upper_blocks:
        color = b[4]
        min_i, min_j, max_j = b[0], b[2], b[3]
        ext_i = min_i - 1
        if ext_i >= 0:
            for j in range(min_j, max_j + 1):
                if canvas[ext_i][j] == background:
                    canvas[ext_i][j] = color
        if b == left_upper:
            ext_i = min_i - 2
            if ext_i >= 0:
                for j in range(min_j, max_j + 1):
                    if canvas[ext_i][j] == background:
                        canvas[ext_i][j] = color

def get_bottom_block(blocks: List[Tuple[int, int, int, int, int]]) -> Tuple[int, int, int, int, int]:
    if not blocks:
        return (0, 0, 0, 0, 0)
    return max(blocks, key=lambda b: (b[0] + b[1]) / 2)

def get_side_blocks(blocks: List[Tuple[int, int, int, int, int]], bottom_block: Tuple[int, int, int, int, int]):
    remaining = [b for b in blocks if b != bottom_block]
    if not remaining:
        return None, None
    left_block = min(remaining, key=lambda b: (b[2] + b[3]) / 2)
    right_block = max(remaining, key=lambda b: (b[2] + b[3]) / 2)
    return left_block, right_block

def fill_vertical(canvas: List[List[int]], background: int, col_start: int, col_end: int, row_start: int, row_end: int):
    height = len(canvas)
    for j in range(col_start, col_end + 1):
        for i in range(max(0, row_start), min(height, row_end + 1)):
            if canvas[i][j] == background:
                canvas[i][j] = 8

def fill_horizontal(canvas: List[List[int]], background: int, row_start: int, row_end: int, col_start: int, col_end: int):
    height = len(canvas)
    width = len(canvas[0]) if height > 0 else 0
    for i in range(max(0, row_start), min(height, row_end + 1)):
        for j in range(col_start, min(width, col_end)):
            if canvas[i][j] == background:
                canvas[i][j] = 8

def program(g: List[List[int]]) -> List[List[int]]:
    canvas = get_main_canvas(g)
    if not canvas:
        return []
    background = get_background(canvas)
    seed_i, seed_j = find_seed(canvas, background)
    blocks = get_blocks(canvas, background)
    extend_upper_blocks(canvas, background, blocks, seed_i)
    bottom_block = get_bottom_block(blocks)
    left_block, right_block = get_side_blocks(blocks, bottom_block)
    middle_start, middle_end = seed_j, min(seed_j + 1, len(canvas[0]) - 1)
    left_start, left_end = 0, 0
    right_start, right_end = 0, 0
    if left_block:
        left_start = left_block[3] + 1
        left_end = left_start + 1
    if right_block:
        right_start = right_block[2] - 2
        right_end = right_start + 1
    bottom_i = bottom_block[0]
    uh1 = max(0, seed_i - 1)
    uh2 = min(len(canvas) - 1, seed_i)
    lh1 = max(0, bottom_i - 2)
    lh2 = min(len(canvas) - 1, bottom_i - 1)
    # upper horizontal from left to right vertical
    fill_horizontal(canvas, background, uh1, uh2, left_start, right_end + 1)
    # lower horizontal from left to right edge
    fill_horizontal(canvas, background, lh1, lh2, left_start, len(canvas[0]))
    # verticals
    # left from upper to lower
    fill_vertical(canvas, background, left_start, left_end, uh1, lh2)
    # right from 0 to upper
    fill_vertical(canvas, background, right_start, right_end, 0, uh2)
    # middle from 0 to lower
    fill_vertical(canvas, background, middle_start, middle_end, 0, lh2)
    return canvas
```