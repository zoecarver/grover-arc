```python
from typing import List

def find_noise_params(g: List[List[int]]) -> tuple[int, int, int, int]:
    n = len(g)
    start = next((i for i in range(n) if 8 in g[i]), None)
    if start is None:
        raise ValueError("No noise block found")
    end = start + 1
    while end < n and 8 in g[end]:
        end += 1
    h = end - start
    row = g[start]
    m = len(row)
    s = next((j for j in range(m) if row[j] == 8), None)
    if s is None:
        raise ValueError("No 8s in noise row")
    ww = 0
    while s + ww < m and row[s + ww] == 8:
        ww += 1
    w = ww
    return start, h, s, w

def extract_missing_segment(g: List[List[int]], nr: int, s: int, w: int, noise_set: set[int]) -> List[int]:
    prefix = g[nr][:s]
    suffix_start = s + w
    suffix = g[nr][suffix_start:]
    n = len(g)
    for k in range(n):
        if k in noise_set:
            continue
        if g[k][:s] == prefix and g[k][suffix_start:] == suffix:
            return g[k][s:s + w]
    raise ValueError(f"No matching clean row found for noise row {nr}")

def program(g: List[List[int]]) -> List[List[int]]:
    start, h, s, w = find_noise_params(g)
    noise_set = set(range(start, start + h))
    output = []
    for i in range(h):
        nr = start + i
        segment = extract_missing_segment(g, nr, s, w, noise_set)
        output.append(segment)
    return output
```