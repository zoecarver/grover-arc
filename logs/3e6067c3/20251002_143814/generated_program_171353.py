```python
from typing import List, Dict, Tuple
from collections import defaultdict, deque

def find_background_color(g: List[List[int]]) -> int:
    return g[0][0]

def extract_legend(g: List[List[int]], bg: int) -> List[int]:
    n = len(g)
    m = len(g[0])
    return [g[n-2][c] for c in range(m) if g[n-2][c] != bg]

def find_connected_blocks(g: List[List[int]], bg: int) -> Dict[int, List[Tuple[int, int, int, int]]]:
    n = len(g)
    m = len(g[0])
    visited = [[False] * m for _ in range(n)]
    blocks: Dict[int, List[Tuple[int, int, int, int]]] = defaultdict(list)
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(n):
        for c in range(m):
            if g[r][c] != bg and not visited[r][c]:
                col = g[r][c]
                min_r = max_r = r
                min_c = max_c = c
                stack = [(r, c)]
                visited[r][c] = True
                while stack:
                    rr, cc = stack.pop()
                    min_r = min(min_r, rr)
                    max_r = max(max_r, rr)
                    min_c = min(min_c, cc)
                    max_c = max(max_c, cc)
                    for dr, dc in dirs:
                        nr = rr + dr
                        nc = cc + dc
                        if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and g[nr][nc] == col:
                            visited[nr][nc] = True
                            stack.append((nr, nc))
                blocks[col].append((min_r, max_r, min_c, max_c))
    return blocks

def sort_blocks_by_position(blocks: Dict[int, List[Tuple[int, int, int, int]]]) -> Dict[int, List[Tuple[int, int, int, int]]]:
    for col in blocks:
        blocks[col] = sorted(blocks[col], key=lambda bbox: (bbox[0], bbox[2]))
    return blocks

def fill_horizontal_gap(g: List[List[int]], left_bbox: Tuple[int, int, int, int], right_bbox: Tuple[int, int, int, int], fill_col: int, bg: int) -> None:
    min_r = left_bbox[0]
    max_r = left_bbox[1]
    start_c = left_bbox[3] + 1
    end_c = right_bbox[2]
    for r in range(min_r, max_r + 1):
        for c in range(start_c, end_c):
            if g[r][c] == bg:
                g[r][c] = fill_col

def fill_vertical_gap(g: List[List[int]], up_bbox: Tuple[int, int, int, int], down_bbox: Tuple[int, int, int, int], fill_col: int, bg: int) -> None:
    min_c = up_bbox[2]
    max_c = up_bbox[3]
    start_r = up_bbox[1] + 1
    end_r = down_bbox[0]
    for c in range(min_c, max_c + 1):
        for r in range(start_r, end_r):
            if g[r][c] == bg:
                g[r][c] = fill_col

def connect_two_blocks(g: List[List[int]], start_bbox: Tuple[int, int, int, int], end_bbox: Tuple[int, int, int, int], fill_col: int, bg: int) -> None:
    minr_s, maxr_s, minc_s, maxc_s = start_bbox
    minr_e, maxr_e, minc_e, maxc_e = end_bbox
    if minr_s == minr_e and maxr_s == maxr_e:
        if minc_s < minc_e:
            fill_horizontal_gap(g, start_bbox, end_bbox, fill_col, bg)
        else:
            fill_horizontal_gap(g, end_bbox, start_bbox, fill_col, bg)
    elif minc_s == minc_e and maxc_s == maxc_e:
        if minr_s < minr_e:
            fill_vertical_gap(g, start_bbox, end_bbox, fill_col, bg)
        else:
            fill_vertical_gap(g, end_bbox, start_bbox, fill_col, bg)

def program(g: List[List[int]]) -> List[List[int]]:
    g = [row[:] for row in g]
    bg = find_background_color(g)
    seq = extract_legend(g, bg)
    raw_blocks = find_connected_blocks(g, bg)
    sorted_blocks = sort_blocks_by_position(raw_blocks)
    queues = {col: deque(bboxes) for col, bboxes in sorted_blocks.items()}
    for i in range(len(seq) - 1):
        s_col = seq[i]
        e_col = seq[i + 1]
        if s_col in queues and queues[s_col] and e_col in queues and queues[e_col]:
            s_bbox = queues[s_col].popleft()
            e_bbox = queues[e_col].popleft()
            connect_two_blocks(g, s_bbox, e_bbox, s_col, bg)
    return g
```