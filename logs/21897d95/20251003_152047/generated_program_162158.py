```python
from typing import List, Tuple, Dict
from collections import deque
import math
import heapq

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_size(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    return len(g), len(g[0])

def fill_holes(g: List[List[int]]) -> List[List[int]]:
    h, w = get_size(g)
    if h == 0 or w == 0:
        return g
    priority = {0: 0, 1: 0, 2: 2, 3: 10, 4: 3, 5: 6, 6: 5, 7: 8, 8: 7, 9: 9}
    dist = [[math.inf] * w for _ in range(h)]
    assigned_color = [[0] * w for _ in range(h)]
    pq = []
    for i in range(h):
        for j in range(w):
            if g[i][j] != 1:
                dist[i][j] = 0
                assigned_color[i][j] = g[i][j]
                heapq.heappush(pq, (0, -priority[g[i][j]], i, j))
    while pq:
        d, neg_pri, i, j = heapq.heappop(pq)
        if d > dist[i][j]:
            continue
        curr_pri = priority[assigned_color[i][j]]
        if -neg_pri != curr_pri:
            continue
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < h and 0 <= nj < w:
                new_d = d + 1
                new_color = assigned_color[i][j]
                new_pri = priority[new_color]
                update = False
                if new_d < dist[ni][nj]:
                    update = True
                elif new_d == dist[ni][nj] and new_pri > priority[assigned_color[ni][nj]]:
                    update = True
                if update:
                    dist[ni][nj] = new_d
                    assigned_color[ni][nj] = new_color
                    heapq.heappush(pq, (new_d, -new_pri, ni, nj))
    new_g = [[assigned_color[r][c] if g[r][c] == 1 else g[r][c] for c in range(w)] for r in range(h)]
    return new_g

def find_connected_components(g: List[List[int]]) -> List[Dict]:
    h, w = get_size(g)
    if h == 0 or w == 0:
        return []
    visited = [[False] * w for _ in range(h)]
    components = []
    for i in range(h):
        for j in range(w):
            if g[i][j] != 0 and not visited[i][j]:
                color = g[i][j]
                q = deque([(i, j)])
                visited[i][j] = True
                min_r, min_c, max_r, max_c = i, j, i, j
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
                components.append({'color': color, 'bbox': (min_r, min_c, max_r, max_c), 'size': size})
    return components

def bboxes_adjacent_or_overlap(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1, c1, r2, c2 = b1
    r3, c3, r4, c4 = b2
    if max(r1, r3) <= min(r2, r4) and max(c1, c3) <= min(c2, c4):
        return True
    if r2 + 1 == r3 or r4 + 1 == r1 and max(c1, c3) <= min(c2, c4):
        return True
    if c2 + 1 == c3 or c4 + 1 == c1 and max(r1, r3) <= min(r2, r4):
        return True
    return False

def adjust_four_to_six(components: List[Dict]) -> List[Dict]:
    i = 0
    while i < len(components):
        if components[i]['color'] == 4:
            for k in range(len(components)):
                if k != i and components[k]['color'] == 6:
                    b4 = components[i]['bbox']
                    b6 = components[k]['bbox']
                    r1, _, r2, _ = b4
                    r3, c3, r4, c4 = b6
                    _, c1, _, c2 = b4
                    if r1 == r4 + 1 and max(c1, c3) <= min(c2, c4):
                        components[k]['size'] += components[i]['size']
                        minr = min(components[k]['bbox'][0], b4[0])
                        minc = min(components[k]['bbox'][1], b4[1])
                        maxr = max(components[k]['bbox'][2], b4[2])
                        maxc = max(components[k]['bbox'][3], b4[3])
                        components[k]['bbox'] = (minr, minc, maxr, maxc)
                        del components[i]
                        break
            else:
                i += 1
        else:
            i += 1
    return components

def adjust_three_to_two(components: List[Dict]) -> List[Dict]:
    i = 0
    while i < len(components):
        if components[i]['color'] == 3:
            for k in range(len(components)):
                if k != i and components[k]['color'] == 2 and bboxes_adjacent_or_overlap(components[i]['bbox'], components[k]['bbox']):
                    components[k]['size'] += components[i]['size']
                    minr = min(components[k]['bbox'][0], components[i]['bbox'][0])
                    minc = min(components[k]['bbox'][1], components[i]['bbox'][1])
                    maxr = max(components[k]['bbox'][2], components[i]['bbox'][2])
                    maxc = max(components[k]['bbox'][3], components[i]['bbox'][3])
                    components[k]['bbox'] = (minr, minc, maxr, maxc)
                    del components[i]
                    break
            else:
                i += 1
        else:
            i += 1
    return components

def adjust_five_to_nine(components: List[Dict]) -> List[Dict]:
    i = 0
    while i < len(components):
        if components[i]['color'] == 5:
            for k in range(len(components)):
                if k != i and components[k]['color'] == 9:
                    b5 = components[i]['bbox']
                    b9 = components[k]['bbox']
                    r1, c1, r2, c2 = b5
                    r3, c3, r4, c4 = b9
                    if r1 > r4 and r1 <= r4 + 2 and max(c1, c3) <= min(c2, c4):
                        components[k]['size'] += components[i]['size']
                        minr = min(r3, r1)
                        minc = min(c3, c1)
                        maxr = max(r4, r2)
                        maxc = max(c4, c2)
                        components[k]['bbox'] = (minr, minc, maxr, maxc)
                        del components[i]
                        break
            else:
                i += 1
        else:
            i += 1
    return components

def remove_four_near_nine(components: List[Dict]) -> List[Dict]:
    i = 0
    while i < len(components):
        if components[i]['color'] == 4:
            for k in range(len(components)):
                if k != i and components[k]['color'] == 9 and bboxes_adjacent_or_overlap(components[i]['bbox'], components[k]['bbox']):
                    del components[i]
                    break
            else:
                i += 1
        else:
            i += 1
    return components

def merge_six_into_seven(components: List[Dict]) -> List[Dict]:
    i = 0
    while i < len(components):
        if components[i]['color'] == 6:
            for k in range(len(components)):
                if k != i and components[k]['color'] == 7 and bboxes_adjacent_or_overlap(components[i]['bbox'], components[k]['bbox']):
                    components[k]['size'] += components[i]['size']
                    minr = min(components[k]['bbox'][0], components[i]['bbox'][0])
                    minc = min(components[k]['bbox'][1], components[i]['bbox'][1])
                    maxr = max(components[k]['bbox'][2], components[i]['bbox'][2])
                    maxc = max(components[k]['bbox'][3], components[i]['bbox'][3])
                    components[k]['bbox'] = (minr, minc, maxr, maxc)
                    del components[i]
                    break
            else:
                i += 1
        else:
            i += 1
    return components

def merge_eight_into_seven(components: List[Dict]) -> List[Dict]:
    i = 0
    while i < len(components):
        if components[i]['color'] == 8:
            for k in range(len(components)):
                if k != i and components[k]['color'] == 7 and bboxes_adjacent_or_overlap(components[i]['bbox'], components[k]['bbox']):
                    components[k]['size'] += components[i]['size']
                    minr = min(components[k]['bbox'][0], components[i]['bbox'][0])
                    minc = min(components[k]['bbox'][1], components[i]['bbox'][1])
                    maxr = max(components[k]['bbox'][2], components[i]['bbox'][2])
                    maxc = max(components[k]['bbox'][3], components[i]['bbox'][3])
                    components[k]['bbox'] = (minr, minc, maxr, maxc)
                    del components[i]
                    break
            else:
                i += 1
        else:
            i += 1
    return components

def merge_all_greens(components: List[Dict]) -> List[Dict]:
    greens = [c for c in components if c['color'] == 3]
    if greens:
        total_size = sum(c['size'] for c in greens)
        min_r = min(c['bbox'][0] for c in greens)
        min_c = min(c['bbox'][1] for c in greens)
        max_r = max(c['bbox'][2] for c in greens)
        max_c = max(c['bbox'][3] for c in greens)
        new_green = {'color': 3, 'bbox': (min_r, min_c, max_r, max_c), 'size': total_size}
        components = [c for c in components if c['color'] != 3]
        components.append(new_green)
    return components

def absorb_small_non_blues(components: List[Dict]) -> List[Dict]:
    i = 0
    threshold = 4
    while i < len(components):
        c = components[i]
        if c['size'] <= threshold and c['color'] not in [3, 7, 8, 9]:
            candidates = [k for k in range(len(components)) if k != i and bboxes_adjacent_or_overlap(c['bbox'], components[k]['bbox'])]
            if candidates:
                k = max(candidates, key=lambda kk: components[kk]['size'])
                components[k]['size'] += c['size']
                minr = min(components[k]['bbox'][0], c['bbox'][0])
                minc = min(components[k]['bbox'][1], c['bbox'][1])
                maxr = max(components[k]['bbox'][2], c['bbox'][2])
                maxc = max(components[k]['bbox'][3], c['bbox'][3])
                components[k]['bbox'] = (minr, minc, maxr, maxc)
                del components[i]
            else:
                i += 1
        else:
            i += 1
    return components

def create_filled_grid(components: List[Dict], h: int, w: int) -> List[List[int]]:
    grid = [[0] * w for _ in range(h)]
    sorted_comps = sorted(components, key=lambda c: c['size'], reverse=True)
    for c in sorted_comps:
        r1, c1, r2, c2 = c['bbox']
        colr = c['color']
        for r in range(r1, r2 + 1):
            for cc in range(c1, c2 + 1):
                if 0 <= r < h and 0 <= cc < w:
                    grid[r][cc] = colr
    return grid

def transpose(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    g = fill_holes(g)
    components = find_connected_components(g)
    components = adjust_four_to_six(components)
    components = adjust_three_to_two(components)
    components = adjust_five_to_nine(components)
    components = remove_four_near_nine(components)
    components = merge_six_into_seven(components)
    components = merge_eight_into_seven(components)
    components = merge_all_greens(components)
    components = absorb_small_non_blues(components)
    h, w = get_size(g)
    g = create_filled_grid(components, h, w)
    g = transpose(g)
    return g
```