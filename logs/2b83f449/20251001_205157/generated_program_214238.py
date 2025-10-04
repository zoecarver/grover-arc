```python
def program(g: List[List[int]]) -> List[List[int]]:
    if not g:
        return []
    height = len(g)
    width = len(g[0])
    output = [[0] * width for _ in range(height)]
    # Compute pink positions per row
    pink_per_row = [[] for _ in range(height)]
    for r in range(1, height, 2):
        centers = []
        j = 0
        while j < width - 2:
            if g[r][j:j+3] == [7, 7, 7]:
                centers.append(j + 1)
                j += 3
            else:
                j += 1
        start_y = (r // 2) * 2
        for dy in range(3):
            y = start_y + dy
            if y < height:
                for c in centers:
                    if c not in pink_per_row[y]:
                        pink_per_row[y].append(c)
    # Handle odd rows
    for r in range(1, height, 2):
        row_out = []
        j = 0
        while j < width:
            if j < width - 2 and g[r][j:j+3] == [7, 7, 7]:
                row_out += [8, 6, 8]
                j += 3
            else:
                row_out.append(g[r][j])
                j += 1
        output[r] = row_out
    # Find last_red
    last_red = -1
    for rr in range(1, height, 2):
        if 7 in g[rr]:
            last_red = rr
    last_start = (last_red // 2) * 2 if last_red != -1 else -2
    last_end = last_start + 2 if last_red != -1 else -2
    # Handle even rows
    for r in range(0, height, 2):
        row_out = [8] * width
        num_zeros = 0
        zero_positions = []
        for j in range(width):
            if g[r][j] == 0:
                row_out[j] = 0
                num_zeros += 1
                zero_positions.append(j)
        # Place pinks
        for c in pink_per_row[r]:
            row_out[c] = 6
        # Now place 3's
        if r == 0:
            # Special: no 3's
            pass
        else:
            if num_zeros == 0 and r >= 2:
                # No zeros case: double if condition
                prev_r = r - 1
                prev_centers = []
                j = 0
                while j < width - 2:
                    if g[prev_r][j:j+3] == [7, 7, 7]:
                        prev_centers.append(j + 1)
                        j += 3
                    else:
                        j += 1
                if prev_centers:
                    l_min = min(prev_centers)
                    r_max = max(prev_centers)
                    if l_min <= 4:
                        row_out[0] = 3
                        if width > 1:
                            row_out[1] = 3
                    if r_max >= width - 5:
                        if width > 1:
                            row_out[width - 2] = 3
                        row_out[width - 1] = 3
                # Special for last end no zeros middle
                if r == last_end and prev_centers:
                    l_min = min(prev_centers)
                    r_max = max(prev_centers)
                    if l_min > 4 and r_max < width - 5:
                        row_out[0] = 3
                        row_out[width - 1] = 3
            else:
                # Has zeros or special, apply segment rules
                # Find all segments with 6
                segs = []
                j = 0
                while j < width:
                    if row_out[j] != 0:
                        s = j
                        has6_seg = False
                        while j < width and row_out[j] != 0:
                            if row_out[j] == 6:
                                has6_seg = True
                            j += 1
                        e = j - 1
                        if has6_seg:
                            segs.append((s, e))
                    else:
                        j += 1
                # Process left and right for segs
                for s, e in segs:
                    # left
                    if s == 0:
                        row_out[s] = 3
                    elif s > 0 and row_out[s - 1] == 0:
                        row_out[s] = 3
                    # right before 0
                    if e < width - 1 and row_out[e + 1] == 0:
                        # find last6
                        last6_pos = e
                        while last6_pos >= s and row_out[last6_pos] != 6:
                            last6_pos -= 1
                        if last6_pos >= s:  # found
                            gap = e - last6_pos
                            if gap >= 3:
                                row_out[e] = 3
                # Handle last segment for end
                # First, set if last seg has6 and e == width-1
                rightmost_e = -1
                rightmost_has6 = False
                for s, e in segs:
                    if e > rightmost_e:
                        rightmost_e = e
                        rightmost_has6 = True
                if rightmost_e == width - 1 and rightmost_has6:
                    row_out[width - 1] = 3
                # Extra for trailing seg without 6 after 0, if prev has6
                j = width - 1
                trailing_has6 = False
                while j >= 0 and row_out[j] != 0:
                    if row_out[j] == 6:
                        trailing_has6 = True
                    j -= 1
                if j >= 0 and row_out[j] == 0 and not trailing_has6:
                    # check if any 6 left of j inclusive? but since trailing no, left of the 0
                    has_prev6 = False
                    for k in range(j):
                        if row_out[k] == 6:
                            has_prev6 = True
                            break
                    if has_prev6:
                        row_out[width - 1] = 3
        output[r] = row_out
    return output
```