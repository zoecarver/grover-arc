```python
from typing import List, Tuple, Set
from collections import Counter, deque

def get_component(g: List[List[int]], start_r: int, start_c: int, bg: int, height: int, width: int) -> Set[Tuple[int, int]]:
    """Find the connected component of non-background cells starting from (start_r, start_c) using 4-connectivity."""
    queue = deque([(start_r, start_c)])
    visited = set([(start_r, start_c)])
    component = set()
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while queue:
        r, c = queue.popleft()
        component.add((r, c))
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and g[nr][nc] != bg and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return component

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    if h == 0:
        return g
    w = len(g[0])
    flat = [cell for row in g for cell in row]
    count = Counter(flat)
    if not count:
        return g
    bg = count.most_common(1)[0][0]
    specials = [k for k in count if k != bg and 0 < count[k] <= 4]
    specials.sort(key=lambda k: (count[k], k))
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    is_horizontal = h > w
    current_target = None
    for s in specials:
        s_pos_set = {(r, c) for r in range(h) for c in range(w) if g[r][c] == s}
        if not s_pos_set:
            continue
        visited = set()
        components: List[Set[Tuple[int, int]]] = []
        s_cells_per_comp: List[List[Tuple[int, int]]] = []
        for r, c in list(s_pos_set):
            if (r, c) in visited:
                continue
            comp = get_component(g, r, c, bg, h, w)
            visited.update(comp)
            s_in_comp = [(rr, cc) for rr, cc in comp if g[rr][cc] == s]
            components.append(comp)
            s_cells_per_comp.append(s_in_comp)
        single_comps_indices = [i for i in range(len(components)) if len(components[i]) == 1]
        num_singles = len(single_comps_indices)
        if num_singles == 0:
            if current_target is None:
                target = w // 2 if is_horizontal else h // 2
                current_target = target
            else:
                target = current_target
        else:
            single_pos = [list(components[i])[0] for i in single_comps_indices]
            if is_horizontal:
                anchor = min(single_pos, key=lambda p: (p[0], p[1]))
                target = anchor[1]
            else:
                anchor = min(single_pos, key=lambda p: (p[1], p[0]))
                target = anchor[0]
            current_target = target
        for i in range(len(components)):
            comp = components[i]
            s_in = s_cells_per_comp[i]
            if not s_in:
                continue
            if is_horizontal:
                ref = min(s_in, key=lambda p: p[1])
                varying = ref[1]
                shift_v = target - varying
                dx = shift_v
                dy = 0
            else:
                ref = min(s_in, key=lambda p: p[0])
                varying = ref[0]
                shift_v = target - varying
                dy = shift_v
                dx = 0
                if num_singles > 0 and len(comp) > 1 and ref[0] < target:
                    dx -= 1
            old_cells = {p: g[p[0]][p[1]] for p in comp}
            for p in comp:
                g[p[0]][p[1]] = bg
            for (r, c), val in old_cells.items():
                nr = r + dy
                nc = c + dx
                if 0 <= nr < h and 0 <= nc < w:
                    g[nr][nc] = val
    return g
```