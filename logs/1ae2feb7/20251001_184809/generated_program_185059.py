```python
from typing import List

def find_trunk_position(row: List[int]) -> int:
    non_zeros = [c for c in range(len(row)) if row[c] != 0]
    return max(non_zeros) if non_zeros else -1

def find_blocks(row: List[int], T: int) -> List[tuple]:
    blocks = []
    c = 0
    N_left = T
    while c < N_left:
        if row[c] == 0:
            c += 1
            continue
        C = row[c]
        start = c
        while c < N_left and row[c] == C:
            c += 1
        end = c - 1
        L = end - start + 1
        dist = T - end - 1
        blocks.append((C, L, dist))
    return blocks

def fill_right(row: List[int], T: int, blocks: List[tuple], N: int) -> List[int]:
    result_row = row[:]
    for p in range(T + 1, N):
        rel = p - (T + 1)
        candidates = []
        for C, L, dist in blocks:
            if rel % L == 0:
                candidates.append((dist, C))
        if candidates:
            candidates.sort(key=lambda x: (x[0], x[1]))
            _, chosen_C = candidates[0]
            result_row[p] = chosen_C
    return result_row

def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    M = len(g)
    N = len(g[0])
    result = [row[:] for row in g]
    for r in range(M):
        T = find_trunk_position(g[r])
        if T == -1:
            continue
        blocks = find_blocks(g[r], T)
        result[r] = fill_right(g[r], T, blocks, N)
    return result
```