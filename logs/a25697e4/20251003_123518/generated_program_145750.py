```python
from typing import List, Tuple
from collections import Counter

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [c for row in g for c in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int, h: int, w: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for i in range(h):
        for j in range(w):
            if not visited[i][j] and g[i][j] != bg:
                color = g[i][j]
                stack = [(i, j)]
                visited[i][j] = True
                comp = [(i, j)]
                while stack:
                    x, y = stack.pop()
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                            comp.append((nx, ny))
                components.append((color, comp))
    return components

def touches_left(pos: List[Tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in pos)

def touches_bottom(pos: List[Tuple[int, int]], h: int) -> bool:
    return any(r == h - 1 for r, _ in pos)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    bg = get_background(g)
    components = find_components(g, bg, h, w)
    anchored_comps = [comp for comp in components if touches_left(comp[1])]
    has_anchored = bool(anchored_comps)
    if has_anchored:
        main_colors = {comp[0] for comp in anchored_comps}
        if len(main_colors) != 1:
            return [[cell for cell in row] for row in g]
        main = next(iter(main_colors))
        main_positions = []
        for colr, poss in components:
            if colr == main:
                main_positions.extend(poss)
        l4 = min(4, w)
        full = [r for r in range(h) if sum(g[r][j] == main for j in range(l4)) == l4]
        partial = [r for r in range(h) if sum(g[r][j] == main for j in range(l4)) == 2]
        gaps = [r for r in range(h) if sum(g[r][j] == main for j in range(l4)) == 0]
        if len(full) != 2 or len(partial) != 1 or len(gaps) != 1:
            out = [[bg] * w for _ in range(h)]
            for r, c in main_positions:
                if 0 <= r < h and 0 <= c < w:
                    out[r][c] = main
            return out
        top, bottom = sorted(full)
        middle = partial[0]
        gap = gaps[0]
        if not (top < gap < bottom and top < middle < bottom and middle != gap):
            out = [[bg] * w for _ in range(h)]
            for r, c in main_positions:
                if 0 <= r < h and 0 <= c < w:
                    out[r][c] = main
            return out
        noise_colors = set(colr for colr, poss in components if colr != bg and colr != main and not touches_left(poss))
        if len(noise_colors) != 2:
            out = [[bg] * w for _ in range(h)]
            for r, c in main_positions:
                if 0 <= r < h and 0 <= c < w:
                    out[r][c] = main
            return out
        min_rows = {}
        for colr in noise_colors:
            all_poss = [p for cc, p in components if cc == colr for _ in p]
            if all_poss:
                min_rows[colr] = min(r for r, _ in all_poss)
            else:
                min_rows[colr] = float('inf')
        upper = min(noise_colors, key=lambda x: min_rows[x])
        lower = max(noise_colors, key=lambda x: min_rows[x])
        if gap < middle:
            inner = upper
            outer = lower
        else:
            inner = lower
            outer = upper
        out = [[bg] * w for _ in range(h)]
        for r, c in main_positions:
            if 0 <= r < h and 0 <= c < w:
                out[r][c] = main
        for j in range(l4):
            if out[middle][j] == bg:
                out[middle][j] = inner
        for j in range(4, 9):
            if j < w:
                out[middle][j] = outer
        for j in range(l4):
            out[gap][j] = inner
        if 8 < w:
            out[gap][8] = outer
        for j in (8, 9):
            if j < w:
                if gap - 1 == top:
                    out[top][j] = outer
                if gap + 1 == bottom:
                    out[bottom][j] = outer
        return out
    else:
        out = [[bg] * w for _ in range(h)]
        for color, pos in components:
            if color == bg:
                continue
            touch_bot = touches_bottom(pos, h)
            new_pos = [(r + 1, c + 6) for r, c in pos]
            all_fit = all(0 <= nr < h and 0 <= nc < w for nr, nc in new_pos)
            if touch_bot or not all_fit:
                place_pos = pos
            else:
                place_pos = new_pos
            for r, c in place_pos:
                if 0 <= r < h and 0 <= c < w:
                    out[r][c] = color
        return out
```