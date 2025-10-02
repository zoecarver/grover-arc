```python
from typing import List, Tuple

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    bg = g[0][0]
    rows = len(g)
    cols = len(g[0])
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(rows):
        for j in range(cols):
            if g[i][j] != bg and not visited[i][j]:
                comp = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and g[nx][ny] != bg:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                if len(comp) >= 10:
                    components.append(comp)
    processed_shapes = []
    for comp in components:
        minr = min(r for r, c in comp)
        maxr = max(r for r, c in comp)
        minc = min(c for r, c in comp)
        maxc = max(c for r, c in comp)
        h = maxr - minr + 1
        w = maxc - minc + 1
        sub = [[g[minr + ii][minc + jj] for jj in range(w)] for ii in range(h)]
        # trim bg columns
        l = 0
        while l < w and all(sub[ii][l] == bg for ii in range(h)):
            l += 1
        r = w - 1
        while r > l and all(sub[ii][r] == bg for ii in range(h)):
            r -= 1
        if l > r:
            continue
        sub = [[sub[ii][l + jj] for jj in range(r - l + 1)] for ii in range(h)]
        h = len(sub)
        w = len(sub[0])
        # trim left protrusions
        l = 0
        while l < w:
            col_col = [sub[ii][l] for ii in range(h)]
            non_bg_col = [c for c in col_col if c != bg]
            if non_bg_col:
                col_set = set(non_bg_col)
                ls = len(col_set)
                if (ls == 1 and 8 in col_set) or (ls <= 3 and 4 in col_set):
                    l += 1
                else:
                    break
            else:
                l += 1
        if l > 0:
            sub = [[sub[ii][l + jj] for jj in range(w - l)] for ii in range(h)]
            w -= l
        # trim right protrusions
        r = w - 1
        while r >= 0:
            col_col = [sub[ii][r] for ii in range(h)]
            non_bg_col = [c for c in col_col if c != bg]
            if non_bg_col:
                col_set = set(non_bg_col)
                ls = len(col_set)
                if ls <= 2 and 5 in col_set:
                    r -= 1
                else:
                    break
            else:
                r -= 1
        if r < w - 1:
            sub = [[sub[ii][jj] for jj in range(r + 1)] for ii in range(h)]
            w = r + 1
        if w == 0:
            continue
        # pad to 5
        pad_top = (5 - h) // 2
        pad_bottom = 5 - h - pad_top
        padded = [[bg] * w for _ in range(5)]
        for ii in range(h):
            for jj in range(w):
                padded[pad_top + ii][jj] = sub[ii][jj]
        processed_shapes.append((minr, minc, padded))
    # order by minr descending
    processed_shapes.sort(key=lambda x: -x[0])
    # build out
    total_w = sum(len(s[2][0]) for _, _, s in processed_shapes)
    out = [[bg] * total_w for _ in range(5)]
    curr = 0
    for _, _, shape in processed_shapes:
        sw = len(shape[0])
        for rr in range(5):
            for jj in range(sw):
                out[rr][curr + jj] = shape[rr][jj]
        curr += sw
    return out
```