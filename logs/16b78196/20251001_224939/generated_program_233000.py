```python
def get_connected_components(g):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = [[False] * 30 for _ in range(30)]
    components = []
    for i in range(30):
        for j in range(30):
            if g[i][j] > 0 and not visited[i][j]:
                color = g[i][j]
                component = []
                stack = [(i, j)]
                visited[i][j] = True
                while stack:
                    x, y = stack.pop()
                    component.append((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 30 and 0 <= ny < 30 and not visited[nx][ny] and g[nx][ny] == color:
                            visited[nx][ny] = True
                            stack.append((nx, ny))
                components.append((color, component))
    return components

def get_anchor(comp):
    min_r = min(r for r, c in comp)
    min_cs = [c for r, c in comp if r == min_r]
    min_c = min(min_cs)
    return min_r, min_c

def try_place(pos, color, out, base_pos):
    ar, ac = get_anchor(pos)
    min_r_b = min(r for r, c in base_pos)
    max_r_b = max(r for r, c in base_pos)
    min_c_b = min(c for r, c in base_pos)
    max_c_b = max(c for r, c in base_pos)
    for tr in range(max(0, min_r_b - 5), min(30, max_r_b + 6)):
        for tc in range(max(0, min_c_b - 5), min(30, max_c_b + 6)):
            if out[tr][tc] != 0:
                continue
            dr = tr - ar
            dc = tc - ac
            valid = True
            for r, c in pos:
                nr = r + dr
                nc = c + dc
                if not (0 <= nr < 30 and 0 <= nc < 30) or out[nr][nc] != 0:
                    valid = False
                    break
            if valid:
                adjacent = False
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for r, c in pos:
                    nr = r + dr
                    nc = c + dc
                    for dx, dy in directions:
                        nnr = nr + dx
                        nnc = nc + dy
                        if 0 <= nnr < 30 and 0 <= nnc < 30 and out[nnr][nnc] > 0:
                            adjacent = True
                            break
                    if adjacent:
                        break
                if adjacent:
                    for r, c in pos:
                        out[r + dr][c + dc] = color
                    return True
    return False

def try_place_above(pos, color, out, base_pos):
    ar, ac = get_anchor(pos)
    min_r_b = min(r for r, c in base_pos)
    for tr in range(0, min_r_b):
        for tc in range(0, 30):
            if out[tr][tc] != 0:
                continue
            dr = tr - ar
            dc = tc - ac
            valid = True
            for r, c in pos:
                nr = r + dr
                nc = c + dc
                if not (0 <= nr < 30 and 0 <= nc < 30) or out[nr][nc] != 0:
                    valid = False
                    break
            if valid:
                adjacent = False
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for r, c in pos:
                    nr = r + dr
                    nc = c + dc
                    for dx, dy in directions:
                        nnr = nr + dx
                        nnc = nc + dy
                        if 0 <= nnr < 30 and 0 <= nnc < 30 and out[nnr][nnc] > 0:
                            adjacent = True
                            break
                    if adjacent:
                        break
                if adjacent:
                    for r, c in pos:
                        out[r + dr][c + dc] = color
                    return True
    return False

def program(g):
    components = get_connected_components(g)
    if not components:
        return [[0] * 30 for _ in range(30)]
    base = max(components, key=lambda x: (len(x[1]), x[0]))
    base_color, base_pos = base
    out = [[0] * 30 for _ in range(30)]
    for r, c in base_pos:
        out[r][c] = base_color
    small_components = [(color, pos) for color, pos in components if (color, pos) != (base_color, base_pos)]
    small_components.sort(key=lambda x: (-len(x[1]), x[0]))
    for color, pos in small_components:
        placed = try_place(pos, color, out, base_pos)
        if not placed:
            placed = try_place_above(pos, color, out, base_pos)
            if not placed:
                for r, c in pos:
                    out[r][c] = color
    return out
```