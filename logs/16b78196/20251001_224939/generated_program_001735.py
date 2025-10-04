```python
from typing import List
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    n = 30

    def get_components():
        visited = [False] * (n * n)
        components = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for i in range(n * n):
            r = i // n
            c = i % n
            if g[r][c] != 0 and not visited[i]:
                color = g[r][c]
                stack = [i]
                visited[i] = True
                positions = []
                min_r = max_r = r
                min_c = max_c = c
                while stack:
                    curr = stack.pop()
                    cr = curr // n
                    cc = curr % n
                    positions.append((cr, cc))
                    min_r = min(min_r, cr)
                    max_r = max(max_r, cr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in directions:
                        nr = cr + dr
                        nc = cc + dc
                        if 0 <= nr < n and 0 <= nc < n:
                            ni = nr * n + nc
                            if not visited[ni] and g[nr][nc] == color:
                                visited[ni] = True
                                stack.append(ni)
                components.append({
                    'color': color,
                    'positions': positions,
                    'bbox': (min_r, max_r, min_c, max_c),
                    'pixels': len(positions)
                })
        return components

    components = get_components()
    if not components:
        return [[0] * n for _ in range(n)]

    base = max(components, key=lambda x: x['pixels'])

    output = [[0] * n for _ in range(n)]

    # Place base
    for r, c in base['positions']:
        output[r][c] = base['color']

    # Small components
    small = [c for c in components if id(c) != id(base)]

    # Group by width
    groups = defaultdict(list)
    for c in small:
        min_r, max_r, min_c, max_c = c['bbox']
        w = max_c - min_c + 1
        groups[w].append(c)

    # Sort each group: min_r ascending, then min_c descending
    for w in groups:
        groups[w].sort(key=lambda c: (c['bbox'][0], -c['bbox'][2]))

    # Base bbox
    b_min_r, b_max_r, b_min_c, b_max_c = base['bbox']
    b_h = b_max_r - b_min_r + 1
    b_w = b_max_c - b_min_c + 1
    is_vertical = b_h > b_w

    # Sorted widths descending for placement order
    sorted_widths = sorted(groups.keys(), reverse=True)

    if is_vertical:
        # Place stacks to the left of base, stacked vertically from top
        max_w = max(sorted_widths) if sorted_widths else 0
        x_start_base = b_min_c
        current_y = b_min_r
        sx = x_start_base - max_w
        for w in sorted_widths:
            group = groups[w]
            for shape in group:
                min_r_shape, max_r_shape, min_c_shape, max_c_shape = shape['bbox']
                h = max_r_shape - min_r_shape + 1
                sy = current_y
                for pr, pc in shape['positions']:
                    rel_r = pr - min_r_shape
                    rel_c = pc - min_c_shape
                    gr = sy + rel_r
                    gc = sx + rel_c
                    if 0 <= gr < n and 0 <= gc < n and output[gr][gc] == 0:
                        output[gr][gc] = shape['color']
                current_y += h
    else:
        # Place stacks below base, stacked horizontally from left, vertically within group
        y_start_base = b_max_r + 1
        current_x = b_min_c
        for w in sorted_widths:
            group = groups[w]
            sy = y_start_base
            sx = current_x
            for shape in group:
                min_r_shape, max_r_shape, min_c_shape, max_c_shape = shape['bbox']
                h = max_r_shape - min_r_shape + 1
                for pr, pc in shape['positions']:
                    rel_r = pr - min_r_shape
                    rel_c = pc - min_c_shape
                    gr = sy + rel_r
                    gc = sx + rel_c
                    if 0 <= gr < n and 0 <= gc < n and output[gr][gc] == 0:
                        output[gr][gc] = shape['color']
                sy += h
            current_x += w

    return output
```