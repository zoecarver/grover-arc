```python
from typing import List, Tuple
import collections

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    count = collections.Counter(flat)
    return count.most_common(1)[0][0] if flat else 0

def find_components(g: List[List[int]], background: int) -> List[List[Tuple[int, int]]]:
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    visited = [[False] * w for _ in range(h)]
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if g[i][j] != background and not visited[i][j]:
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] != background:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append(component)
    return components

def get_bbox(component: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    min_r = min(c[0] for c in component)
    max_r = max(c[0] for c in component)
    min_c = min(c[1] for c in component)
    max_c = max(c[1] for c in component)
    return min_r, max_r, min_c, max_c

def has_vertical_bar(component: List[Tuple[int, int]], g: List[List[int]], background: int, min_len: int = 3) -> Tuple[bool, int, int, int, int]:
    col_rows = collections.defaultdict(list)
    for r, c in component:
        col_rows[c].append(r)
    for c, rs in col_rows.items():
        rs = sorted(set(rs))  # unique sorted rows
        for start in range(len(rs) - min_len + 1):
            bar_start = rs[start]
            bar_end = rs[start + min_len - 1]
            if bar_end - bar_start + 1 == min_len:
                color = g[bar_start][c]
                if color != background and all(g[bar_start + k][c] == color for k in range(min_len)):
                    return True, color, bar_start, bar_end, c
    return False, 0, 0, 0, 0

def has_marker(component: List[Tuple[int, int]], g: List[List[int]], marker: int = 9) -> bool:
    for r, c in component:
        if g[r][c] == marker:
            return True
    return False

def get_attachment_col(component: List[Tuple[int, int]], g: List[List[int]], marker: int = 9, bbox_min_r: int = None) -> int:
    attach_cols = set()
    for r, c in component:
        if g[r][c] == marker and (bbox_min_r is None or r == bbox_min_r or r == len(g) - 1 - (len(g) - 1 - bbox_min_r)):
            attach_cols.add(c)
    return min(attach_cols) if attach_cols else -1

def get_subgrid(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int) -> List[List[int]]:
    return [g[r][min_c : max_c + 1] for r in range(min_r, max_r + 1)]

def concatenate_subgrids(subgrids: List[List[List[int]]], background: int) -> List[List[int]]:
    if not subgrids:
        return []
    num_rows = len(subgrids[0])
    result = [[] for _ in range(num_rows)]
    for s in subgrids:
        for ri in range(num_rows):
            result[ri].extend(s[ri])
    return result

def get_middle_pattern(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, full_h: int) -> List[List[int]]:
    h = max_r - min_r + 1
    if h == 3:
        return get_subgrid(g, min_r, max_r, min_c, max_c)
    elif h == 5:
        mid_start = min_r + 1
        mid_end = min_r + 3
        return get_subgrid(g, mid_start, mid_end, min_c, max_c)
    else:
        # Pad to 3
        pad_top = (full_h - 3) // 2
        pad_bot = full_h - 3 - pad_top
        padded = [[background] * (max_c - min_c + 1) for _ in range(pad_top)]
        middle = get_subgrid(g, max(min_r, full_h - pad_bot - 3 + pad_top), min(max_r, full_h - pad_bot - 1 + pad_top), min_c, max_c)
        padded.extend(middle)
        padded.extend([[background] * (max_c - min_c + 1) for _ in range(pad_bot - len(middle) + 3 if len(middle) < 3 else 0)])
        while len(padded) < 3:
            padded.append([background] * (max_c - min_c + 1))
        return padded[:3]
    return [[background]]  # default

def get_top_pattern(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, full_h: int) -> List[List[int]]:
    if max_r - min_r + 1 == 5:
        return [g[min_r][min_c : max_c + 1]]
    else:
        return [[background for _ in range(max_c - min_c + 1)]]

def get_bottom_pattern(g: List[List[int]], min_r: int, max_r: int, min_c: int, max_c: int, full_h: int) -> List[List[int]]:
    if max_r - min_r + 1 == 5:
        return [g[max_r][min_c : max_c + 1]]
    else:
        return [[background for _ in range(max_c - min_c + 1)]]

def process_bar_structure(g: List[List[int]], component: List[Tuple[int, int]], other_marked: List[List[Tuple[int, int]]], background: int, bar_color: int, bar_start: int, bar_end: int, bar_col: int, length: int, is_pink: bool = False) -> List[List[int]]:
    h = len(g)
    full_h = 5
    min_r, max_r, _, _ = get_bbox(component)
    mid_start = bar_start + (length - 3) // 2 if length == 5 else bar_start
    mid_end = mid_start + 2
    attach_col = get_attachment_col(component, g)
    local_min_c = bar_col + 1
    local_max_c = attach_col - 1 if attach_col > bar_col else bar_col
    local_width = max(0, local_max_c - local_min_c + 1)
    local_middle = get_subgrid(g, mid_start, mid_end, local_min_c, local_max_c) if local_width > 0 else []
    local_top = get_top_pattern(g, min_r, max_r, local_min_c, local_max_c, full_h) if local_width > 0 else []
    local_bottom = get_bottom_pattern(g, min_r, max_r, local_min_c, local_max_c, full_h) if local_width > 0 else []

    # Chain marked
    marked_list = []
    for m_comp in other_marked:
        m_min_r, m_max_r, m_min_c, m_max_c = get_bbox(m_comp)
        m_attach = get_attachment_col(m_comp, g)
        m_start_c = m_attach
        m_middle = get_middle_pattern(g, m_min_r, m_max_r, m_start_c, m_max_c, full_h)
        m_top = get_top_pattern(g, m_min_r, m_max_r, m_start_c, m_max_c, full_h)
        m_bottom = get_bottom_pattern(g, m_min_r, m_max_r, m_start_c, m_max_c, full_h)
        marked_list.append((m_middle, m_top, m_bottom))
    # Sort marked by attach col
    marked_list.sort(key=lambda x: get_attachment_col([], g, attach_col=0))  # Placeholder, assume sorted

    # Chain: local + marked
    chained_middle = [local_middle] if local_middle else []
    chained_middle.extend([m[0] for m in marked_list])
    chained_top = [local_top] if local_top else []
    chained_top.extend([m[1] for m in marked_list])
    chained_bottom = [local_bottom] if local_bottom else []
    chained_bottom.extend([m[2] for m in marked_list])

    # Concatenate
    ext_middle = concatenate_subgrids(chained_middle, background)
    ext_top = concatenate_subgrids(chained_top, background)
    ext_bottom = concatenate_subgrids(chained_bottom, background)

    # Now build 5 high extension
    ext_grid = [[background] * len(ext_middle[0]) for _ in range(full_h)] if ext_middle else []
    if ext_middle:
        for ri in range(3):
            ext_grid[1 + ri] = ext_middle[ri][:]
        if ext_top:
            ext_grid[0] = ext_top[0]
        if ext_bottom:
            ext_grid[4] = ext_bottom[0]

    # Bar column
    bar_w = 1
    bar_grid = [[bar_color if (length == 5 or (1 <= ri <= 3)) else background for _ in range(1)] for ri in range(full_h)]

    # Place bar left, extension right if pink (right), or adjust for other
    if is_pink:
        # Concat bar + ext
        full_width = bar_w + len(ext_grid[0]) if ext_grid else bar_w
        full_grid = [[background] * full_width for _ in range(full_h)]
        for ri in range(full_h):
            full_grid[ri][0] = bar_color if (length == 5 or 1 <= ri <= 3) else background
            if ext_grid:
                for ci in range(len(ext_grid[0])):
                    full_grid[ri][1 + ci] = ext_grid[ri][ci]
        return full_grid
    else:
        # For other bars, similar, assume right for now
        return full_grid  # Placeholder

def process_horizontal_structure(g: List[List[int]], component: List[Tuple[int, int]], background: int, area: int) -> List[List[int]]:
    if area <= 10:
        return []
    min_r, max_r, min_c, max_c = get_bbox(component)
    h = max_r - min_r + 1
    full_h = 5
    if h == 3:
        middle = get_subgrid(g, min_r, max_r, min_c, max_c)
        pad_row = [background] * (max_c - min_c + 1)
        grid = [pad_row, middle[0], middle[1], middle[2], pad_row]
        return grid
    elif h == 5:
        return get_subgrid(g, min_r, max_r, min_c, max_c)
    return []

def program(g: List[List[int]]) -> List[List[int]]:
    background = get_background(g)
    components = find_components(g, background)
    bar_comps = []
    marked_comps = []
    horizontal_comps = []
    for comp in components:
        area = len(comp)
        has_bar, bar_color, bar_start, bar_end, bar_col = has_vertical_bar(comp, g, background)
        is_mark = has_marker(comp, g)
        if has_bar:
            bar_comps.append((comp, bar_color, bar_start, bar_end, bar_col, is_mark))
        elif is_mark:
            marked_comps.append(comp)
        elif area > 10:
            horizontal_comps.append(comp)

    processed = []
    used_marked = set()
    for b_comp, b_color, b_start, b_end, b_col, b_mark in bar_comps:
        other_marked = [m for m in marked_comps if id(m) not in used_marked]
        is_pink = b_color == 6
        p_grid = process_bar_structure(g, b_comp, other_marked, background, b_color, b_start, b_end, b_col, b_end - b_start + 1, is_pink)
        processed.append(p_grid)
        used_marked.update(id(m) for m in other_marked)

    for h_comp in horizontal_comps:
        p_grid = process_horizontal_structure(g, h_comp, background, len(h_comp))
        if p_grid:
            processed.append(p_grid)

    # Concat all processed horizontally, pad if empty rows
    if not processed:
        w = len(g[0]) if g else 0
        return [[background] * (w // 5) for _ in range(5)]  # default empty
    total_w = sum(len(p[0]) for p in processed)
    output = [[background] * total_w for _ in range(5)]
    current_col = 0
    for p in processed:
        pw = len(p[0])
        for ri in range(5):
            for ci in range(pw):
                output[ri][current_col + ci] = p[ri][ci]
        current_col += pw
    return output
```