```python
from typing import List, Tuple
import collections

def identify_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = collections.Counter(flat)
    return count.most_common(1)[0][0]

def find_max_r(g: List[List[int]], background: int) -> int:
    n = len(g)
    m = len(g[0])
    max_r = 0
    for i in range(n):
        for j in range(m - 10):
            c = g[i][j]
            if c == background:
                continue
            is_bar = True
            for k in range(1, 11):
                if g[i][j + k] != c:
                    is_bar = False
                    break
            if is_bar:
                max_r = max(max_r, j + 10)
    return max_r

def remove_strays(g: List[List[int]], background: int, max_r: int) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    h = [row[:] for row in g]
    for i in range(n):
        for j in range(max_r + 1, m):
            h[i][j] = background
    return h

def get_s_rel(c: int, l: int) -> int:
    if l == 1:
        if c in (1, 4):
            return 5
        elif c == 2:
            return 8
        elif c == 8:
            return 0
        elif c == 3:
            return 6
        else:
            return 5
    elif l == 2:
        if c == 1:
            return 8
        elif c == 4:
            return 6
        elif c == 6:
            return 4
        else:
            return 6
    return 0

def detect_5row_frames(g: List[List[int]], background: int) -> List[Tuple[int, int, int, int]]:
    n = len(g)
    m = len(g[0])
    frames = []
    for i in range(n - 4):
        for j in range(m - 10):
            c = g[i][j]
            if c == background:
                continue
            is_top = True
            for k in range(11):
                if g[i][j + k] != c:
                    is_top = False
                    break
            if not is_top:
                continue
            l = j
            r = j + 10
            is_frame = True
            for kk in range(1, 4):
                row = i + kk
                if g[row][l] != c or g[row][r] != c:
                    is_frame = False
                    break
            if not is_frame:
                continue
            is_bottom = True
            for k in range(11):
                if g[i + 4][l + k] != c:
                    is_bottom = False
                    break
            if is_bottom:
                frames.append((i, l, r, c))
    return frames

def complete_5row(g: List[List[int]], frame: Tuple[int, int, int, int], background: int) -> List[List[int]]:
    i, l, r, c = frame
    h = [row[:] for row in g]
    for k in range(l, r + 1):
        h[i][k] = c
    for k in range(l, r + 1):
        h[i + 4][k] = c
    for kk in range(1, 4):
        row = i + kk
        h[row][l] = c
        h[row][r] = c
        for k in range(l + 1, r):
            h[row][k] = background
    middle = i + 2
    for k in range(l + 1, r):
        h[middle][k] = background
    h[middle][l] = c
    h[middle][r] = c
    if c != 2:
        s_rel = get_s_rel(c, l)
        for p in range(s_rel, 11, 2):
            pp = l + p
            if pp <= r:
                h[middle][pp] = c
    return h

def detect_4row_frames(g: List[List[int]], background: int) -> List[Tuple[int, int, int, int]]:
    n = len(g)
    m = len(g[0])
    frames = []
    for i in range(1, n - 2):
        for j in range(m - 10):
            c = g[i][j]
            if c == background:
                continue
            is_bar = True
            for k in range(11):
                if g[i][j + k] != c:
                    is_bar = False
                    break
            if not is_bar:
                continue
            l = j
            r = j + 10
            if (g[i + 1][l] != c or g[i + 1][r] != c or
                g[i + 2][l] != c or g[i + 2][r] != c):
                continue
            is_bottom = True
            for k in range(11):
                if g[i + 3][l + k] != c:
                    is_bottom = False
                    break
            if is_bottom:
                frames.append((i, l, r, c))
    return frames

def complete_4row(g: List[List[int]], frame: Tuple[int, int, int, int], background: int) -> List[List[int]]:
    i, l, r, c = frame
    h = [row[:] for row in g]
    for k in range(l, r + 1):
        h[i - 1][k] = c
    for k in range(l, r + 1):
        h[i + 3][k] = c
    for kk in range(3):
        row = i + kk
        h[row][l] = c
        h[row][r] = c
        for k in range(l + 1, r):
            h[row][k] = background
    middle = i + 1
    for k in range(l + 1, r):
        h[middle][k] = background
    h[middle][l] = c
    h[middle][r] = c
    s_rel = get_s_rel(c, l)
    for p in range(s_rel, 11, 2):
        pp = l + p
        if pp <= r:
            h[middle][pp] = c
    return h

def detect_bottom_incomplete(g: List[List[int]], background: int) -> List[Tuple[int, int, int, int]]:
    n = len(g)
    m = len(g[0])
    frames = []
    for i in range(n - 3):
        for j in range(m - 10):
            c = g[i][j]
            if c == background:
                continue
            is_top = True
            for k in range(11):
                if g[i][j + k] != c:
                    is_top = False
                    break
            if not is_top:
                continue
            l = j
            r = j + 10
            if (g[i + 1][l] == c and g[i + 1][r] == c and
                g[i + 2][l] == c and g[i + 2][r] == c and
                g[i + 3][l] == c and g[i + 3][r] == c):
                frames.append((i, l, r, c))
    return frames

def complete_bottom_incomplete(g: List[List[int]], frame: Tuple[int, int, int, int], background: int) -> List[List[int]]:
    i, l, r, c = frame
    h = [row[:] for row in g]
    for k in range(l, r + 1):
        h[i][k] = c
    for kk in range(1, 4):
        row = i + kk
        h[row][l] = c
        h[row][r] = c
        for k in range(l + 1, r):
            h[row][k] = background
    middle = i + 2
    for k in range(l + 1, r):
        h[middle][k] = background
    h[middle][l] = c
    h[middle][r] = c
    if c != 2:
        s_rel = get_s_rel(c, l)
        for p in range(s_rel, 11, 2):
            pp = l + p
            if pp <= r:
                h[middle][pp] = c
    return h

def program(g: List[List[int]]) -> List[List[int]]:
    background = identify_background(g)
    max_r = find_max_r(g, background)
    h = remove_strays(g, background, max_r)
    frames5 = detect_5row_frames(h, background)
    for f in frames5:
        h = complete_5row(h, f, background)
    frames4 = detect_4row_frames(h, background)
    for f in frames4:
        h = complete_4row(h, f, background)
    frames_b = detect_bottom_incomplete(h, background)
    for f in frames_b:
        h = complete_bottom_incomplete(h, f, background)
    return h
```