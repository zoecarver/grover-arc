```python
from typing import List, Tuple, Dict
from collections import deque

def get_size(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    return len(g), len(g[0])

def fill_holes(g: List[List[int]]) -> List[List[int]]:
    h, w = get_size(g)
    if h == 0 or w == 0:
        return g
    grid = [row[:] for row in g]
    visited = [[False] * w for _ in range(h)]
    q = deque()
    for i in range(h):
        for j in range(w):
            if grid[i][j] != 1:
                q.append((i, j))
                visited[i][j] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
        i, j = q.popleft()
        color = grid[i][j]
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and grid[ni][nj] == 1:
                grid[ni][nj] = color
                visited[ni][nj] = True
                q.append((ni, nj))
    return grid

def find_connected_components(g: List[List[int]]) -> List[Dict]:
    h, w = get_size(g)
    if h == 0 or w == 0:
        return []
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != 0 and not visited[i][j]:
                color = g[i][j]
                q = deque([(i, j)])
                visited[i][j] = True
                min_r, min_c = i, j
                max_r, max_c = i, j
                size = 1
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            size += 1
                            min_r = min(min_r, nx)
                            max_r = max(max_r, nx)
                            min_c = min(min_c, ny)
                            max_c = max(max_c, ny)
                components.append({
                    'color': color,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'size': size
                })
    return components

def bboxes_adjacent_or_overlap(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1, c1, r2, c2 = b1
    r3, c3, r4, c4 = b2
    if max(r1, r3) <= min(r2, r4) and max(c1, c3) <= min(c2, c4):
        return True
    if (r2 + 1 == r3 or r4 + 1 == r1) and max(c1, c3) <= min(c2, c4):
        return True
    if (c2 + 1 == c3 or c4 + 1 == c1) and max(r1, r3) <= min(r2, r4):
        return True
    return False

def adjust_four_to_six(components: List[Dict]) -> List[Dict]:
    new_components = []
    i = 0
    while i < len(components):
        comp = components[i]
        merged = False
        j = 0
        while j < len(components):
            if j == i:
                j += 1
                continue
            other = components[j]
            if comp['color'] == 4 and other['color'] == 6:
                b1 = comp['bbox']
                b2 = other['bbox']
                if b1[0] == b2[2] + 1 and max(b1[1], b2[1]) <= min(b1[3], b2[3]):
                    r1 = min(b1[0], b2[0])
                    c1 = min(b1[1], b2[1])
                    r2 = max(b1[2], b2[2])
                    c2 = max(b1[3], b2[3])
                    components[j]['bbox'] = (r1, c1, r2, c2)
                    components[j]['size'] += comp['size']
                    merged = True
                    break
            j += 1
        if not merged:
            new_components.append(comp)
        i += 1
    return new_components

def adjust_five_to_nine(components: List[Dict]) -> List[Dict]:
    new_components = []
    i = 0
    while i < len(components):
        comp = components[i]
        merged = False
        j = 0
        while j < len(components):
            if j == i:
                j += 1
                continue
            other = components[j]
            if comp['color'] == 5 and other['color'] == 9:
                b1 = comp['bbox']
                b2 = other['bbox']
                if b1[0] >= b2[2] + 1 and b1[0] <= b2[2] + 2 and max(b1[1], b2[1]) <= min(b1[3], b2[3]):
                    r1 = min(b1[0], b2[0])
                    c1 = min(b1[1], b2[1])
                    r2 = max(b1[2], b2[2])
                    c2 = max(b1[3], b2[3])
                    components[j]['bbox'] = (r1, c1, r2, c2)
                    components[j]['size'] += comp['size']
                    merged = True
                    break
            j += 1
        if not merged:
            new_components.append(comp)
        i += 1
    return new_components

def adjust_three_to_two(components: List[Dict]) -> List[Dict]:
    new_components = []
    i = 0
    while i < len(components):
        comp = components[i]
        merged = False
        j = 0
        while j < len(components):
            if j == i:
                j += 1
                continue
            other = components[j]
            if comp['color'] == 3 and other['color'] == 2:
                if bboxes_adjacent_or_overlap(comp['bbox'], other['bbox']):
                    r1 = min(comp['bbox'][0], other['bbox'][0])
                    c1 = min(comp['bbox'][1], other['bbox'][1])
                    r2 = max(comp['bbox'][2], other['bbox'][2])
                    c2 = max(comp['bbox'][3], other['bbox'][3])
                    components[j]['bbox'] = (r1, c1, r2, c2)
                    components[j]['size'] += comp['size']
                    merged = True
                    break
            j += 1
        if not merged:
            new_components.append(comp)
        i += 1
    return new_components

def merge_six_and_seven(components: List[Dict]) -> List[Dict]:
    ss = [c for c in components if c['color'] in (6, 7)]
    other = [c for c in components if c['color'] not in (6, 7)]
    changed = True
    while changed:
        changed = False
        new_ss = []
        i = 0
        while i < len(ss):
            comp = ss[i]
            merged = False
            j = i + 1
            while j < len(ss):
                oth = ss[j]
                if comp['color'] != oth['color'] and bboxes_adjacent_or_overlap(comp['bbox'], oth['bbox']):
                    if comp['size'] < oth['size']:
                        small = comp
                        large = oth
                    else:
                        small = oth
                        large = comp
                        j = i
                    r1 = min(large['bbox'][0], small['bbox'][0])
                    c1 = min(large['bbox'][1], small['bbox'][1])
                    r2 = max(large['bbox'][2], small['bbox'][2])
                    c2 = max(large['bbox'][3], small['bbox'][3])
                    large['bbox'] = (r1, c1, r2, c2)
                    large['size'] += small['size']
                    changed = True
                    del ss[j]
                else:
                    j += 1
            if not merged:
                new_ss.append(comp)
            i += 1
        ss = new_ss
    return other + ss

def merge_adjacent_greens(components: List[Dict]) -> List[Dict]:
    greens = [c for c in components if c['color'] == 3]
    other = [c for c in components if c['color'] != 3]
    changed = True
    while changed:
        changed = False
        new_greens = []
        i = 0
        while i < len(greens):
            comp = greens[i]
            merged = False
            j = i + 1
            while j < len(greens):
                oth = greens[j]
                if bboxes_adjacent_or_overlap(comp['bbox'], oth['bbox']):
                    r1 = min(comp['bbox'][0], oth['bbox'][0])
                    c1 = min(comp['bbox'][1], oth['bbox'][1])
                    r2 = max(comp['bbox'][2], oth['bbox'][2])
                    c2 = max(comp['bbox'][3], oth['bbox'][3])
                    comp['bbox'] = (r1, c1, r2, c2)
                    comp['size'] += oth['size']
                    changed = True
                    del greens[j]
                else:
                    j += 1
            new_greens.append(comp)
            i += 1
    return other + new_greens

def absorb_small_components(components: List[Dict]) -> List[Dict]:
    smalls = [c for c in components if c['size'] <= 4 and c['color'] not in (0, 3, 8, 9)]
    larges = [c for c in components if not (c['size'] <= 4 and c['color'] not in (0, 3, 8, 9))]
    for small in smalls:
        candidates = [l for l in larges if bboxes_adjacent_or_overlap(small['bbox'], l['bbox'])]
        if candidates:
            large = max(candidates, key=lambda x: x['size'])
            r1 = min(small['bbox'][0], large['bbox'][0])
            c1 = min(small['bbox'][1], large['bbox'][1])
            r2 = max(small['bbox'][2], large['bbox'][2])
            c2 = max(small['bbox'][3], large['bbox'][3])
            large['bbox'] = (r1, c1, r2, c2)
            large['size'] += small['size']
    return larges

def expand_maroon_components(components: List[Dict], h: int, w: int) -> List[Dict]:
    for comp in components:
        if comp['color'] == 8:
            r1, c1, r2, c2 = comp['bbox']
            new_r1 = max(0, r1 - 1)
            new_r2 = min(h - 1, r2 + 1)
            comp['bbox'] = (new_r1, c1, new_r2, c2)
            comp['size'] = (new_r2 - new_r1 + 1) * (c2 - c1 + 1)
    return components

def create_filled_grid(components: List[Dict], h: int, w: int) -> List[List[int]]:
    grid = [[0] * w for _ in range(h)]
    sorted_comps = sorted(components, key=lambda x: x['size'], reverse=True)
    for comp in sorted_comps:
        r1, c1, r2, c2 = comp['bbox']
        color = comp['color']
        for ii in range(max(0, r1), min(h, r2 + 1)):
            for jj in range(max(0, c1), min(w, c2 + 1)):
                grid[ii][jj] = color
    return grid

def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    g = fill_holes(g)
    h, w = get_size(g)
    components = find_connected_components(g)
    components = adjust_four_to_six(components)
    components = adjust_five_to_nine(components)
    components = adjust_three_to_two(components)
    components = merge_six_and_seven(components)
    components = merge_adjacent_greens(components)
    components = absorb_small_components(components)
    components = expand_maroon_components(components, h, w)
    g = create_filled_grid(components, h, w)
    g = transpose_grid(g)
    return g
```