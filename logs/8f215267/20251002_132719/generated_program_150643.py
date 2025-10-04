```python
from collections import Counter
from typing import List, Dict, Tuple

def get_bg_color(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def find_components(g: List[List[int]], bg: int) -> List[Dict]:
    rows = len(g)
    cols = len(g[0]) if rows > 0 else 0
    visited = [[False] * cols for _ in range(rows)]
    components = []
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r in range(rows):
        for c in range(cols):
            if g[r][c] != bg and not visited[r][c]:
                color = g[r][c]
                positions = []
                stack = [(r, c)]
                visited[r][c] = True
                positions.append((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c
                while stack:
                    cr, cc = stack.pop()
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and g[nr][nc] == color:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                            positions.append((nr, nc))
                            min_r = min(min_r, nr)
                            max_r = max(max_r, nr)
                            min_c = min(min_c, nc)
                            max_c = max(max_c, nc)
                size = len(positions)
                components.append({
                    'color': color,
                    'size': size,
                    'positions': positions,
                    'bbox': (min_r, max_r, min_c, max_c)
                })
    return components

def get_small_blobs(components: List[Dict]) -> Dict[int, int]:
    count = {}
    for comp in components:
        if 2 <= comp['size'] <= 8:
            c = comp['color']
            count[c] = count.get(c, 0) + 1
    return count

def get_frames(components: List[Dict]) -> List[Dict]:
    frames = [comp for comp in components if comp['size'] > 8]
    frames.sort(key=lambda x: x['bbox'][0])
    return frames

def get_inner_range(g: List[List[int]], frame: Dict) -> Tuple[int, int, int]:
    outer = frame['color']
    min_r, max_r, _, _ = frame['bbox']
    mrow = (min_r + max_r) // 2
    cols = len(g[0])
    left = None
    right = None
    for c in range(cols):
        if g[mrow][c] == outer:
            if left is None:
                left = c
            right = c
    if left is None or right is None or left >= right:
        return mrow, 0, -1
    ileft = left + 1
    iright = right - 1
    return mrow, ileft, iright

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    out = [row[:] for row in g]
    bg = get_bg_color(g)
    components = find_components(g, bg)
    small_count = get_small_blobs(components)
    frames = get_frames(components)
    for frame in frames:
        outer = frame['color']
        k = small_count.get(outer, 0)
        if k == 0:
            continue
        mrow, ileft, iright = get_inner_range(g, frame)
        if ileft > iright:
            continue
        span = (k - 1) * 2
        start = iright - span - 1
        if start < ileft:
            start = ileft
        i = 0
        while i < k:
            pos = start + i * 2
            if ileft <= pos <= iright:
                out[mrow][pos] = outer
                i += 1
            else:
                break
    for comp in components:
        if 2 <= comp['size'] <= 8:
            for r, c in comp['positions']:
                out[r][c] = bg
    return out
```