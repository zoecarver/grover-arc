```python
from typing import List, Tuple, Dict, DefaultDict
from collections import defaultdict

def get_background(g: List[List[int]]) -> int:
    return g[-1][0]

def get_sequence(g: List[List[int]], bg: int) -> List[int]:
    key = g[-2]
    m = len(key)
    seq = []
    for j in range(m):
        if key[j] != bg:
            seq.append(key[j])
    return seq

def find_seed_blocks(g: List[List[int]], bg: int) -> List[Tuple[int, int, int, int, int]]:
    n = len(g)
    m = len(g[0])
    blocks = []
    visited = [[False] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if 2 <= g[i][j] <= 9 and not visited[i][j]:
                c = g[i][j]
                # horizontal extent at i
                j_left = j
                while j_left > 0 and g[i][j_left - 1] == c:
                    j_left -= 1
                j_right = j
                while j_right < m - 1 and g[i][j_right + 1] == c:
                    j_right += 1
                # vertical extent
                i_top = i
                while i_top > 0:
                    if all(g[i_top - 1][jj] == c for jj in range(j_left, j_right + 1)):
                        i_top -= 1
                    else:
                        break
                i_bot = i
                while i_bot < n - 1:
                    if all(g[i_bot + 1][jj] == c for jj in range(j_left, j_right + 1)):
                        i_bot += 1
                    else:
                        break
                # mark visited
                for ii in range(i_top, i_bot + 1):
                    for jj in range(j_left, j_right + 1):
                        visited[ii][jj] = True
                blocks.append((c, i_top, i_bot, j_left, j_right))
    return blocks

def build_adjacency(blocks: List[Tuple[int, int, int, int, int]], g: List[List[int]], bg: int) -> List[List[int]]:
    num = len(blocks)
    adj = [[] for _ in range(num)]
    n = len(g)
    for i in range(num):
        for j in range(i + 1, num):
            _, r1s, r1e, c1s, c1e = blocks[i]
            _, r2s, r2e, c2s, c2e = blocks[j]
            added = False
            # h adjacent
            if r1s == r2s and r1e == r2e:
                if c1e < c2s:
                    gs = c1e + 1
                    ge = c2s - 1
                    if gs <= ge:
                        is_adj = True
                        for rr in range(r1s, r1e + 1):
                            for cc in range(gs, ge + 1):
                                if g[rr][cc] != bg:
                                    is_adj = False
                                    break
                            if not is_adj:
                                break
                        if is_adj:
                            adj[i].append(j)
                            adj[j].append(i)
                            added = True
                elif c2e < c1s:
                    gs = c2e + 1
                    ge = c1s - 1
                    if gs <= ge:
                        is_adj = True
                        for rr in range(r1s, r1e + 1):
                            for cc in range(gs, ge + 1):
                                if g[rr][cc] != bg:
                                    is_adj = False
                                    break
                            if not is_adj:
                                break
                        if is_adj:
                            adj[i].append(j)
                            adj[j].append(i)
                            added = True
            # v adjacent
            if not added and c1s == c2s and c1e == c2e:
                if r1e < r2s:
                    gs = r1e + 1
                    ge = r2s - 1
                    if gs <= ge:
                        is_adj = True
                        for rr in range(gs, ge + 1):
                            if not all(g[rr][cc] == bg for cc in range(c1s, c1e + 1)):
                                is_adj = False
                                break
                        if is_adj:
                            adj[i].append(j)
                            adj[j].append(i)
                elif r2e < r1s:
                    gs = r2e + 1
                    ge = r1s - 1
                    if gs <= ge:
                        is_adj = True
                        for rr in range(gs, ge + 1):
                            if not all(g[rr][cc] == bg for cc in range(c1s, c1e + 1)):
                                is_adj = False
                                break
                        if is_adj:
                            adj[i].append(j)
                            adj[j].append(i)
    return adj

def find_path(seq: List[int], blocks: List[Tuple[int, int, int, int, int]], adj: List[List[int]]) -> List[int]:
    num = len(blocks)
    def backtrack(pos: int, path: List[int], used: List[bool]) -> List[int]:
        if pos == len(seq):
            return path[:]
        c = seq[pos]
        prev = path[-1] if path else -1
        cands = list(range(num)) if prev == -1 else adj[prev]
        for k in cands:
            if not used[k] and blocks[k][0] == c:
                path.append(k)
                used[k] = True
                res = backtrack(pos + 1, path, used)
                if res:
                    return res
                path.pop()
                used[k] = False
        return None
    for k in range(num):
        if blocks[k][0] == seq[0]:
            used = [False] * num
            used[k] = True
            res = backtrack(1, [k], used)
            if res:
                return res
    return []

def fill_gap_between_blocks(out: List[List[int]], blocks: List[Tuple[int, int, int, int, int]], k: int, l: int, fill_c: int, bg: int):
    _, rks, rke, cks, cke = blocks[k]
    _, rls, rle, cls, cle = blocks[l]
    # horizontal
    if rks == rls and rke == rle:
        if cke < cls:
            gcs = cke + 1
            gce = cls - 1
            if gcs > gce:
                return
            for ii in range(rks, rke + 1):
                for jj in range(gcs, gce + 1):
                    if out[ii][jj] == bg:
                        out[ii][jj] = fill_c
        elif cle < cks:
            gcs = cle + 1
            gce = cks - 1
            if gcs > gce:
                return
            for ii in range(rks, rke + 1):
                for jj in range(gcs, gce + 1):
                    if out[ii][jj] == bg:
                        out[ii][jj] = fill_c
    # vertical
    if cks == cls and cke == cle:
        if rke < rls:
            grs = rke + 1
            gre = rls - 1
            if grs > gre:
                return
            for ii in range(grs, gre + 1):
                if all(out[ii][jj] == bg for jj in range(cks, cke + 1)):
                    for jj in range(cks, cke + 1):
                        out[ii][jj] = fill_c
        elif rle < rks:
            grs = rle + 1
            gre = rks - 1
            if grs > gre:
                return
            for ii in range(grs, gre + 1):
                if all(out[ii][jj] == bg for jj in range(cks, cke + 1)):
                    for jj in range(cks, cke + 1):
                        out[ii][jj] = fill_c

def group_by_col_range(path: List[int], blocks: List[Tuple[int, int, int, int, int]]) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    col_to_visits: DefaultDict[Tuple[int, int], List[Tuple[int, int]]] = defaultdict(list)
    for idx, k in enumerate(path):
        cs = blocks[k][3]
        ce = blocks[k][4]
        col_to_visits[(cs, ce)].append((idx, k))
    return col_to_visits

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]
    bg = get_background(g)
    seq = get_sequence(g, bg)
    blocks = find_seed_blocks(out, bg)
    adj_list = build_adjacency(blocks, out, bg)
    path = find_path(seq, blocks, adj_list)
    for i in range(len(path) - 1):
        fill_gap_between_blocks(out, blocks, path[i], path[i + 1], blocks[path[i]][0], bg)
    col_groups = group_by_col_range(path, blocks)
    for _, visits in col_groups.items():
        sub_path = [k for _, k in sorted(visits)]
        for i in range(len(sub_path) - 1):
            fill_gap_between_blocks(out, blocks, sub_path[i], sub_path[i + 1], blocks[sub_path[i]][0], bg)
    return out
```