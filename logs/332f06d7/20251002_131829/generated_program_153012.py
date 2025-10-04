```python
import collections

def find_active_components(g, n):
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    components = []
    for i in range(n):
        for j in range(n):
            if g[i][j] in (1, 2) and (i, j) not in visited:
                component = []
                queue = collections.deque([(i, j)])
                visited.add((i, j))
                while queue:
                    r, c = queue.popleft()
                    component.append((r, c))
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and g[nr][nc] in (1, 2) and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                components.append(component)
    return components

def get_adjacent_zeros(component, g, n):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    adj_set = set()
    for r, c in component:
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and g[nr][nc] == 0:
                adj_set.add((nr, nc))
    return list(adj_set)

def absorb(out, two_pos, k, n):
    if k == 0:
        return
    sorted_two = sorted(two_pos, key=lambda p: (p[0], p[1]))
    for i in range(k):
        r, c = sorted_two[i]
        out[r][c] = 0

def reshape(out, one_pos, adj0, n):
    if not adj0 or not one_pos:
        return
    # bbox of adj0
    min_r0 = min(r for r, c in adj0)
    max_r0 = max(r for r, c in adj0)
    min_c0 = min(c for r, c in adj0)
    max_c0 = max(c for r, c in adj0)
    h = max_r0 - min_r0 + 1
    w = max_c0 - min_c0 + 1
    # bbox of one_pos
    one_set = set(one_pos)
    min_r1 = min(r for r, c in one_pos)
    max_r1 = max(r for r, c in one_pos)
    min_c1 = min(c for r, c in one_pos)
    max_c1 = max(c for r, c in one_pos)
    target_start_c = max_c1 - w + 1
    possible = []
    for start_r in range(min_r1, max_r1 - h + 2):
        good = True
        for dr in range(h):
            rr = start_r + dr
            for dc in range(w):
                cc = target_start_c + dc
                if (rr, cc) not in one_set:
                    good = False
                    break
            if not good:
                break
        if good:
            possible.append(start_r)
    if possible:
        chosen_start_r = max(possible)
        for dr in range(h):
            rr = chosen_start_r + dr
            for dc in range(w):
                cc = target_start_c + dc
                out[rr][cc] = 0

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    out = [row[:] for row in g]
    components = find_active_components(g, n)
    for component in components:
        adj0 = get_adjacent_zeros(component, g, n)
        k = len(adj0)
        if k == 0:
            continue
        two_pos = [p for p in component if g[p[0]][p[1]] == 2]
        num2 = len(two_pos)
        one_pos = [p for p in component if g[p[0]][p[1]] == 1]
        if num2 >= k:
            absorb(out, two_pos, k, n)
        else:
            reshape(out, one_pos, adj0, n)
        # fill adj0 to 1
        for r, c in adj0:
            out[r][c] = 1
    return out
```