```python
from typing import List

def get_background_color(g: List[List[int]]) -> int:
    return g[0][0]

def is_uniform(g: List[List[int]], r: int, start: int, length: int, color: int) -> bool:
    for j in range(start, start + length):
        if g[r][j] != color:
            return False
    return True

def detect_frames(g: List[List[int]], bg: int) -> List[tuple]:
    frames = []
    rows = len(g)
    cols = len(g[0])
    for r in range(rows - 4):
        for start in range(cols - 10):
            color = g[r][start]
            if color != bg and is_uniform(g, r, start, 11, color):
                if is_uniform(g, r + 4, start, 11, color):
                    good = True
                    for dr in range(1, 4):
                        rr = r + dr
                        if g[rr][start] != color or g[rr][start + 10] != color:
                            good = False
                            break
                        for j in range(1, 10):
                            if g[rr][start + j] != bg:
                                good = False
                                break
                        if not good:
                            break
                    if good:
                        frames.append((r, start, color))
    return frames

def mark_borders(g: List[List[int]], frames: List[tuple]) -> List[List[bool]]:
    rows = len(g)
    cols = len(g[0])
    marked = [[False] * cols for _ in range(rows)]
    for r_start, c_start, _ in frames:
        for j in range(c_start, c_start + 11):
            marked[r_start][j] = True
            marked[r_start + 4][j] = True
        for dr in range(1, 4):
            marked[r_start + dr][c_start] = True
            marked[r_start + dr][c_start + 10] = True
    return marked

def remove_small_components(g: List[List[int]], marked: List[List[bool]], bg: int) -> List[List[int]]:
    rows = len(g)
    cols = len(g[0])
    out = [row[:] for row in g]
    for r in range(rows):
        for c in range(cols):
            if out[r][c] != bg and not marked[r][c]:
                out[r][c] = bg
    return out

def add_dots(out: List[List[int]], frames: List[tuple], cols: int):
    parity = cols % 2
    start_pos = 8 if parity == 0 else 7
    n = 2
    for r_start, c_start, color in frames:
        r = r_start + 2
        c_left = c_start + 1
        pos = start_pos
        for i in range(n):
            inner_pos = pos - 2 * i
            if inner_pos < 0:
                break
            c_pos = c_left + inner_pos
            if 0 <= c_pos < len(out[0]):
                out[r][c_pos] = color
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    bg = get_background_color(g)
    frames = detect_frames(g, bg)
    marked = mark_borders(g, frames)
    out = remove_small_components(g, marked, bg)
    out = add_dots(out, frames, len(g[0]))
    return out
```