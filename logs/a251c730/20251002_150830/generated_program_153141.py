```python
from typing import List
import collections

def find_3_border(g: List[List[int]]) -> tuple:
    n = len(g)
    max_s = 0
    best_left = best_right = best_start = -1
    best_b = 0
    for l in range(n):
        if g[0][l] != 3:
            continue
        b = 3
        for rgt in range(l + 2, n):
            current_s = 0
            curr_start = 0
            for row in range(n):
                if g[row][l] == b and g[row][rgt] == b:
                    current_s += 1
                    if current_s > max_s:
                        max_s = current_s
                        best_left = l
                        best_right = rgt
                        best_start = row - current_s + 1
                        best_b = b
                else:
                    current_s = 0
    return best_left, best_right, best_start, max_s, best_b

def compute_fill(g: List[List[int]], left: int, right: int, start: int, s: int) -> int:
    inner_colors = []
    for r in range(start, start + s):
        for c in range(left + 1, right):
            inner_colors.append(g[r][c])
    if not inner_colors:
        return 0
    return collections.Counter(inner_colors).most_common(1)[0][0]

def program(g: List[List[int]]) -> List[List[int]]:
    left, right, start, s, b = find_3_border(g)
    if s == 0:
        return []
    width = right - left + 1
    height = s + 1
    f = compute_fill(g, left, right, start, s)
    output = [[b] * width for _ in range(height)]
    for i in range(1, height):
        r = start + i - 1
        for j in range(width):
            output[i][j] = g[r][left + j]
    for i in range(1, height - 1):
        inner = output[i][1:width - 1]
        if all(x == b for x in inner):
            for j in range(1, width - 1):
                output[i][j] = f
    return output
```