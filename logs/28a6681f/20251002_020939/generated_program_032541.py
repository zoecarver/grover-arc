```python
from typing import List
from copy import deepcopy

class UF:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        px = self.find(x)
        py = self.find(y)
        if px != py:
            self.parent[px] = py

def build_components(g: List[List[int]]) -> dict:
    components = {}
    all_fixed = set()
    for row in g:
        for val in row:
            if val > 1:
                all_fixed.add(val)
    for C in all_fixed:
        uf = UF(100)
        for r in range(10):
            for c in range(10):
                if g[r][c] == C:
                    pos = r * 10 + c
                    if r > 0 and g[r - 1][c] == C:
                        uf.union(pos, (r - 1) * 10 + c)
                    if r < 9 and g[r + 1][c] == C:
                        uf.union(pos, (r + 1) * 10 + c)
                    if c > 0 and g[r][c - 1] == C:
                        uf.union(pos, r * 10 + (c - 1))
                    if c < 9 and g[r][c + 1] == C:
                        uf.union(pos, r * 10 + (c + 1))
        comp_dict = {}
        for r in range(10):
            for c in range(10):
                if g[r][c] == C:
                    comp_dict[(r, c)] = uf.find(r * 10 + c)
        components[C] = comp_dict
    return components

def fill_gaps(g: List[List[int]], components: dict) -> tuple[List[List[int]], int]:
    out = [row[:] for row in g]
    num_added = 0
    for r in range(10):
        c = 0
        while c < 10:
            if g[r][c] > 1:
                C = g[r][c]
                m = c + 1
                while m < 10 and g[r][m] == 0:
                    m += 1
                k = m - 1
                if k > c:
                    size = k - c
                    fill_it = False
                    left_pos = (r, c)
                    if m < 10 and g[r][m] == C:
                        right_pos = (r, m)
                        if size == 1 or (left_pos in components.get(C, {}) and right_pos in components.get(C, {}) and components[C][left_pos] == components[C][right_pos]):
                            fill_it = True
                    elif r < 9 and g[r + 1][k] == C:
                        below_pos = (r + 1, k)
                        if size == 1 or (left_pos in components.get(C, {}) and below_pos in components.get(C, {}) and components[C][left_pos] == components[C][below_pos]):
                            fill_it = True
                    if fill_it:
                        for pc in range(c + 1, k + 1):
                            if out[r][pc] == 0:
                                out[r][pc] = 1
                                num_added += 1
                c = m
            else:
                c += 1
    return out, num_added

def remove_top_blues(g: List[List[int]], out: List[List[int]], num_added: int) -> List[List[int]]:
    blue_pos = [(rr, cc) for rr in range(10) for cc in range(10) if g[rr][cc] == 1]
    blue_pos.sort(key=lambda p: (p[0], p[1]))
    for i in range(min(num_added, len(blue_pos))):
        rr, cc = blue_pos[i]
        out[rr][cc] = 0
    return out

def program(g: List[List[int]]) -> List[List[int]]:
    components = build_components(g)
    out, num_added = fill_gaps(g, components)
    out = remove_top_blues(g, out, num_added)
    return out
```