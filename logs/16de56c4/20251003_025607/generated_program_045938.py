```python
import typing as tp
from collections import defaultdict

def program(g: tp.List[tp.List[int]]) -> tp.List[tp.List[int]]:
    if not g:
        return []
    height = len(g)
    if height == 0:
        return g
    width = len(g[0])
    # Vertical transformations first
    for col in range(width):
        pos_by_c = defaultdict(list)
        for row in range(height):
            c = g[row][col]
            if c != 0:
                pos_by_c[c].append(row)
        for c, poss in pos_by_c.items():
            if len(poss) != 2:
                continue
            ps = sorted(poss)
            p, q = ps[0], ps[1]
            d = q - p
            if d == 0:
                continue
            # Up extension (decreasing row)
            potential_up = []
            curr = p
            while curr - d >= 0:
                np = curr - d
                potential_up.append(np)
                curr = np
            chain_set = set([p, q])
            i = 0
            new_c = c
            conflicted = False
            while i < len(potential_up):
                pos = potential_up[i]
                cc = g[pos][col]
                if cc != 0 and cc != c:
                    new_c = cc
                    conflicted = True
                    for j in range(i + 1):
                        chain_set.add(potential_up[j])
                    break
                else:
                    chain_set.add(pos)
                    i += 1
            if conflicted:
                for yy in chain_set:
                    g[yy][col] = new_c
            else:
                for yy in chain_set:
                    if g[yy][col] == 0:
                        g[yy][col] = c
            # Down extension (increasing row)
            potential_down = []
            curr = q
            while curr + d < height:
                np = curr + d
                potential_down.append(np)
                curr = np
            chain_set = set([p, q])
            i = 0
            new_c = c
            conflicted = False
            while i < len(potential_down):
                pos = potential_down[i]
                cc = g[pos][col]
                if cc != 0 and cc != c:
                    new_c = cc
                    conflicted = True
                    for j in range(i + 1):
                        chain_set.add(potential_down[j])
                    break
                else:
                    chain_set.add(pos)
                    i += 1
            if conflicted:
                for yy in chain_set:
                    g[yy][col] = new_c
            else:
                for yy in chain_set:
                    if g[yy][col] == 0:
                        g[yy][col] = c
    # Horizontal transformations second
    for row in range(height):
        pos_by_c = defaultdict(list)
        for colu in range(width):
            c = g[row][colu]
            if c != 0:
                pos_by_c[c].append(colu)
        for c, poss in pos_by_c.items():
            if len(poss) != 2:
                continue
            ps = sorted(poss)
            p, q = ps[0], ps[1]
            d = q - p
            if d == 0:
                continue
            # Left extension (decreasing col)
            potential_left = []
            curr = p
            while curr - d >= 0:
                np = curr - d
                potential_left.append(np)
                curr = np
            chain_set = set([p, q])
            i = 0
            new_c = c
            conflicted = False
            while i < len(potential_left):
                pos = potential_left[i]
                cc = g[row][pos]
                if cc != 0 and cc != c:
                    new_c = cc
                    conflicted = True
                    for j in range(i + 1):
                        chain_set.add(potential_left[j])
                    break
                else:
                    chain_set.add(pos)
                    i += 1
            if conflicted:
                for xx in chain_set:
                    g[row][xx] = new_c
            else:
                for xx in chain_set:
                    if g[row][xx] == 0:
                        g[row][xx] = c
            # Right extension (increasing col)
            potential_right = []
            curr = q
            while curr + d < width:
                np = curr + d
                potential_right.append(np)
                curr = np
            chain_set = set([p, q])
            i = 0
            new_c = c
            conflicted = False
            while i < len(potential_right):
                pos = potential_right[i]
                cc = g[row][pos]
                if cc != 0 and cc != c:
                    new_c = cc
                    conflicted = True
                    for j in range(i + 1):
                        chain_set.add(potential_right[j])
                    break
                else:
                    chain_set.add(pos)
                    i += 1
            if conflicted:
                for xx in chain_set:
                    g[row][xx] = new_c
            else:
                for xx in chain_set:
                    if g[row][xx] == 0:
                        g[row][xx] = c
    return g
```