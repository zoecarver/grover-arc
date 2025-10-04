```python
from collections import Counter
from typing import List

def get_m_s(w: int) -> tuple[int, int]:
    if w <= 1:
        return 0, 0
    m = (w - 1) // 6
    num_b = m + 1
    s = (w - num_b) // m if m > 0 else 0
    return m, s

def extract_panels(row: List[int], m: int, s: int) -> List[List[int]]:
    border_pos = [i * (s + 1) for i in range(m + 1)]
    panels = []
    for k in range(m):
        start = border_pos[k] + 1
        end = start + s
        panels.append(row[start:end])
    return panels

def get_minority(vals: List[int]) -> int:
    if not vals:
        return 0
    freq = Counter(vals)
    min_c = min(freq.values())
    candidates = [c for c, cnt in freq.items() if cnt == min_c]
    return min(candidates)

def compress_row(row: List[int], m: int, s: int) -> List[int]:
    if not row:
        return []
    left_f = row[0]
    right_f = row[-1]
    if s == 0:
        return [left_f]
    panels = extract_panels(row, m, s)
    inner = []
    for j in range(s):
        vals = [p[j] for p in panels]
        inner.append(get_minority(vals))
    return [left_f] + inner + [right_f]

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    h = len(g)
    w = len(g[0])
    m, s = get_m_s(w)
    output = []
    for i in range(min(h, w)):
        output.append(compress_row(g[i], m, s))
    return output
```