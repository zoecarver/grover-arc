```python
from typing import List, Tuple
from collections import deque

def copy_grid(g: List[List[int]]) -> List[List[int]]:
    return [row[:] for row in g]

def find_components(g: List[List[int]]) -> Tuple[List[Tuple[int, int, int, int]], List[List[int]]]:
    if not g or not g[0]:
        return [], [[0]]
    h, w = len(g), len(g[0])
    label = [[0] * w for _ in range(h)]
    next_label = 1
    components = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(h):
        for j in range(w):
            if g[i][j] == 5 and label[i][j] == 0:
                size = 0
                queue = deque([(i, j)])
                label[i][j] = next_label
                min_r, min_c = i, j
                while queue:
                    x, y = queue.popleft()
                    size += 1
                    min_r = min(min_r, x)
                    min_c = min(min_c, y)
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < h and 0 <= ny < w and g[nx][ny] == 5 and label[nx][ny] == 0:
                            label[nx][ny] = next_label
                            queue.append((nx, ny))
                components.append((next_label, min_r, min_c, size))
                next_label += 1
    return components, label

def build_adjacency(label: List[List[int]], num_labels: int) -> List[List[int]]:
    h, w = len(label), len(label[0])
    adj = [[] for _ in range(num_labels + 1)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for i in range(h):
        for j in range(w):
            if label[i][j] > 0:
                l = label[i][j]
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < h and 0 <= nj < w and label[ni][nj] > 0 and label[ni][nj] != l:
                        adj[l].append(label[ni][nj])
    for i in range(1, num_labels + 1):
        adj[i] = list(set(adj[i]))
    return adj

def assign_colors(adj: List[List[int]], num_labels: int) -> List[int]:
    colors = [0] * (num_labels + 1)
    for l in range(1, num_labels + 1):
        forbidden = set(colors[n] for n in adj[l] if colors[n] != 0)
        for c in range(4, 0, -1):
            if c not in forbidden:
                colors[l] = c
                break
    return colors

def program(g: List[List[int]]) -> List[List[int]]:
    output = copy_grid(g)
    components, label = find_components(g)
    if not components:
        return output
    num_labels = len(components)
    adj = build_adjacency(label, num_labels)
    colors = assign_colors(adj, num_labels)
    h, w = len(g), len(g[0])
    for i in range(h):
        for j in range(w):
            if g[i][j] == 5:
                output[i][j] = colors[label[i][j]]
    return output
```