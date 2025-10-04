```python
from typing import List, Tuple, Dict
import collections

def find_8s_block(g: List[List[int]]) -> Tuple[int, int, int, int]:
    n_rows = len(g)
    n_cols = len(g[0])
    max_w = 0
    for row in g:
        curr = 0
        for val in row:
            if val == 8:
                curr += 1
                max_w = max(max_w, curr)
            else:
                curr = 0
    best_h = 0
    best_c_start = -1
    best_r_start = -1
    for c_start in range(n_cols - max_w + 1):
        curr_h = 0
        r_start_curr = 0
        for r in range(n_rows):
            is_good = all(g[r][c_start + k] == 8 for k in range(max_w))
            if is_good:
                curr_h += 1
                if curr_h == 1:
                    r_start_curr = r
                if curr_h > best_h:
                    best_h = curr_h
                    best_c_start = c_start
                    best_r_start = r_start_curr
            else:
                curr_h = 0
    return best_h, max_w, best_r_start, best_c_start

def find_blobs(g: List[List[int]]) -> List[Dict]:
    n_rows = len(g)
    n_cols = len(g[0])
    visited = [[False] * n_cols for _ in range(n_rows)]
    blobs: List[Dict] = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    def compute_blob(y: int, x: int, color: int) -> Dict:
        stack = [(y, x)]
        min_y = max_y = y
        min_x = max_x = x
        count = 0
        while stack:
            cy, cx = stack.pop()
            if visited[cy][cx]:
                continue
            visited[cy][cx] = True
            count += 1
            min_y = min(min_y, cy)
            max_y = max(max_y, cy)
            min_x = min(min_x, cx)
            max_x = max(max_x, cx)
            for dy, dx in directions:
                ny = cy + dy
                nx = cx + dx
                if 0 <= ny < n_rows and 0 <= nx < n_cols and not visited[ny][nx] and g[ny][nx] == color:
                    stack.append((ny, nx))
        return {'color': color, 'bbox': (min_y, min_x, max_y, max_x), 'pixels': count}
    for y in range(n_rows):
        for x in range(n_cols):
            if not visited[y][x]:
                color = g[y][x]
                blob = compute_blob(y, x, color)
                count = blob['pixels']
                if color == 8 or (color == 7 and count > 10):
                    continue
                blobs.append(blob)
    return blobs

def adjust_blobs(blobs: List[Dict]) -> List[Dict]:
    anchors = [b for b in blobs if b['color'] in (1, 9) and b['bbox'][0] <= 5 and b['pixels'] > 20]
    adjusted = []
    for b in blobs:
        y1, x1, y2, x2 = b['bbox']
        for a in anchors:
            a_y1, a_x1, a_y2, a_x2 = a['bbox']
            if max(x1, a_x1) <= min(x2, a_x2) + 2:
                y1 //= 2
                y2 //= 2
                break
        if b['color'] == 4:
            y1 = 0
            y2 = min(y2, 3)
        if 10 <= x1 <= 20:
            x1 = 0
            x2 = min(x2, 5)
        p = b['pixels']
        if p <= 2:
            y_mid = (y1 + y2) // 2
            x_mid = (x1 + x2) // 2
            y1 = y2 = y_mid
            x1 = x2 = x_mid
        elif 3 <= p <= 6:
            adj_blue = any(max(b['bbox'][1], x1) <= min(b['bbox'][3], x2) + 1 and max(b['bbox'][0], y1) <= min(b['bbox'][2], y2) + 1 for b in blobs if b['color'] in (1, 9))
            if adj_blue:
                height = y2 - y1 + 1
                y2 = y1 + 2 * height - 1
        b['bbox'] = (y1, x1, y2, x2)
        adjusted.append(b)
    green_blobs = [b for b in adjusted if b['color'] == 3]
    blue_blobs = [b for b in adjusted if b['color'] in (1, 9)]
    for gb in green_blobs:
        adj_blue = any(max(gb['bbox'][1], bb['bbox'][1]) <= min(gb['bbox'][3], bb['bbox'][3]) + 1 and max(gb['bbox'][0], bb['bbox'][0]) <= min(gb['bbox'][2], bb['bbox'][2]) + 1 for bb in blue_blobs)
        if adj_blue:
            y1, x1, y2, x2 = gb['bbox']
            x1 = 0
            x2 = min(x2, 3)
            gb['bbox'] = (y1, x1, y2, x2)
    return adjusted

def program(g: List[List[int]]) -> List[List[int]]:
    out_h, out_w, _, _ = find_8s_block(g)
    if out_h == 0 or out_w == 0:
        return []
    blobs = find_blobs(g)
    adjusted_blobs = adjust_blobs(blobs)
    adjusted_blobs.sort(key=lambda b: b['pixels'], reverse=True)
    color_out = [[0] * out_w for _ in range(out_h)]
    strength_out = [[0] * out_w for _ in range(out_h)]
    n = 30
    for b in adjusted_blobs:
        y1, x1, y2, x2 = b['bbox']
        sy1 = max(0, int(y1 * out_h / n))
        sy2 = min(out_h - 1, int(y2 * out_h / n))
        sx1 = max(0, int(x1 * out_w / n))
        sx2 = min(out_w - 1, int(x2 * out_w / n))
        p = b['pixels']
        for yy in range(sy1, sy2 + 1):
            for xx in range(sx1, sx2 + 1):
                if strength_out[yy][xx] < p:
                    strength_out[yy][xx] = p
                    color_out[yy][xx] = b['color']
    return color_out
```