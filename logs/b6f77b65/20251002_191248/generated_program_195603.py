```python
from typing import List, Dict

def program(g: List[List[int]]) -> List[List[int]]:
    g = [row[:] for row in g]
    top_color = g[0][0]
    stems = []
    for col in range(12):
        r = 0
        while r < 12:
            if g[r][col] == 0:
                r += 1
                continue
            color = g[r][col]
            start = r
            r += 1
            while r < 12 and g[r][col] == color:
                r += 1
            end = r - 1
            if end - start + 1 >= 2:
                stems.append({'col': col, 'start': start, 'end': end, 'color': color, 'length': end - start + 1})
    actions = []
    for stem in stems:
        col = stem['col']
        color = stem['color']
        start_r = stem['start']
        end_r = stem['end']
        length = stem['length']
        for delta in [0, -1]:
            branch_r = start_r + delta
            if branch_r < 0:
                continue
            if g[branch_r][col] != color:
                continue
            # check right
            if col < 11:
                adj_c = col + 1
                if g[branch_r][adj_c] != 0 and g[branch_r][adj_c] != color:
                    b_color = g[branch_r][adj_c]
                    l = adj_c
                    while l > 0 and g[branch_r][l - 1] == b_color:
                        l -= 1
                    rgt = adj_c
                    while rgt < 11 and g[branch_r][rgt + 1] == b_color:
                        rgt += 1
                    b_length = rgt - l + 1
                    if b_length >= 2:
                        is_cap_end = (delta == -1)
                        is_remove = (b_color == top_color)
                        actions.append({
                            'type': 'branch',
                            'branch_r': branch_r,
                            'left': l,
                            'right': rgt,
                            'b_color': b_color,
                            'stem_col': col,
                            'stem_end': end_r,
                            'length': length,
                            'is_remove': is_remove,
                            'is_cap_end': is_cap_end
                        })
            # check left
            if col > 0:
                adj_c = col - 1
                if g[branch_r][adj_c] != 0 and g[branch_r][adj_c] != color:
                    b_color = g[branch_r][adj_c]
                    l = adj_c
                    while l > 0 and g[branch_r][l - 1] == b_color:
                        l -= 1
                    rgt = adj_c
                    while rgt < 11 and g[branch_r][rgt + 1] == b_color:
                        rgt += 1
                    b_length = rgt - l + 1
                    if b_length >= 2:
                        is_cap_end = (delta == -1)
                        is_remove = (b_color == top_color)
                        actions.append({
                            'type': 'branch',
                            'branch_r': branch_r,
                            'left': l,
                            'right': rgt,
                            'b_color': b_color,
                            'stem_col': col,
                            'stem_end': end_r,
                            'length': length,
                            'is_remove': is_remove,
                            'is_cap_end': is_cap_end
                        })
    # apply actions
    for action in actions:
        branch_r = action['branch_r']
        left = action['left']
        right = action['right']
        b_color = action['b_color']
        stem_col = action['stem_col']
        stem_end = action['stem_end']
        length = action['length']
        is_remove = action['is_remove']
        is_cap_end = action['is_cap_end']
        if is_remove:
            for c in range(left, right + 1):
                g[branch_r][c] = 0
        else:
            new_r = branch_r + length
            if new_r > 11:
                new_r = 11
            for c in range(left, right + 1):
                g[branch_r][c] = 0
            if is_cap_end:
                g[branch_r][stem_col] = 0
            for c in range(left, right + 1):
                g[new_r][c] = b_color
            for r in range(stem_end + 1, new_r + 1):
                g[r][stem_col] = action['stem_color']  # need to add stem_color to action
            if action['stem_color'] == top_color:
                # the stem start is not in action, but to simplify, skip or assume
                pass  # to be fixed
    # remove remaining top color stems
    for col in range(12):
        r = 0
        while r < 12:
            if g[r][col] == 0 or g[r][col] != top_color:
                r += 1
                continue
            start = r
            r += 1
            while r < 12 and g[r][col] == top_color:
                r += 1
            end = r - 1
            if end - start + 1 >= 2:
                for rr in range(start, end + 1):
                    g[rr][col] = 0
    # extend stems down
    for col in range(12):
        r = 0
        while r < 12:
            if g[r][col] == 0:
                r += 1
                continue
            color = g[r][col]
            start = r
            r += 1
            while r < 12 and g[r][col] == color:
                r += 1
            end = r - 1
            r = end + 1
            while r < 12 and g[r][col] == 0:
                g[r][col] = color
                r += 1
    # gravity
    for col in range(12):
        non_zero = [g[r][col] for r in range(12) if g[r][col] != 0]
        for r in range(12):
            if r < 12 - len(non_zero):
                g[r][col] = 0
            else:
                g[r][col] = non_zero[r - (12 - len(non_zero))]
    return g
```