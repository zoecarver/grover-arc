```python
from typing import List, Tuple, Dict
from collections import deque
import copy

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return g
    h, w = len(g), len(g[0])
    components = find_connected_components(g, h, w)
    components = handle_four_to_six(components, h, w)
    components = handle_five_to_nine(components, h, w)
    components = merge_six_and_seven(components, h, w)
    components = absorb_small_components(components, h, w)
    components = merge_all_greens(components, h, w)
    components = expand_maroon(components, h, w)
    return create_filled_grid(components, h, w)

def find_connected_components(g: List[List[int]], h: int, w: int) -> List[Dict]:
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != 0 and g[i][j] != 1 and not visited[i][j]:
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

def bboxes_adjacent_or_overlap(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> bool:
    r1, c1, r2, c2 = b1
    r3, c3, r4, c4 = b2
    # Overlap
    if max(r1, r3) <= min(r2, r4) and max(c1, c3) <= min(c2, c4):
        return True
    # Vertical adjacency with gap <=1
    dr = max(0, max(r1 - r4, r3 - r2))
    if dr <= 1 and max(c1, c3) <= min(c2, c4):
        return True
    # Horizontal adjacency with gap <=1
    dc = max(0, max(c1 - c4, c3 - c2))
    if dc <= 1 and max(r1, r3) <= min(r2, r4):
        return True
    return False

def handle_four_to_six(components: List[Dict], h: int, w: int) -> List[Dict]:
    new_components = []
    i = 0
    while i < len(components):
        comp = components[i]
        if comp['color'] == 4:
            merged = False
            j = 0
            while j < len(components):
                other = components[j]
                if other['color'] == 6:
                    r1, c1, r2, c2 = comp['bbox']
                    o_r1, o_c1, o_r2, o_c2 = other['bbox']
                    # Below: min_r of 4 == max_r of 6 + 1, col overlap
                    if r1 == o_r2 + 1 and max(c1, o_c1) <= min(c2, o_c2):
                        # Change 4 to 6, merge into 6
                        other['bbox'] = (
                            min(o_r1, r1), min(o_c1, c1), max(o_r2, r2), max(o_c2, c2)
                        )
                        other['size'] += comp['size']
                        merged = True
                        break
                j += 1
            if merged:
                del components[i]
                continue
        new_components.append(comp)
        i += 1
    return new_components

def handle_five_to_nine(components: List[Dict], h: int, w: int) -> List[Dict]:
    new_components = []
    i = 0
    while i < len(components):
        comp = components[i]
        if comp['color'] == 5:
            merged = False
            j = 0
            while j < len(components):
                other = components[j]
                if other['color'] == 9:
                    r1, c1, r2, c2 = comp['bbox']
                    o_r1, o_c1, o_r2, o_c2 = other['bbox']
                    # Below with dist 1 or 2: r1 == o_r2 +1 or +2, col overlap
                    dist = r1 - o_r2
                    if dist == 1 or dist == 2 and max(c1, o_c1) <= min(c2, o_c2):
                        # Change 5 to 9, merge into 9
                        other['bbox'] = (
                            min(o_r1, r1), min(o_c1, c1), max(o_r2, r2), max(o_c2, c2)
                        )
                        other['size'] += comp['size']
                        merged = True
                        break
                j += 1
            if merged:
                del components[i]
                continue
        new_components.append(comp)
        i += 1
    return new_components

def merge_six_and_seven(components: List[Dict], h: int, w: int) -> List[Dict]:
    changed = True
    while changed:
        changed = False
        new_components = []
        i = 0
        while i < len(components):
            comp = components[i]
            if comp['color'] in (6, 7):
                merged = False
                j = 0
                while j < len(components):
                    if i == j:
                        j += 1
                        continue
                    other = components[j]
                    if other['color'] in (6, 7) and bboxes_adjacent_or_overlap(comp['bbox'], other['bbox']):
                        # Merge smaller into larger, or by max_c if tie
                        if comp['size'] > other['size'] or (comp['size'] == other['size'] and comp['bbox'][3] > other['bbox'][3]):
                            target = comp
                            source = other
                        else:
                            target = other
                            source = comp
                        # Color of the one with larger max_c
                        if target['bbox'][3] >= source['bbox'][3]:
                            union_color = target['color']
                        else:
                            union_color = source['color']
                        target['bbox'] = (
                            min(target['bbox'][0], source['bbox'][0]),
                            min(target['bbox'][1], source['bbox'][1]),
                            max(target['bbox'][2], source['bbox'][2]),
                            max(target['bbox'][3], source['bbox'][3])
                        )
                        target['size'] += source['size']
                        target['color'] = union_color
                        merged = True
                        del components[j]
                        if target is comp:
                            continue  # Don't add yet, continue checking for comp
                        else:
                            # comp was source, skip adding it
                            i -= 1
                        break
                    j += 1
                if merged:
                    changed = True
                    i += 1
                    continue
            new_components.append(comp)
            i += 1
        components = new_components
    return components

def absorb_small_components(components: List[Dict], h: int, w: int) -> List[Dict]:
    changed = True
    while changed:
        changed = False
        new_components = []
        i = 0
        while i < len(components):
            comp = components[i]
            if comp['size'] <= 4 and comp['color'] not in (0, 3, 8, 9):
                absorbed = False
                j = 0
                candidates = []
                while j < len(components):
                    if i != j and bboxes_adjacent_or_overlap(comp['bbox'], components[j]['bbox']):
                        candidates.append(components[j])
                    j += 1
                if candidates:
                    # Absorb into largest
                    target = max(candidates, key=lambda x: x['size'])
                    target['bbox'] = (
                        min(target['bbox'][0], comp['bbox'][0]),
                        min(target['bbox'][1], comp['bbox'][1]),
                        max(target['bbox'][2], comp['bbox'][2]),
                        max(target['bbox'][3], comp['bbox'][3])
                    )
                    target['size'] += comp['size']
                    absorbed = True
                    changed = True
                    del components[i]
                    continue
            new_components.append(comp)
            i += 1
        components = new_components
    return components

def merge_all_greens(components: List[Dict], h: int, w: int) -> List[Dict]:
    greens = [c for c in components if c['color'] == 3]
    if len(greens) <= 1:
        return components
    # Union all greens
    union_min_r = min(c['bbox'][0] for c in greens)
    union_min_c = min(c['bbox'][1] for c in greens)
    union_max_r = max(c['bbox'][2] for c in greens)
    union_max_c = max(c['bbox'][3] for c in greens)
    union_size = sum(c['size'] for c in greens)
    union_green = {
        'color': 3,
        'bbox': (union_min_r, union_min_c, union_max_r, union_max_c),
        'size': union_size
    }
    # Remove all greens, add union
    new_components = [c for c in components if c['color'] != 3]
    new_components.append(union_green)
    return new_components

def expand_maroon(components: List[Dict], h: int, w: int) -> List[Dict]:
    new_components = []
    for comp in components:
        if comp['color'] == 8:
            r1, c1, r2, c2 = comp['bbox']
            new_r1 = max(0, r1 - 1)
            new_r2 = min(h - 1, r2 + 1)
            new_size = (new_r2 - new_r1 + 1) * (c2 - c1 + 1)
            comp['bbox'] = (new_r1, c1, new_r2, c2)
            comp['size'] = new_size
        new_components.append(comp)
    return new_components

def create_filled_grid(components: List[Dict], h: int, w: int) -> List[List[int]]:
    grid = [[0] * w for _ in range(h)]
    # Sort by size descending
    sorted_comps = sorted(components, key=lambda c: c['size'], reverse=True)
    for comp in sorted_comps:
        r1, c1, r2, c2 = comp['bbox']
        color = comp['color']
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if 0 <= r < h and 0 <= c < w:
                    grid[r][c] = color
    return grid
```