```python
import typing as tp

List = tp.List

def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def is_power_of_two(x: int) -> bool:
    return x > 0 and (x & (x - 1)) == 0

def get_k(c: int, bg: int) -> int:
    if c == 1:
        return 1 if is_power_of_two(bg) else 2
    if c == 2:
        return 1 if is_power_of_two(bg) else 0
    return c // 2

def is_frame(g: List[List[int]], t: int, l: int, bg: int, n: int, m: int) -> int:
    if t + 4 >= n or l + 10 >= m:
        return -1
    top_c = g[t][l]
    if top_c == bg:
        return -1
    full = all(g[t][j] == top_c for j in range(l, l + 11))
    if not full:
        return -1
    full = all(g[t + 4][j] == top_c for j in range(l, l + 11))
    if not full:
        return -1
    for ii in range(1, 4):
        roww = t + ii
        if g[roww][l] != top_c or g[roww][l + 10] != top_c:
            return -1
        if any(g[roww][j] != bg for j in range(l + 1, l + 10)):
            return -1
    return top_c

def find_frames(g: List[List[int]], bg: int, n: int, m: int) -> List[tp.Tuple[int, int, int]]:
    frames = []
    for t in range(n - 4):
        for l in range(m - 10):
            c = is_frame(g, t, l, bg, n, m)
            if c != -1:
                frames.append((t, l, c))
    return frames

def erase_non_frames(out: List[List[int]], marked: List[List[bool]], bg: int, n: int, m: int):
    for i in range(n):
        for j in range(m):
            if not marked[i][j]:
                out[i][j] = bg

def apply_patterns(out: List[List[int]], frames: List[tp.Tuple[int, int, int]], bg: int):
    for t, l, c in frames:
        mid = t + 2
        for j in range(l + 1, l + 10):
            out[mid][j] = bg
        k = get_k(c, bg)
        s = 9 - 2 * k
        pos = s
        while pos <= 7:
            j = l + 1 + pos
            out[mid][j] = c
            pos += 2

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    if n == 0:
        return []
    m = len(g[0])
    bg = get_background(g)
    frames = find_frames(g, bg, n, m)
    out = [row[:] for row in g]
    marked = [[False] * m for _ in range(n)]
    for t, l, c in frames:
        for j in range(l, l + 11):
            marked[t][j] = True
            marked[t + 4][j] = True
        for ii in range(1, 4):
            marked[t + ii][l] = True
            marked[t + ii][l + 10] = True
    erase_non_frames(out, marked, bg, n, m)
    apply_patterns(out, frames, bg)
    return out
```