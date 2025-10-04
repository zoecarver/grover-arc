```python
from collections import Counter
from typing import List

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return Counter(flat).most_common(1)[0][0]

def get_num_non_background(g: List[List[int]], b: int) -> int:
    non_b = set()
    for row in g:
        for cell in row:
            if cell != b:
                non_b.add(cell)
    return len(non_b)

def compute_threshold(h: int, num_non_b: int) -> int:
    if num_non_b > 1:
        return h // 2
    else:
        return 2

def find_separator_columns(g: List[List[int]], b: int, thresh: int) -> List[int]:
    h = len(g)
    if h == 0:
        return []
    w = len(g[0])
    seps = []
    for j in range(w):
        max_run = 0
        current_run = 0
        prev_v = None
        for i in range(h):
            v = g[i][j]
            if v != b:
                if v == prev_v:
                    current_run += 1
                else:
                    current_run = 1
                    prev_v = v
                max_run = max(max_run, current_run)
            else:
                current_run = 0
                prev_v = None
        if max_run >= thresh:
            seps.append(j)
    return seps

def compute_panel_width(w: int, seps: List[int]) -> int:
    m = len(seps)
    k = m + 1
    if k == 0:
        return w
    return (w - m) // k

def extract_first_panel(g: List[List[int]], s: int) -> List[List[int]]:
    h = len(g)
    return [row[:s] for row in g]

def program(g: List[List[int]]) -> List[List[int]]:
    b = find_background(g)
    num_non_b = get_num_non_background(g, b)
    h = len(g)
    w = len(g[0]) if h > 0 else 0
    thresh = compute_threshold(h, num_non_b)
    seps = find_separator_columns(g, b, thresh)
    s = compute_panel_width(w, seps)
    return extract_first_panel(g, s)
```