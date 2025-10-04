```python
from collections import Counter
from typing import List, Tuple

def get_background(g: List[List[int]]) -> int:
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_bbox(comp: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    if not comp:
        return 0, 0, 0, 0
    rs = [p[0] for p in comp]
    cs = [p[1] for p in comp]
    return min(rs), max(rs), min(cs), max(cs)

def create_section(comp: List[Tuple[int, int]], g: List[List[int]], b: int, rows: int, cols: int) -> List[List[int]]:
    if not comp:
        return []
    min_r, max_r, min_c, max_c = get_bbox(comp)
    h = max_r - min_r + 1
    w = max_c - min_c + 1
    offset = 1 if h <= 3 else 0
    local = [[b for _ in range(w)] for _ in range(5)]
    for pr, pc in comp:
        rel_r = pr - min_r + offset
        if 0 <= rel_r < 5:
            rel_c = pc - min_c
            local[rel_r][rel_c] = g[pr][pc]
    return local

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    rows = len(g)
    cols = len(g[0])
    b = get_background(g)

    # Find all non-b connected components
    visited = set()
    non_b_comps = []
    def neighbors(r: int, c: int) -> List[Tuple[int, int]]:
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                res.append((nr, nc))
        return res

    for r in range(rows):
        for c in range(cols):
            if g[r][c] != b and (r, c) not in visited:
                comp = []
                stack = [(r, c)]
                visited.add((r, c))
                while stack:
                    cr, cc = stack.pop()
                    comp.append((cr, cc))
                    for nr, nc in neighbors(cr, cc):
                        if g[nr][nc] != b and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            stack.append((nr, nc))
                non_b_comps.append(comp)

    # Filter components with at least one b in bbox
    included_comps = []
    for comp in non_b_comps:
        min_r, max_r, min_c, max_c = get_bbox(comp)
        h = max_r - min_r + 1
        w = max_c - min_c + 1
        internal_b = sum(1 for i in range(h) for j in range(w) if g[min_r + i][min_c + j] == b)
        if internal_b > 0:
            included_comps.append(comp)

    # Sort by min_r then min_c
    included_comps.sort(key=lambda comp: (get_bbox(comp)[0], get_bbox(comp)[2]))

    # Create sections
    sections = []
    for comp in included_comps:
        section = create_section(comp, g, b, rows, cols)
        if section:
            sections.append(section)

    # Build out
    out = [[b] for _ in range(5)]  # Start with length 1, will extend
    current_w = 0
    for new_local in sections:
        if not new_local or not new_local[0]:
            continue
        w = len(new_local[0])
        start = current_w
        overlap = 0
        if current_w > 0:
            match = True
            for rr in range(1, 4):
                # Pad out[rr] if necessary
                while len(out[rr]) < start:
                    out[rr].append(b)
                if len(out[rr]) <= start - 1 or out[rr][start - 1] != new_local[rr][0]:
                    match = False
                    break
            if match:
                overlap = 1
                start -= 1

        # Place
        for rr in range(5):
            while len(out[rr]) < start + w:
                out[rr].append(b)
            for cc in range(w):
                pos = start + cc
                while len(out[rr]) < pos + 1:
                    out[rr].append(b)
                new_val = new_local[rr][cc]
                if new_val != b:
                    out[rr][pos] = new_val

        # Update current_w
        current_w = max(current_w, start + w)

    # Ensure all rows same length
    max_len = current_w
    for rr in range(5):
        while len(out[rr]) < max_len:
            out[rr].append(b)

    return out
```