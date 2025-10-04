```python
from typing import List, Tuple, Dict
from collections import deque, Counter
from copy import deepcopy

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h, w = len(g), len(g[0])
    components = find_connected_components(g)
    components = absorb_small_blues(components, h, w)
    components = absorb_small_non_blues(components, h, w)
    components = handle_color_adjustments(components, h, w)
    components = merge_similar_colors(components)
    components = merge_all_greens(components)
    components = expand_maroon_components(components, h, w)
    filled = create_filled_grid(components, h, w)
    return transpose_grid(filled)

def find_connected_components(g: List[List[int]]) -> List[Dict]:
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != 0 and not visited[i][j]:
                color = g[i][j]
                q = deque([(i, j)])
                visited[i][j] = True
                bbox = [i, j, i, j]
                size = 1
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            size += 1
                            bbox[0] = min(bbox[0], nx)
                            bbox[2] = max(bbox[2], nx)
                            bbox[1] = min(bbox[1], ny)
                            bbox[3] = max(bbox[3], ny)
                components.append({
                    'color': color,
                    'bbox': tuple(bbox),
                    'size': size
                })
    return components

def find_adjacent_components(comp: Dict, other_comps: List[Dict]) -> List[Dict]:
    r1, c1, r2, c2 = comp['bbox']
    adjacent = []
    for o in other_comps:
        or1, oc1, or2, oc2 = o['bbox']
        if max(r1, or1) <= min(r2, or2) + 1 and max(c1, oc1) <= min(c2, oc2) + 1:
            adjacent.append(o)
    return adjacent

def absorb_small_blues(components: List[Dict], h: int, w: int) -> List[Dict]:
    blue_comps = [c for c in components if c['color'] == 1 and c['size'] <= 4]
    non_blue_comps = [c for c in components if c['color'] != 1]
    for b in blue_comps:
        adjacent = find_adjacent_components(b, non_blue_comps)
        if adjacent:
            largest = max(adjacent, key=lambda c: c['size'])
            br1, bc1, br2, bc2 = b['bbox']
            ar1, ac1, ar2, ac2 = largest['bbox']
            new_bbox = (min(br1, ar1), min(bc1, ac1), max(br2, ar2), max(bc2, ac2))
            largest['bbox'] = new_bbox
            largest['size'] += b['size']
    return [c for c in components if c['color'] != 1 or c['size'] > 4]

def absorb_small_non_blues(components: List[Dict], h: int, w: int) -> List[Dict]:
    small_comps = [c for c in components if 1 < c['size'] <= 4 and c['color'] not in [3, 8, 9]]
    large_comps = [c for c in components if c['size'] > 4 or c['color'] in [0, 3, 8, 9]]
    for s in small_comps:
        adjacent = find_adjacent_components(s, large_comps)
        if adjacent:
            largest = max(adjacent, key=lambda c: (c['size'], c['color']))
            sr1, sc1, sr2, sc2 = s['bbox']
            ar1, ac1, ar2, ac2 = largest['bbox']
            new_bbox = (min(sr1, ar1), min(sc1, ac1), max(sr2, ar2), max(sc2, ac2))
            largest['bbox'] = new_bbox
            largest['size'] += s['size']
    kept = [c for c in components if c['size'] > 4 or c['color'] in [0, 3, 8, 9]]
    return kept

def handle_color_adjustments(components: List[Dict], h: int, w: int) -> List[Dict]:
    comps = deepcopy(components)
    i = 0
    while i < len(comps):
        c = comps[i]
        changed = False
        if c['color'] == 4:
            for p in comps:
                if p['color'] == 6 and is_below(c, p):
                    c['color'] = 6
                    cr1, cc1, cr2, cc2 = c['bbox']
                    pr1, pc1, pr2, pc2 = p['bbox']
                    new_bbox = (min(cr1, pr1), min(cc1, pc1), max(cr2, pr2), max(cc2, pc2))
                    p['bbox'] = new_bbox
                    p['size'] += c['size']
                    changed = True
                    break
        if c['color'] == 3:
            for r in comps:
                if r['color'] == 2 and bboxes_adjacent_or_overlap(c['bbox'], r['bbox']):
                    c['color'] = 2
                    cr1, cc1, cr2, cc2 = c['bbox']
                    rr1, rc1, rr2, rc2 = r['bbox']
                    new_bbox = (min(cr1, rr1), min(cc1, rc1), max(cr2, rr2), max(cc2, rc2))
                    r['bbox'] = new_bbox
                    r['size'] += c['size']
                    changed = True
                    break
        if c['color'] == 5:
            for lb in comps:
                if lb['color'] == 9 and is_near(c, lb):
                    c['color'] = 9
                    cr1, cc1, cr2, cc2 = c['bbox']
                    lr1, lc1, lr2, lc2 = lb['bbox']
                    new_bbox = (min(cr1, lr1), min(cc1, lc1), max(cr2, lr2), max(cc2, lc2))
                    lb['bbox'] = new_bbox
                    lb['size'] += c['size']
                    changed = True
                    break
        if changed:
            del comps[i]
        else:
            i += 1
    return comps

def is_below(y: Dict, p: Dict) -> bool:
    y1, yc1, y2, yc2 = y['bbox']
    p1, pc1, p2, pc2 = p['bbox']
    return y1 == p2 + 1 and max(yc1, pc1) <= min(yc2, pc2)

def is_near(o: Dict, lb: Dict) -> bool:
    o1, oc1, o2, oc2 = o['bbox']
    l1, lc1, l2, lc2 = lb['bbox']
    return o2 + 2 >= l1 and max(oc1, lc1) <= min(oc2, lc2)

def bboxes_adjacent_or_overlap(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1, c1, r2, c2 = b1
    r3, c3, r4, c4 = b2
    if max(r1, r3) <= min(r2, r4) and max(c1, c3) <= min(c2, c4):
        return True
    if max(c1, c3) <= min(c2, c4) and (min(r2, r4) == max(r1, r3) + 1 or min(r1, r3) == max(r2, r4) + 1):
        return True
    if max(r1, r3) <= min(r2, r4) and (min(c2, c4) == max(c1, c3) + 1 or min(c1, c3) == max(c2, c4) + 1):
        return True
    return False

def merge_similar_colors(components: List[Dict]) -> List[Dict]:
    comps = deepcopy(components)
    i = 0
    while i < len(comps):
        c = comps[i]
        if c['color'] in (6, 7):
            j = i + 1
            while j < len(comps):
                o = comps[j]
                if o['color'] in (6, 7) and o['color'] != c['color'] and bboxes_adjacent_or_overlap(c['bbox'], o['bbox']):
                    if c['size'] >= o['size']:
                        cr1, cc1, cr2, cc2 = c['bbox']
                        or1, oc1, or2, oc2 = o['bbox']
                        new_bbox = (min(cr1, or1), min(cc1, oc1), max(cr2, or2), max(cc2, oc2))
                        c['bbox'] = new_bbox
                        c['size'] += o['size']
                        del comps[j]
                    else:
                        or1, oc1, or2, oc2 = o['bbox']
                        cr1, cc1, cr2, cc2 = c['bbox']
                        new_bbox = (min(or1, cr1), min(oc1, cc1), max(or2, cr2), max(oc2, cc2))
                        o['bbox'] = new_bbox
                        o['size'] += c['size']
                        del comps[i]
                        break
                j += 1
            if i < len(comps):
                i += 1
        else:
            i += 1
    return comps

def merge_all_greens(components: List[Dict]) -> List[Dict]:
    greens = [c for c in components if c['color'] == 3]
    if not greens:
        return components
    union_r1 = min(g['bbox'][0] for g in greens)
    union_c1 = min(g['bbox'][1] for g in greens)
    union_r2 = max(g['bbox'][2] for g in greens)
    union_c2 = max(g['bbox'][3] for g in greens)
    total_size = sum(g['size'] for g in greens)
    merged = {'color': 3, 'bbox': (union_r1, union_c1, union_r2, union_c2), 'size': total_size}
    non_greens = [c for c in components if c['color'] != 3]
    non_greens.append(merged)
    return non_greens

def expand_maroon_components(components: List[Dict], h: int, w: int) -> List[Dict]:
    comps = []
    for c in components:
        if c['color'] == 8:
            r1, c1, r2, c2 = c['bbox']
            new_r1 = max(0, r1 - 1)
            new_r2 = min(h - 1, r2 + 1)
            c['bbox'] = (new_r1, c1, new_r2, c2)
            c['size'] += (new_r2 - new_r1 + 1 - (r2 - r1 + 1)) * (c2 - c1 + 1)
        comps.append(c)
    return comps

def create_filled_grid(components: List[Dict], h: int, w: int) -> List[List[int]]:
    grid = [[0] * w for _ in range(h)]
    def priority(c):
        return (c['size'], 10 if c['color'] == 3 else 0)
    sorted_comps = sorted(components, key=priority, reverse=True)
    for c in sorted_comps:
        if c['color'] == 0:
            continue
        r1, c1, r2, c2 = c['bbox']
        color = c['color']
        for r in range(r1, r2 + 1):
            for col in range(c1, c2 + 1):
                if 0 <= r < h and 0 <= col < w:
                    grid[r][col] = color
    return grid

def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    return [[g[r][c] for r in range(h)] for c in range(w)]
```