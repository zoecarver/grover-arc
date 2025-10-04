```python
from typing import List
from collections import Counter, deque
import copy

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def fill_ones(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    r, c = len(g), len(g[0])
    changed = True
    while changed:
        changed = False
        new_g = [row[:] for row in g]
        for i in range(r):
            for j in range(c):
                if g[i][j] == 1:
                    adj_colors = []
                    for di, dj in directions:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < r and 0 <= nj < c and g[ni][nj] != 1:
                            adj_colors.append(g[ni][nj])
                    if adj_colors:
                        count = Counter(adj_colors)
                        most_common = count.most_common(1)[0][0]
                        new_g[i][j] = most_common
                        changed = True
        g = new_g
    return g

def find_connected_components(g: List[List[int]]) -> List[dict]:
    if not g or not g[0]:
        return []
    h, w = len(g), len(g[0])
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
                components.append({
                    'color': color,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'size': size
                })
    return components

def is_adjacent_or_overlap(b1: tuple, b2: tuple) -> bool:
    r1, c1, r2, c2 = b1
    r3, c3, r4, c4 = b2
    if max(r1, r3) <= min(r2, r4) and max(c1, c3) <= min(c2, c4):
        return True
    if r2 + 1 == r3 or r4 + 1 == r1:
        if max(c1, c3) <= min(c2, c4):
            return True
    if c2 + 1 == c3 or c4 + 1 == c1:
        if max(r1, r3) <= min(r2, r4):
            return True
    return False

def adjust_four_to_six(components: List[dict]) -> List[dict]:
    new_components = copy.deepcopy(components)
    i = 0
    while i < len(new_components):
        if new_components[i]['color'] == 4:
            merged = False
            j = 0
            while j < len(new_components):
                if new_components[j]['color'] == 6:
                    b1 = new_components[j]['bbox']
                    b2 = new_components[i]['bbox']
                    if b1[2] + 1 == b2[0] and max(b1[1], b2[1]) <= min(b1[3], b2[3]):
                        new_b = (
                            min(b1[0], b2[0]),
                            min(b1[1], b2[1]),
                            max(b1[2], b2[2]),
                            max(b1[3], b2[3])
                        )
                        new_components[j]['bbox'] = new_b
                        new_components[j]['size'] += new_components[i]['size']
                        del new_components[i]
                        merged = True
                        break
                j += 1
            if not merged:
                i += 1
        else:
            i += 1
    return new_components

def adjust_five_to_nine(components: List[dict]) -> List[dict]:
    new_components = copy.deepcopy(components)
    i = 0
    while i < len(new_components):
        if new_components[i]['color'] == 5:
            merged = False
            j = 0
            while j < len(new_components):
                if new_components[j]['color'] == 9:
                    b1 = new_components[j]['bbox']
                    b2 = new_components[i]['bbox']
                    dist = b2[0] - b1[2]
                    if 1 <= dist <= 2 and max(b1[1], b2[1]) <= min(b1[3], b2[3]):
                        new_b = (
                            min(b1[0], b2[0]),
                            min(b1[1], b2[1]),
                            max(b1[2], b2[2]),
                            max(b1[3], b2[3])
                        )
                        new_components[j]['bbox'] = new_b
                        new_components[j]['size'] += new_components[i]['size']
                        del new_components[i]
                        merged = True
                        break
                j += 1
            if not merged:
                i += 1
        else:
            i += 1
    return new_components

def adjust_three_to_two(components: List[dict]) -> List[dict]:
    new_components = copy.deepcopy(components)
    i = 0
    while i < len(new_components):
        if new_components[i]['color'] == 3:
            merged = False
            j = 0
            while j < len(new_components):
                if new_components[j]['color'] == 2:
                    b1 = new_components[j]['bbox']
                    b2 = new_components[i]['bbox']
                    if is_adjacent_or_overlap(b1, b2):
                        new_b = (
                            min(b1[0], b2[0]),
                            min(b1[1], b2[1]),
                            max(b1[2], b2[2]),
                            max(b1[3], b2[3])
                        )
                        new_components[j]['bbox'] = new_b
                        new_components[j]['size'] += new_components[i]['size']
                        del new_components[i]
                        merged = True
                        break
                j += 1
            if not merged:
                i += 1
        else:
            i += 1
    return new_components

def merge_six_and_seven(components: List[dict]) -> List[dict]:
    new_components = copy.deepcopy(components)
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(new_components):
            comp_i = new_components[i]
            if comp_i['color'] in (6, 7):
                j = i + 1
                while j < len(new_components):
                    comp_j = new_components[j]
                    if comp_j['color'] == (13 - comp_i['color']):
                        if is_adjacent_or_overlap(comp_i['bbox'], comp_j['bbox']):
                            if comp_i['size'] >= comp_j['size']:
                                new_b = (
                                    min(comp_i['bbox'][0], comp_j['bbox'][0]),
                                    min(comp_i['bbox'][1], comp_j['bbox'][1]),
                                    max(comp_i['bbox'][2], comp_j['bbox'][2]),
                                    max(comp_i['bbox'][3], comp_j['bbox'][3])
                                )
                                comp_i['bbox'] = new_b
                                comp_i['size'] += comp_j['size']
                                del new_components[j]
                                changed = True
                            else:
                                new_b = (
                                    min(comp_j['bbox'][0], comp_i['bbox'][0]),
                                    min(comp_j['bbox'][1], comp_i['bbox'][1]),
                                    max(comp_j['bbox'][2], comp_i['bbox'][2]),
                                    max(comp_j['bbox'][3], comp_i['bbox'][3])
                                )
                                comp_j['bbox'] = new_b
                                comp_j['size'] += comp_i['size']
                                del new_components[i]
                                changed = True
                                i -= 1
                                break
                    j += 1
            if changed:
                break
            i += 1
    return new_components

def merge_all_greens(components: List[dict]) -> List[dict]:
    greens = [c for c in components if c['color'] == 3]
    if not greens:
        return components
    min_r = min(c['bbox'][0] for c in greens)
    min_c = min(c['bbox'][1] for c in greens)
    max_r = max(c['bbox'][2] for c in greens)
    max_c = max(c['bbox'][3] for c in greens)
    total_size = sum(c['size'] for c in greens)
    union_green = {'color': 3, 'bbox': (min_r, min_c, max_r, max_c), 'size': total_size}
    new_components = [c for c in components if c['color'] != 3]
    new_components.append(union_green)
    return new_components

def expand_maroon(components: List[dict], h: int, w: int) -> List[dict]:
    new_components = []
    for c in components:
        if c['color'] == 8:
            min_r = max(0, c['bbox'][0] - 1)
            max_r = min(h - 1, c['bbox'][2] + 1)
            new_bbox = (min_r, c['bbox'][1], max_r, c['bbox'][3])
            new_size = (max_r - min_r + 1) * (c['bbox'][3] - c['bbox'][1] + 1)
            new_c = copy.deepcopy(c)
            new_c['bbox'] = new_bbox
            new_c['size'] = new_size
            new_components.append(new_c)
        else:
            new_components.append(copy.deepcopy(c))
    return new_components

def absorb_small_components(components: List[dict]) -> List[dict]:
    new_components = copy.deepcopy(components)
    i = 0
    while i < len(new_components):
        comp = new_components[i]
        if comp['size'] <= 4 and comp['color'] not in [3, 8, 9]:
            candidates = []
            for j in range(len(new_components)):
                if j != i and is_adjacent_or_overlap(comp['bbox'], new_components[j]['bbox']):
                    candidates.append((new_components[j], j))
            if candidates:
                candidates.sort(key=lambda x: x[0]['size'], reverse=True)
                absorber, j_idx = candidates[0]
                b1 = absorber['bbox']
                b2 = comp['bbox']
                new_b = (
                    min(b1[0], b2[0]),
                    min(b1[1], b2[1]),
                    max(b1[2], b2[2]),
                    max(b1[3], b2[3])
                )
                absorber['bbox'] = new_b
                absorber['size'] += comp['size']
                del new_components[i]
            else:
                i += 1
        else:
            i += 1
    return new_components

def absorb_nine_to_maroon(components: List[dict]) -> List[dict]:
    new_components = copy.deepcopy(components)
    i = 0
    while i < len(new_components):
        if new_components[i]['color'] == 9:
            merged = False
            j = 0
            while j < len(new_components):
                if new_components[j]['color'] == 8 and is_adjacent_or_overlap(new_components[i]['bbox'], new_components[j]['bbox']):
                    if new_components[i]['size'] < new_components[j]['size']:
                        b1 = new_components[j]['bbox']
                        b2 = new_components[i]['bbox']
                        new_b = (
                            min(b1[0], b2[0]),
                            min(b1[1], b2[1]),
                            max(b1[2], b2[2]),
                            max(b1[3], b2[3])
                        )
                        new_components[j]['bbox'] = new_b
                        new_components[j]['size'] += new_components[i]['size']
                        del new_components[i]
                        merged = True
                        break
                j += 1
            if not merged:
                i += 1
        else:
            i += 1
    return new_components

def create_filled_grid(components: List[dict], h: int, w: int) -> List[List[int]]:
    grid = [[0] * w for _ in range(h)]
    sorted_comps = sorted(components, key=lambda x: x['size'], reverse=True)
    for comp in sorted_comps:
        r1, c1, r2, c2 = comp['bbox']
        color = comp['color']
        for rr in range(r1, r2 + 1):
            for cc in range(c1, c2 + 1):
                if 0 <= rr < h and 0 <= cc < w:
                    grid[rr][cc] = color
    return grid

def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    return [list(row) for row in zip(*g)]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h, w = len(g), len(g[0])
    filled = fill_ones(g)
    components = find_connected_components(filled)
    components = adjust_four_to_six(components)
    components = adjust_five_to_nine(components)
    components = adjust_three_to_two(components)
    components = absorb_small_components(components)
    components = absorb_nine_to_maroon(components)
    components = merge_six_and_seven(components)
    components = merge_all_greens(components)
    components = expand_maroon(components, h, w)
    filled_grid = create_filled_grid(components, h, w)
    return transpose_grid(filled_grid)
```