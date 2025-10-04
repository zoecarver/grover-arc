```python
from collections import Counter
from typing import List, Dict

def get_connected_components(g: List[List[int]]) -> List[Dict]:
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
                comp = {
                    'color': color,
                    'area': 0,
                    'min_r': i,
                    'max_r': i,
                    'min_c': j,
                    'max_c': j
                }
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    comp['area'] += 1
                    comp['min_r'] = min(comp['min_r'], x)
                    comp['max_r'] = max(comp['max_r'], x)
                    comp['min_c'] = min(comp['min_c'], y)
                    comp['max_c'] = max(comp['max_c'], y)
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(comp)
    return components

def get_num_non_empty(g: List[List[int]]) -> int:
    return sum(1 for row in g if any(c != 0 for c in row))

def generate_u_pattern(color: int) -> List[List[int]]:
    top = [color] * 6
    middle = [color] + [0] * 5
    bottom = [color] * 6
    return [top, middle, bottom]

def generate_h_pattern(color: int, height: int) -> List[List[int]]:
    pattern = []
    for i in range(height):
        if i % 2 == 0:
            pattern.append([color, color, color])
        else:
            pattern.append([color, 0, color])
    return pattern

def generate_mixed_pattern(g: List[List[int]], height: int, min_r: int, max_r: int, min_c: int, max_c: int) -> List[List[int]]:
    h_span = max_r - min_r + 1
    start = min_r + max(0, (h_span - height) // 2)
    result = []
    for k in range(height):
        r = start + k
        if r > max_r or r >= len(g):
            result.append([0, 0])
            continue
        sub_row = g[r][min_c:max_c + 1]
        len_sub = len(sub_row)
        half = len_sub // 2
        left_part = sub_row[:half]
        right_part = sub_row[half:]
        left_cs = [c for c in left_part if c != 0]
        right_cs = [c for c in right_part if c != 0]
        left = Counter(left_cs).most_common(1)[0][0] if left_cs else 0
        right = Counter(right_cs).most_common(1)[0][0] if right_cs else 0
        result.append([left, right])
    return result

def program(g: List[List[int]]) -> List[List[int]]:
    components = get_connected_components(g)
    main_components = [c for c in components if c['area'] > 5]
    if not main_components:
        return []
    overall_min_r = min(c['min_r'] for c in main_components)
    overall_max_r = max(c['max_r'] for c in main_components)
    overall_min_c = min(c['min_c'] for c in main_components)
    overall_max_c = max(c['max_c'] for c in main_components)
    h_span = overall_max_r - overall_min_r + 1
    w_span = overall_max_c - overall_min_c + 1
    input_size = len(g)
    num_non_empty = get_num_non_empty(g)
    calc_height = input_size - num_non_empty
    if w_span > h_span * 2:
        left_comp = min(main_components, key=lambda c: c['min_c'])
        color = left_comp['color']
        return generate_u_pattern(color)
    else:
        total_area = sum(c['area'] for c in components)
        if not components:
            return []
        areas = [c['area'] for c in components]
        dominant_area = max(areas)
        second_area = sorted(areas, reverse=True)[1] if len(areas) > 1 else 0
        if dominant_area > second_area:
            dominant_comp = max(components, key=lambda c: c['area'])
            color = dominant_comp['color']
            return generate_h_pattern(color, calc_height)
        else:
            return generate_mixed_pattern(g, calc_height, overall_min_r, overall_max_r, overall_min_c, overall_max_c)
```