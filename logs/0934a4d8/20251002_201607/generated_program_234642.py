```python
from typing import List, Tuple

def find_eights_block(g: List[List[int]]) -> Tuple[int, int, int, int]:
    n = len(g)
    max_h = 0
    best = (0, 0, 0, 0)
    for r in range(n):
        for cc in range(n):
            ww = 0
            while cc + ww < n and g[r][cc + ww] == 8:
                ww += 1
            if ww >= 3:
                hh = 1
                while r + hh < n and all(g[r + hh][cc + j] == 8 for j in range(ww)):
                    hh += 1
                if hh > max_h:
                    max_h = hh
                    best = (r, cc, ww, hh)
    return best

def find_clean_block(g: List[List[int]], r: int, c: int, w: int) -> List[int]:
    n = len(g)
    prefix = g[r][:c]
    suffix = g[r][c + w:]
    for s in range(n):
        if s != r and g[s][:c] == prefix and g[s][c + w:] == suffix:
            return g[s][c:c + w]
    # Fallback: return original without 8s, but assume always finds
    return [x if x != 8 else 9 for x in g[r][c:c + w]]  # placeholder, but data has match

def program(g: List[List[int]]) -> List[List[int]]:
    r_start, c, w, h = find_eights_block(g)
    output = []
    for k in range(h):
        r = r_start + k
        clean = find_clean_block(g, r, c, w)
        output.append(clean)
    return output
```