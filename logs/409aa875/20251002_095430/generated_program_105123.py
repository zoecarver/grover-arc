```python
from typing import List

def get_non7_color_and_positions(g: List[List[int]]) -> tuple:
    pos_list = [j for j in range(16) if g[15][j] != 7]
    if not pos_list:
        return 7, []
    color = g[15][pos_list[0]]
    return color, pos_list

def compute_positions(pos_list: List[int]) -> List[int]:
    if len(pos_list) < 2:
        return pos_list[:]
    diffs = [pos_list[k + 1] - pos_list[k] for k in range(len(pos_list) - 1)]
    if all(d == diffs[0] for d in diffs):
        d = diffs[0]
        return [k * d for k in range(len(pos_list))]
    # grouping
    groups = []
    if pos_list:
        curr = [pos_list[0]]
        for k in range(1, len(pos_list)):
            if pos_list[k] - curr[-1] == 2:
                curr.append(pos_list[k])
            else:
                groups.append(curr)
                curr = [pos_list[k]]
        groups.append(curr)
    positions = []
    for grp in groups:
        if len(grp) == 1:
            positions.append(grp[0])
        elif len(grp) == 2:
            positions.append((grp[0] + grp[1]) // 2)
    return positions

def is_matching(g: List[List[int]]) -> bool:
    return all(g[6][j] == g[14][j] and g[7][j] == g[15][j] for j in range(16))

def is_upper_empty(g: List[List[int]]) -> bool:
    return all(all(cell == 7 for cell in row) for row in g[:9])

def count_upper_non7(g: List[List[int]]) -> int:
    return sum(1 for row in g[:9] for cell in row if cell != 7)

def program(g: List[List[int]]) -> List[List[int]]:
    new_g = [row[:] for row in g]
    color, pos_list = get_non7_color_and_positions(g)
    positions = compute_positions(pos_list)
    for p in positions:
        if 0 <= p < 16:
            new_g[9][p] = 9
    if len(positions) == 3 and color == 9:
        if len(positions) > 1:
            new_g[9][positions[1]] = 1
    matching = is_matching(g)
    upper_empty = is_upper_empty(g)
    count_upper = count_upper_non7(g)
    if matching:
        for p in positions:
            if 0 <= p < 16:
                new_g[1][p] = 9
        new_g[6][8] = 9
        new_g[6][9] = 9
        new_g[7][8] = 9
    if upper_empty:
        new_g[5][1] = 9
        new_g[6][8] = 9
        new_g[7][4] = 9
        new_g[8][11] = 9
    if not matching and not upper_empty and count_upper > 3:
        for p in positions:
            if 0 <= p < 16:
                new_g[1][p] = 9
    return new_g
```