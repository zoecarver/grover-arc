```python
from typing import List, Dict, Tuple
from collections import defaultdict

def program(g: List[List[int]]) -> List[List[int]]:
    result = [row[:] for row in g]
    h = len(result)
    if h == 0:
        return result
    w = len(result[0])

    def count_non_blanks(grid: List[List[int]]) -> Dict[int, int]:
        counts = defaultdict(int)
        for i in range(h):
            for j in range(w):
                c = grid[i][j]
                if c != 8:
                    counts[c] += 1
        return counts

    def find_singleton_positions(grid: List[List[int]], singletons: List[int]) -> Dict[int, Tuple[int, int]]:
        pos_dict: Dict[int, Tuple[int, int]] = {}
        for i in range(h):
            for j in range(w):
                cc = grid[i][j]
                if cc in singletons:
                    pos_dict[cc] = (i, j)
        return pos_dict

    def find_stems(grid: List[List[int]]) -> List[Tuple[int, int, int, int]]:
        runs = []
        for col in range(w):
            i = 0
            while i < h:
                val = grid[i][col]
                if val == 1 or val == 2:
                    cl = val
                    start_i = i
                    i += 1
                    while i < h and grid[i][col] == cl:
                        i += 1
                    length = i - start_i
                    if length >= 4:
                        runs.append((start_i, i, col, cl))
                else:
                    i += 1
        return runs

    def process_top_patterns(grid: List[List[int]], s1: int, s2: int, s3: int, singletons: List[int], pos: Dict[int, Tuple[int, int]]):
        for sk in [s1, s2, s3]:
            if sk not in pos or pos[sk][0] != 0:
                continue
            _, c = pos[sk]
            pat_colors = [s3, s2, s1]
            if sk == s1:
                pat_cols = [c - 4, c - 2, c]
            elif sk == s2:
                pat_cols = [c - 2, c, c + 2]
            elif sk == s3:
                pat_cols = [c, c + 2, c + 4]
            else:
                continue
            if not all(0 <= cc < w for cc in pat_cols):
                continue
            current_r = 0
            while current_r < h:
                can_fill = all(
                    0 <= pat_cols[ii] < w and (grid[current_r][pat_cols[ii]] == 8 or grid[current_r][pat_cols[ii]] == pat_colors[ii])
                    for ii in range(3)
                )
                if not can_fill:
                    break
                for ii in range(3):
                    cc = pat_cols[ii]
                    if grid[current_r][cc] == 8:
                        grid[current_r][cc] = pat_colors[ii]
                current_r += 1

    def process_bottom_patterns(grid: List[List[int]], s1: int, s2: int, s3: int, singletons: List[int], pos: Dict[int, Tuple[int, int]]):
        for sk in [s1, s2, s3]:
            if sk not in pos or pos[sk][0] != h - 1:
                continue
            _, c = pos[sk]
            pat_colors = [s1, s2, s3]
            if sk == s1:
                pat_cols = [c, c + 1, c + 4]
            elif sk == s2:
                pat_cols = [c - 1, c, c + 3]
            elif sk == s3:
                pat_cols = [c - 4, c - 3, c]
            else:
                continue
            if not all(0 <= cc < w for cc in pat_cols):
                continue
            current_r = h - 1
            while current_r >= 0:
                can_fill = all(
                    0 <= pat_cols[ii] < w and (grid[current_r][pat_cols[ii]] == 8 or grid[current_r][pat_cols[ii]] == pat_colors[ii])
                    for ii in range(3)
                )
                if not can_fill:
                    break
                for ii in range(3):
                    cc = pat_cols[ii]
                    if grid[current_r][cc] == 8:
                        grid[current_r][cc] = pat_colors[ii]
                current_r -= 1

    def process_middle_extensions(grid: List[List[int]], singletons: List[int], pos: Dict[int, Tuple[int, int]]):
        for sk in singletons:
            if sk not in pos:
                continue
            r, c = pos[sk]
            if r == 0 or r == h - 1:
                continue
            # left
            j = c - 1
            while j >= 0 and grid[r][j] == 8:
                grid[r][j] = sk
                j -= 1
            # right
            j = c + 1
            while j < w and grid[r][j] == 8:
                grid[r][j] = sk
                j += 1

    def process_stems(grid: List[List[int]], s1: int, s2: int, s3: int, stems: List[Tuple[int, int, int, int]]):
        for stem in stems:
            sr, er, c, typ = stem
            length = er - sr
            adjacent = None
            for other in stems:
                if other is stem:
                    continue
                osr, oer, oc, otyp = other
                if otyp == 3 - typ and abs(oc - c) == 1 and max(sr, osr) < min(er, oer):
                    adjacent = other
                    break
            if adjacent is not None:
                osr, oer, oc, otyp = adjacent
                other_len = oer - osr
                if length < other_len:
                    continue
                overlap_start = max(sr, osr)
                overlap_end = min(er, oer)
                ol_len = overlap_end - overlap_start
                if ol_len < 3:
                    continue
                offsets = [0, 1, ol_len // 2]
                if typ == 1:
                    colors = [s1, s2, s3]
                else:
                    colors = [s3, s2, s1]
                # direction away
                if oc < c:
                    # right
                    start_j = c + 1
                    step = 1
                    bound = w
                else:
                    # left
                    start_j = c - 1
                    step = -1
                    bound = 0
                    if step == -1:
                        start_j = c - 1
                        bound = 0
                for i, off in enumerate(offsets):
                    fill_row = overlap_start + off
                    if fill_row >= h:
                        continue
                    fill_color = colors[i]
                    j = start_j
                    while (step == 1 and j < bound) or (step == -1 and j >= bound):
                        if grid[fill_row][j] != 8:
                            break
                        grid[fill_row][j] = fill_color
                        j += step
            else:
                # isolated
                if typ == 1:
                    offsets = [1, 3, 5]
                    colors = [s1, s2, s3]
                else:
                    offsets = [0, length // 2, length - 2]
                    colors = [s3, s2, s1]
                unique_offsets = sorted(set(off for off in offsets if 0 <= off < length))
                num = len(unique_offsets)
                col_list = colors[:num]
                for ii, off in enumerate(unique_offsets):
                    fill_row = sr + off
                    if fill_row >= h:
                        continue
                    fill_color = col_list[ii]
                    # normal fills left and right
                    for dirr in [-1, 1]:
                        j = c + dirr
                        while 0 <= j < w and grid[fill_row][j] == 8:
                            grid[fill_row][j] = fill_color
                            j += dirr
                    # special for type2 off==0
                    if typ == 2 and off == 0:
                        next_r = fill_row + 1
                        if next_r < h:
                            # left fill check reached
                            left_reached = False
                            left_reach_j = None
                            j = c - 1
                            temp_j = j
                            while 0 <= j < w and grid[fill_row][j] == 8:
                                j -= 1
                            if 0 <= j < w and grid[fill_row][j] == fill_color:
                                left_reached = True
                                left_reach_j = j
                            # right
                            right_reached = False
                            right_reach_j = None
                            j = c + 1
                            temp_j = j
                            while 0 <= j < w and grid[fill_row][j] == 8:
                                j += 1
                            if 0 <= j < w and grid[fill_row][j] == fill_color:
                                right_reached = True
                                right_reach_j = j
                            # now special fills
                            if right_reached:
                                for jj in range(c + 1, right_reach_j + 1):
                                    if 0 <= jj < w and grid[next_r][jj] == 8:
                                        grid[next_r][jj] = fill_color
                                # opposite left
                                if 0 <= c - 1 < w:
                                    grid[next_r][c - 1] = grid[fill_row][c - 1]
                            if left_reached:
                                for jj in range(left_reach_j, c):
                                    if 0 <= jj < w and grid[next_r][jj] == 8:
                                        grid[next_r][jj] = fill_color
                                # opposite right
                                if 0 <= c + 1 < w:
                                    grid[next_r][c + 1] = grid[fill_row][c + 1]

    # main logic
    counts = count_non_blanks(result)
    singletons_list = [c for c in counts if counts[c] == 1]
    if len(singletons_list) != 3:
        return result
    singletons_list.sort()
    s1, s2, s3 = singletons_list
    pos = find_singleton_positions(result, singletons_list)

    process_top_patterns(result, s1, s2, s3, singletons_list, pos)
    process_bottom_patterns(result, s1, s2, s3, singletons_list, pos)
    process_middle_extensions(result, singletons_list, pos)

    stems = find_stems(result)
    process_stems(result, s1, s2, s3, stems)

    return result
```