```python
from typing import List, Tuple
from collections import Counter, defaultdict

def get_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], background: int) -> List[Tuple[int, List[Tuple[int, int]]]]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j] and g[i][j] != background:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def touches_left(component: List[Tuple[int, int]]) -> bool:
    return any(c == 0 for _, c in component)

def has_anchored(g: List[List[int]], bg: int) -> bool:
    return any(row[0] != bg for row in g)

def count_main_in_left(g: List[List[int]], r: int, main_color: int, cols: int) -> int:
    return sum(1 for j in range(min(4, cols)) if g[r][j] == main_color)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    rows = len(g)
    cols = len(g[0])
    bg = get_background(g)
    anchored = has_anchored(g, bg)
    components = find_components(g, bg)
    if anchored:
        # Find main_color
        main_color = None
        for r in range(rows):
            if g[r][0] != bg:
                if main_color is None:
                    main_color = g[r][0]
                # Assume consistent
                break
        if main_color is None:
            return [[bg] * cols for _ in range(rows)]
        # Find noise min_rs
        min_rs = defaultdict(lambda: 1000)
        for color, pos in components:
            if color != bg and color != main_color:
                if not touches_left(pos):
                    min_rs[color] = min(min_rs[color], min(r for r, _ in pos))
        noise_list = [c for c in min_rs if min_rs[c] < 1000]
        if len(noise_list) != 2:
            # Fallback: copy input but remove non-main non-bg? Assume 2
            out_g = [[bg] * cols for _ in range(rows)]
            for r in range(rows):
                for c in range(cols):
                    if g[r][c] == main_color:
                        out_g[r][c] = main_color
            return out_g
        c1, c2 = noise_list
        if min_rs[c1] < min_rs[c2]:
            upper, lower = c1, c2
        else:
            upper, lower = c2, c1
        # Find bars
        top_bar = -1
        bottom_bar = -1
        middle_bar = -1
        for r in range(rows):
            cnt = count_main_in_left(g, r, main_color, cols)
            if cnt == 4:
                if top_bar == -1:
                    top_bar = r
                bottom_bar = r
            elif cnt == 2:
                middle_bar = r
        if top_bar == -1 or bottom_bar == -1 or middle_bar == -1:
            # Fallback
            out_g = [[bg] * cols for _ in range(rows)]
            for r in range(rows):
                for c in range(cols):
                    if g[r][c] == main_color:
                        out_g[r][c] = main_color
            return out_g
        # Find gap_row, assume one
        gaps = []
        for r in range(top_bar + 1, bottom_bar):
            if count_main_in_left(g, r, main_color, cols) == 0:
                gaps.append(r)
        if len(gaps) != 1:
            # Fallback
            out_g = [[bg] * cols for _ in range(rows)]
            for r in range(rows):
                for c in range(cols):
                    if g[r][c] == main_color:
                        out_g[r][c] = main_color
            return out_g
        gap_row = gaps[0]
        if gap_row < middle_bar:
            inner = upper
            ext = lower
            upper_gap = True
        else:
            inner = lower
            ext = upper
            upper_gap = False
        # Build output
        out_g = [[bg] * cols for _ in range(rows)]
        # Place original main
        for r in range(rows):
            for c in range(cols):
                if g[r][c] == main_color:
                    out_g[r][c] = main_color
        # Fill middle partial col2-3
        for j in range(2, 4):
            if j < cols:
                out_g[middle_bar][j] = inner
        # Fill gap col0-3
        for j in range(4):
            if j < cols:
                out_g[gap_row][j] = inner
        # Middle extension col4-8
        for j in range(4, 9):
            if j < cols:
                out_g[middle_bar][j] = ext
        # Conditional extensions
        if upper_gap:
            for j in (8, 9):
                if j < cols:
                    out_g[top_bar][j] = ext
            if 8 < cols:
                out_g[gap_row][8] = ext
        else:
            for j in (8, 9):
                if j < cols:
                    out_g[bottom_bar][j] = ext
            if 8 < cols:
                out_g[gap_row][8] = ext
        return out_g
    else:
        # Unanchored: shift components down 1 right 6 if possible
        out_g = [[bg] * cols for _ in range(rows)]
        for color, pos_list in components:
            new_pos_list = [(r + 1, c + 6) for r, c in pos_list]
            if all(0 <= nr < rows and 0 <= nc < cols for nr, nc in new_pos_list):
                for nr, nc in new_pos_list:
                    out_g[nr][nc] = color
            else:
                for r, c in pos_list:
                    out_g[r][c] = color
        return out_g
```