```python
from typing import List, Tuple, Dict
from collections import deque

def find_connected_components(g: List[List[int]]) -> List[Dict]:
    if not g or not g[0]:
        return []
    h, w = len(g), len(g[0])
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != 0 and not visited[i][j]:
                color = g[i][j]
                positions = []
                q = deque([(i, j)])
                visited[i][j] = True
                min_r, min_c = i, j
                max_r, max_c = i, j
                size = 1
                positions.append((i, j))
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            positions.append((nx, ny))
                            size += 1
                            min_r = min(min_r, nx)
                            max_r = max(max_r, nx)
                            min_c = min(min_c, ny)
                            max_c = max(max_c, ny)
                components.append({
                    'color': color,
                    'positions': positions,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'size': size
                })
    return components

def get_blue_components(components: List[Dict]) -> List[Dict]:
    return [c for c in components if c['color'] == 1 and c['size'] <= 5]

def get_non_blue_components(components: List[Dict]) -> List[Dict]:
    return [c for c in components if c['color'] != 0 and c['color'] != 1]

def bboxes_overlap_or_adjacent(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1, c1, r2, c2 = b1
    r3, c3, r4, c4 = b2
    # Overlap
    if max(r1, r3) <= min(r2, r4) and max(c1, c3) <= min(c2, c4):
        return True
    # Adjacent vertically (touching or gap 0)
    if abs(min(r2, r4) - max(r1, r3)) <= 1 and max(c1, c3) <= min(c2, c4):
        return True
    # Adjacent horizontally (touching or gap 0)
    if abs(min(c2, c4) - max(c1, c3)) <= 1 and max(r1, r3) <= min(r2, r4):
        return True
    return False

def absorb_small_blues(non_blues: List[Dict], blues: List[Dict]) -> List[Dict]:
    updated = non_blues[:]
    for blue in blues:
        candidates = [nb for nb in updated if bboxes_overlap_or_adjacent(blue['bbox'], nb['bbox'])]
        if candidates:
            chosen = max(candidates, key=lambda c: (c['size'], c['color']))
            br1, bc1, br2, bc2 = blue['bbox']
            r1, c1, r2, c2 = chosen['bbox']
            chosen['bbox'] = (min(r1, br1), min(c1, bc1), max(r2, br2), max(c2, bc2))
            chosen['size'] += blue['size']
    return updated

def absorb_small_non_blues(non_blues: List[Dict]) -> List[Dict]:
    updated = non_blues[:]
    i = 0
    while i < len(updated):
        c = updated[i]
        if c['size'] <= 4 and c['color'] not in {0, 3, 8, 9}:
            candidates = [nb for j, nb in enumerate(updated) if j != i and bboxes_overlap_or_adjacent(c['bbox'], nb['bbox'])]
            if candidates:
                chosen = max(candidates, key=lambda x: (x['size'], x['color']))
                br1, bc1, br2, bc2 = c['bbox']
                r1, c1, r2, c2 = chosen['bbox']
                chosen['bbox'] = (min(r1, br1), min(c1, bc1), max(r2, br2), max(c2, bc2))
                chosen['size'] += c['size']
                del updated[i]
                i -= 1
        i += 1
    return updated

def merge_greens(non_blues: List[Dict]) -> List[Dict]:
    greens = [c for c in non_blues if c['color'] == 3]
    if not greens:
        return non_blues
    min_r = min(c['bbox'][0] for c in greens)
    min_c = min(c['bbox'][1] for c in greens)
    max_r = max(c['bbox'][2] for c in greens)
    max_c = max(c['bbox'][3] for c in greens)
    total_size = sum(c['size'] for c in greens)
    union_green = {'color': 3, 'positions': [], 'bbox': (min_r, min_c, max_r, max_c), 'size': total_size}
    return [c for c in non_blues if c['color'] != 3] + [union_green]

def merge_pink_darkred(non_blues: List[Dict]) -> List[Dict]:
    updated = non_blues[:]
    i = 0
    while i < len(updated):
        c = updated[i]
        if c['color'] == 6:
            for j in range(len(updated)):
                if j != i and updated[j]['color'] == 7 and bboxes_overlap_or_adjacent(c['bbox'], updated[j]['bbox']):
                    if c['size'] >= updated[j]['size']:
                        br1, bc1, br2, bc2 = updated[j]['bbox']
                        r1, c1, r2, c2 = c['bbox']
                        c['bbox'] = (min(r1, br1), min(c1, bc1), max(r2, br2), max(c2, bc2))
                        c['size'] += updated[j]['size']
                        del updated[j]
                        if j < i:
                            i -= 1
                        break
                    else:
                        br1, bc1, br2, bc2 = c['bbox']
                        r1, c1, r2, c2 = updated[j]['bbox']
                        updated[j]['bbox'] = (min(r1, br1), min(c1, bc1), max(r2, br2), max(c2, bc2))
                        updated[j]['size'] += c['size']
                        del updated[i]
                        i -= 1
                        break
        i += 1
    return updated

def expand_maroon(non_blues: List[Dict], h: int, w: int) -> List[Dict]:
    for c in non_blues:
        if c['color'] == 8:
            r1, c1, r2, c2 = c['bbox']
            new_r1 = max(0, r1 - 1)
            new_r2 = min(h - 1, r2 + 1)
            c['bbox'] = (new_r1, c1, new_r2, c2)
    return non_blues

def adjust_yellow_to_pink(non_blues: List[Dict]) -> List[Dict]:
    yellows = [c for c in non_blues if c['color'] == 4]
    pinks = [c for c in non_blues if c['color'] == 6]
    for y in yellows:
        for p in pinks:
            pr1, pc1, pr2, pc2 = p['bbox']
            yr1, yc1, yr2, yc2 = y['bbox']
            if yr1 == pr2 + 1 and max(pc1, yc1) <= min(pc2, yc2):
                y['color'] = 6
                break
    return non_blues

def adjust_green_to_red(non_blues: List[Dict]) -> List[Dict]:
    greens = [c for c in non_blues if c['color'] == 3]
    reds = [c for c in non_blues if c['color'] == 2]
    for g in greens:
        for r in reds:
            if bboxes_overlap_or_adjacent(g['bbox'], r['bbox']):
                g['color'] = 2
                break
    return non_blues

def adjust_orange_to_lightblue(non_blues: List[Dict]) -> List[Dict]:
    oranges = [c for c in non_blues if c['color'] == 5]
    lightblues = [c for c in non_blues if c['color'] == 9]
    for o in oranges:
        for lb in lightblues:
            or1, oc1, or2, oc2 = o['bbox']
            lr1, lc1, lr2, lc2 = lb['bbox']
            if or1 > lr2 and or1 <= lr2 + 2 and max(oc1, lc1) <= min(oc2, lc2):
                o['color'] = 9
                break
    return non_blues

def create_filled_grid(components: List[Dict], h: int, w: int) -> List[List[int]]:
    grid = [[0] * w for _ in range(h)]
    sorted_comps = sorted(components, key=lambda c: c['size'], reverse=True)
    for c in sorted_comps:
        r1, c1, r2, c2 = c['bbox']
        color = c['color']
        for r in range(r1, r2 + 1):
            for col in range(c1, c2 + 1):
                grid[r][col] = color
    return grid

def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h, w = len(g), len(g[0])
    return [[g[r][c] for r in range(h)] for c in range(w)]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h, w = len(g), len(g[0])
    components = find_connected_components(g)
    blues = get_blue_components(components)
    non_blues = get_non_blue_components(components)
    non_blues = absorb_small_blues(non_blues, blues)
    non_blues = absorb_small_non_blues(non_blues)
    non_blues = adjust_yellow_to_pink(non_blues)
    non_blues = adjust_green_to_red(non_blues)
    non_blues = adjust_orange_to_lightblue(non_blues)
    non_blues = merge_greens(non_blues)
    non_blues = merge_pink_darkred(non_blues)
    non_blues = expand_maroon(non_blues, h, w)
    filled = create_filled_grid(non_blues, h, w)
    return transpose_grid(filled)
```