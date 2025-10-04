```python
from typing import List
from collections import Counter

def find_walls(g: List[List[int]], B: int, h: int, w: int) -> List[int]:
    walls = [0, w - 1]
    for j in range(1, w - 1):
        if all(g[i][j] == B for i in range(h)):
            walls.append(j)
    return sorted(set(walls))

def get_mode_k(blocks: List[int]) -> int:
    if not blocks:
        return 0
    count = Counter(blocks)
    max_f = max(count.values())
    cand_ks = [k for k, f in count.items() if f == max_f]
    return max(cand_ks)

def compute_best_phase(inner: List[int], S: int, B: int, K: int, inner_len: int) -> tuple[int, int, int]:
    p = K + 1
    best_mis = float('inf')
    best_pres = -1
    best_ph = -1
    for ph in range(p):
        mis = 0
        pres = 0
        for ii in range(inner_len):
            pos_mod = (ii + ph) % p
            exp = S if pos_mod < K else B
            curr = inner[ii]
            if curr != 2 and curr != exp:
                mis += 1
            if curr == S and exp == S:
                pres += 1
        if (mis < best_mis or
            (mis == best_mis and (pres > best_pres or (pres == best_pres and ph < best_ph)))):
            best_mis = mis
            best_pres = pres
            best_ph = ph
    return best_ph, best_mis, best_pres

def compute_solid(inner: List[int], S: int) -> tuple[int, int]:
    inner_len = len(inner)
    solid_mis = sum(1 for v in inner if v != S and v != 2)
    solid_pres = sum(1 for v in inner if v == S)
    return solid_mis, solid_pres

def apply_pattern(inner: List[int], S: int, B: int, K: int, ph: int) -> None:
    inner_len = len(inner)
    p = K + 1
    for ii in range(inner_len):
        pos_mod = (ii + ph) % p
        inner[ii] = S if pos_mod < K else B

def apply_solid_fill(inner: List[int], S: int) -> None:
    for i in range(len(inner)):
        inner[i] = S

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return [row[:] for row in g]
    h = len(g)
    w = len(g[0])
    B = g[0][0]
    walls = find_walls(g, B, h, w)
    new_g = [row[:] for row in g]
    for r in range(h):
        row = new_g[r]
        prev_j = None
        for j in walls:
            if prev_j is not None:
                j1 = prev_j
                j2 = j
                sub_start = j1 + 1
                sub_end = j2
                subrow = row[sub_start:sub_end]
                n_sub = len(subrow)
                if n_sub == 0:
                    continue
                side_c = None
                inner_start_local = 0
                inner = subrow[:]
                inner_len = n_sub
                if n_sub >= 2 and subrow[0] == subrow[-1] != B:
                    side_c = subrow[0]
                    inner_start_local = 1
                    inner = subrow[1:n_sub - 1]
                    inner_len = n_sub - 2
                if inner_len == 0:
                    continue
                cands = set(val for val in inner if val != B and val != side_c)
                if len(cands) != 1:
                    continue
                S = next(iter(cands))
                if S not in {1, 2, 3, 4, 8, 9}:
                    continue
                blocks = []
                i = 0
                while i < inner_len:
                    if inner[i] == S:
                        sz = 0
                        while i < inner_len and inner[i] == S:
                            sz += 1
                            i += 1
                        blocks.append(sz)
                    else:
                        i += 1
                if not blocks:
                    continue
                K = get_mode_k(blocks)
                if K == 0:
                    continue
                best_ph, pattern_mis, pattern_pres = compute_best_phase(inner, S, B, K, inner_len)
                solid_mis, solid_pres = compute_solid(inner, S)
                apply_solid_flag = (solid_mis < pattern_mis or
                                    (solid_mis == pattern_mis and solid_pres > pattern_pres))
                if apply_solid_flag:
                    apply_solid_fill(inner, S)
                else:
                    apply_pattern(inner, S, B, K, best_ph)
                # put back
                back_start = sub_start + inner_start_local
                back_end = back_start + inner_len
                row[back_start:back_end] = inner
            prev_j = j
    return new_g
```