```python
from collections import Counter
from typing import List

def find_background(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    if not flat:
        return 0
    return Counter(flat).most_common(1)[0][0]

def get_num_distinct(g: List[List[int]]) -> int:
    if not g or not g[0]:
        return 0
    flat = [cell for row in g for cell in row]
    return len(set(flat))

def find_separator_columns(g: List[List[int]], b: int, h: int, distinct: int) -> List[int]:
    if not g or not g[0]:
        return []
    w = len(g[0])
    seps = []
    thresh = h // 2 if distinct > 2 else h // 5
    for j in range(w):
        non_b_count = 0
        non_b_vals = set()
        for i in range(h):
            if g[i][j] != b:
                non_b_count += 1
                non_b_vals.add(g[i][j])
        if non_b_count >= thresh and len(non_b_vals) == 1:
            seps.append(j)
    return sorted(seps)

def calculate_panel_size(w: int, seps: List[int]) -> int:
    m = len(seps)
    if m == 0:
        return w // 3
    k = m + 1
    return (w - m) // k

def extract_first_panel(g: List[List[int]], s: int) -> List[List[int]]:
    if not g or s <= 0:
        return []
    h = len(g)
    output = []
    for row in g:
        panel_row = row[:s]
        output.append(panel_row)
    return output

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    h = len(g)
    w = len(g[0])
    b = find_background(g)
    distinct = get_num_distinct(g)
    seps = find_separator_columns(g, b, h, distinct)
    s = calculate_panel_size(w, seps)
    return extract_first_panel(g, s)
```