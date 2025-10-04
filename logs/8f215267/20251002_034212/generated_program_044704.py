```python
from typing import List
from collections import defaultdict

def get_background_color(g: List[List[int]]) -> int:
    return g[0][0] if g else 0

def find_frames(g: List[List[int]], B: int) -> List[tuple]:
    frames = []
    h = len(g)
    if h == 0:
        return frames
    w = len(g[0])
    width = 11
    for start_r in range(h - 3):
        for start_c in range(w - width + 1):
            for f_height in [4, 5]:
                end_r = start_r + f_height - 1
                if end_r >= h:
                    continue
                if g[start_r][start_c] == B:
                    continue
                C = g[start_r][start_c]
                # check top
                top_ok = all(g[start_r][j] == C for j in range(start_c, start_c + width))
                if not top_ok:
                    continue
                # check bottom
                bottom_ok = all(g[end_r][j] == C for j in range(start_c, start_c + width))
                if not bottom_ok:
                    continue
                # check sides
                side_ok = True
                for i in range(1, f_height - 1):
                    if g[start_r + i][start_c] != C or g[start_r + i][start_c + width - 1] != C:
                        side_ok = False
                        break
                if not side_ok:
                    continue
                # check inner all B
                inner_ok = True
                for i in range(1, f_height - 1):
                    for j in range(1, width - 1):
                        if g[start_r + i][start_c + j] != B:
                            inner_ok = False
                            break
                    if not inner_ok:
                        break
                if inner_ok:
                    frames.append((C, start_r, start_c, f_height))
    return frames

def process_smalls(g: List[List[int]], B: int, out: List[List[int]], frames: List[tuple]) -> dict:
    h = len(g)
    if h == 0:
        return {}
    w = len(g[0])
    visited = [[False] * w for _ in range(h)]
    small_count = defaultdict(int)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(h):
        for j in range(w):
            if visited[i][j] or g[i][j] == B:
                continue
            color = g[i][j]
            comp_pos = []
            stack = [(i, j)]
            visited[i][j] = True
            comp_pos.append((i, j))
            while stack:
                x, y = stack.pop()
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < h and 0 <= ny < w and not visited[nx][ny] and g[nx][ny] == color:
                        visited[nx][ny] = True
                        stack.append((nx, ny))
                        comp_pos.append((nx, ny))
            size = len(comp_pos)
            if size > 8 or size == 0:
                continue
            is_special = False
            if size == 4:
                min_r = min(p[0] for p in comp_pos)
                max_r = max(p[0] for p in comp_pos)
                min_c = min(p[1] for p in comp_pos)
                max_c = max(p[1] for p in comp_pos)
                if max_r - min_r == 1 and max_c - min_c == 1:
                    is_special = True
                    small_count[color] += 2
            if not is_special:
                small_count[color] += 1
            # remove small
            for px, py in comp_pos:
                out[px][py] = B
    return dict(small_count)

def program(g: List[List[int]]) -> List[List[int]]:
    if not g or not g[0]:
        return []
    out = [row[:] for row in g]
    B = get_background_color(g)
    frames = find_frames(g, B)
    small_counts = process_smalls(g, B, out, frames)
    for C, fr, fc, fheight in frames:
        N = small_counts.get(C, 0)
        num_inner = fheight - 2
        middle_offset = (num_inner - 1) // 2
        mid_row = fr + 1 + middle_offset
        inner_left = fc + 1
        possible_rel = [1, 3, 5, 7]
        num_pos = len(possible_rel)
        to_fill = min(N, num_pos)
        selected_rel = possible_rel[num_pos - to_fill:]
        for rel in selected_rel:
            col = inner_left + rel
            if 0 <= mid_row < len(g) and 0 <= col < len(g[0]):
                out[mid_row][col] = C
    return out
```