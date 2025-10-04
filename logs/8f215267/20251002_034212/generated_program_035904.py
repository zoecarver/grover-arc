```python
def get_background(g: List[List[int]]) -> int:
    return g[0][0]

def is_full(row: List[int], l: int, c: int, m: int) -> bool:
    if l < 0 or l + 10 >= m:
        return False
    return all(row[k] == c for k in range(l, l + 11))

def is_leg(row: List[int], l: int, c: int, bg: int, m: int) -> bool:
    if l < 0 or l + 10 >= m:
        return False
    if row[l] != c or row[l + 10] != c:
        return False
    for k in range(l + 1, l + 10):
        if row[k] != bg:
            return False
    return True

def get_k(c: int, l: int, s: int) -> int:
    if c == 1:
        return 4 - l
    if c == 2:
        return 1 if s == 1 else 2
    return c // 2 + 1

def program(g: List[List[int]]) -> List[List[int]]:
    n = len(g)
    m = len(g[0])
    bg = get_background(g)
    out = [[bg for _ in range(m)] for _ in range(n)]
    visited = [False] * n
    for s in range(n):
        if visited[s]:
            continue
        for l in range(m - 10):
            c = g[s][l]
            if c == bg or not is_full(g[s], l, c, m):
                continue
            num_leg = 0
            r = s + 1
            while r < n and is_leg(g[r], l, c, bg, m):
                num_leg += 1
                r += 1
            if num_leg < 3:
                continue
            potential_bottom = s + num_leg + 1
            if potential_bottom < n and is_full(g[potential_bottom], l, c, m):
                bottom = potential_bottom
            else:
                bottom = s + 4
            # draw top full
            for kk in range(l, l + 11):
                out[s][kk] = c
            # draw bottom full if valid
            if bottom < n:
                for kk in range(l, l + 11):
                    out[bottom][kk] = c
            # draw legs
            for ii in range(num_leg):
                rr = s + 1 + ii
                if rr < n:
                    out[rr][l] = c
                    out[rr][l + 10] = c
            # draw cross
            cross_r = s + 1 + (num_leg // 2)
            if cross_r < n:
                out[cross_r][l] = c
                out[cross_r][l + 10] = c
                k = get_k(c, l, s)
                for p in range(k):
                    pos = l + 10 - 2 * p
                    if 0 <= pos < m:
                        out[cross_r][pos] = c
            # mark visited
            end_row = min(bottom, n - 1)
            for rr in range(s, end_row + 1):
                visited[rr] = True
    return out
```