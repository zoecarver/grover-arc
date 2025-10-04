```python
from typing import List, Tuple, Dict
from collections import deque
import copy

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h, w = get_size(g)
    components = find_connected_components(g)
    components = handle_small_blue_interaction(components, h, w)
    components = handle_small_non_blue_interaction(components, h, w)
    components = handle_color_adjustments(components, h, w)
    components = merge_similar_colors(components, 6, 7)
    components = handle_green_merge(components, h, w)
    components = handle_maroon_expansion(components, h, w)
    filled = create_filled_grid(components, h, w)
    return transpose_grid(filled)

def get_size(g: List[List[int]]) -> Tuple[int, int]:
    if not g:
        return 0, 0
    return len(g), len(g[0])

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

def bboxes_overlap(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1, c1, r2, c2 = b1
    r3, c3, r4, c4 = b2
    return max(r1, r3) <= min(r2, r4) and max(c1, c3) <= min(c2, c4)

def bboxes_adjacent(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1, c1, r2, c2 = b1
    r3, c3, r4, c4 = b2
    # Vertical adjacent (touching)
    if min(r2, r4) == max(r1, r3) + 1 and max(c1, c3) <= min(c2, c4) and min(c1, c3) <= max(c2, c4):
        return True
    # Horizontal adjacent (touching)
    if min(c2, c4) == max(c1, c3) + 1 and max(r1, r3) <= min(r2, r4) and min(r1, r3) <= max(r2, r4):
        return True
    return False

def bboxes_adjacent_or_overlap(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    return bboxes_overlap(b1, b2) or bboxes_adjacent(b1, b2)

def handle_small_blue_interaction(components: List[Dict], h: int, w: int) -> List[Dict]:
    blues = [c for c in components if c['color'] == 1 and c['size'] <= 4]
    non_blues = [c for c in components if c['color'] != 1]
    updated_non_blues = [copy.deepcopy(c) for c in non_blues]
    for blue in blues:
        candidates = [(nb['size'], idx, nb) for idx, nb in enumerate(updated_non_blues) if bboxes_adjacent_or_overlap(blue['bbox'], nb['bbox'])]
        if candidates:
            _, idx, absorber = max(candidates)
            r1 = min(blue['bbox'][0], absorber['bbox'][0])
            c1 = min(blue['bbox'][1], absorber['bbox'][1])
            r2 = max(blue['bbox'][2], absorber['bbox'][2])
            c2 = max(blue['bbox'][3], absorber['bbox'][3])
            absorber['bbox'] = (r1, c1, r2, c2)
            absorber['size'] += blue['size']
    return updated_non_blues

def handle_small_non_blue_interaction(components: List[Dict], h: int, w: int) -> List[Dict]:
    small_non = [c for c in components if c['color'] != 1 and c['color'] != 0 and c['size'] <= 4 and c['color'] not in (3, 8, 9)]
    large = [c for c in components if c['color'] != 1 and c['color'] != 0 and (c['size'] > 4 or c['color'] in (3, 8, 9))]
    updated_large = [copy.deepcopy(c) for c in large]
    for small in small_non:
        candidates = [(l['size'], idx, l) for idx, l in enumerate(updated_large) if bboxes_adjacent_or_overlap(small['bbox'], l['bbox'])]
        if candidates:
            _, idx, absorber = max(candidates)
            r1 = min(small['bbox'][0], absorber['bbox'][0])
            c1 = min(small['bbox'][1], absorber['bbox'][1])
            r2 = max(small['bbox'][2], absorber['bbox'][2])
            c2 = max(small['bbox'][3], absorber['bbox'][3])
            absorber['bbox'] = (r1, c1, r2, c2)
            absorber['size'] += small['size']
    return updated_large

def handle_color_adjustments(components: List[Dict], h: int, w: int) -> List[Dict]:
    updated = [copy.deepcopy(c) for c in components]
    # Yellow (4) to pink (6) if directly below adjacent
    for i, y in enumerate([c for c in updated if c['color'] == 4]):
        for p in [c for c in updated if c['color'] == 6]:
            if bboxes_adjacent(y['bbox'], p['bbox']) and y['bbox'][0] == p['bbox'][2] + 1 and max(y['bbox'][1], p['bbox'][1]) <= min(y['bbox'][3], p['bbox'][3]):
                y['color'] = 6
                r1 = min(y['bbox'][0], p['bbox'][0])
                c1 = min(y['bbox'][1], p['bbox'][1])
                r2 = max(y['bbox'][2], p['bbox'][2])
                c2 = max(y['bbox'][3], p['bbox'][3])
                p['bbox'] = (r1, c1, r2, c2)
                p['size'] += y['size']
                break
    # Green (3) to red (2) if adjacent
    for g in [c for c in updated if c['color'] == 3]:
        for r in [c for c in updated if c['color'] == 2]:
            if bboxes_adjacent_or_overlap(g['bbox'], r['bbox']):
                g['color'] = 2
                r1 = min(g['bbox'][0], r['bbox'][0])
                c1 = min(g['bbox'][1], r['bbox'][1])
                r2 = max(g['bbox'][2], r['bbox'][2])
                c2 = max(g['bbox'][3], r['bbox'][3])
                r['bbox'] = (r1, c1, r2, c2)
                r['size'] += g['size']
                g['color'] = 0  # mark deleted
                break
    # Orange (5) to light blue (9) if below within 2 rows with overlap
    for o in [c for c in updated if c['color'] == 5]:
        for lb in [c for c in updated if c['color'] == 9]:
            if o['bbox'][0] > lb['bbox'][2] and o['bbox'][0] <= lb['bbox'][2] + 2 and max(o['bbox'][1], lb['bbox'][1]) <= min(o['bbox'][3], lb['bbox'][3]):
                o['color'] = 9
                r1 = min(o['bbox'][0], lb['bbox'][0])
                c1 = min(o['bbox'][1], lb['bbox'][1])
                r2 = max(o['bbox'][2], lb['bbox'][2])
                c2 = max(o['bbox'][3], lb['bbox'][3])
                lb['bbox'] = (r1, c1, r2, c2)
                lb['size'] += o['size']
                o['color'] = 0
                break
    return [c for c in updated if c['color'] != 0]

def merge_similar_colors(components: List[Dict], color1: int, color2: int) -> List[Dict]:
    updated = [copy.deepcopy(c) for c in components]
    changed = True
    while changed:
        changed = False
        i = 0
        while i < len(updated):
            c = updated[i]
            if c['color'] == color1 or c['color'] == color2:
                target_color = color2 if c['color'] == color1 else color1
                candidates = [(d['size'], j, d) for j, d in enumerate(updated) if j > i and d['color'] == target_color and bboxes_adjacent_or_overlap(c['bbox'], d['bbox'])]
                for _, j, cand in sorted(candidates):
                    if cand['size'] < c['size']:
                        r1 = min(c['bbox'][0], cand['bbox'][0])
                        c1 = min(c['bbox'][1], cand['bbox'][1])
                        r2 = max(c['bbox'][2], cand['bbox'][2])
                        c2 = max(c['bbox'][3], cand['bbox'][3])
                        c['bbox'] = (r1, c1, r2, c2)
                        c['size'] += cand['size']
                        del updated[j]
                        changed = True
                        break
            if changed:
                i = max(0, i - 1)
            else:
                i += 1
    return updated

def handle_green_merge(components: List[Dict], h: int, w: int) -> List[Dict]:
    greens = [c for c in components if c['color'] == 3]
    if not greens:
        return components
    min_r = min(g['bbox'][0] for g in greens)
    min_c = min(g['bbox'][1] for g in greens)
    max_r = max(g['bbox'][2] for g in greens)
    max_c = max(g['bbox'][3] for g in greens)
    total_size = sum(g['size'] for g in greens)
    big_green = {
        'color': 3,
        'bbox': (min_r, min_c, max_r, max_c),
        'size': total_size
    }
    updated = [c for c in components if c['color'] != 3]
    updated.append(big_green)
    return updated

def handle_maroon_expansion(components: List[Dict], h: int, w: int) -> List[Dict]:
    updated = []
    for c in components:
        if c['color'] == 8:
            r1, c1, r2, c2 = c['bbox']
            new_r1 = max(0, r1 - 1)
            new_r2 = min(h - 1, r2 + 1)
            c['bbox'] = (new_r1, c1, new_r2, c2)
        updated.append(copy.deepcopy(c))
    return updated

def create_filled_grid(components: List[Dict], h: int, w: int) -> List[List[int]]:
    grid = [[0] * w for _ in range(h)]
    sorted_comps = sorted(components, key=lambda c: c['size'], reverse=True)
    for c in sorted_comps:
        r1, c1, r2, c2 = c['bbox']
        color = c['color']
        for r in range(max(0, r1), min(h, r2 + 1)):
            for col in range(max(0, c1), min(w, c2 + 1)):
                grid[r][col] = color
    return grid

def transpose_grid(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h, w = len(g), len(g[0])
    return [[g[r][c] for r in range(h)] for c in range(w)]
```