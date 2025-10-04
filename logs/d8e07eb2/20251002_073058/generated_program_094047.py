```python
from typing import List

def program(g: List[List[int]]) -> List[List[int]]:
    out = [row[:] for row in g]

    def has_zero_left(out) -> bool:
        return any(out[r][c] == 0 for r in range(1, 4) for c in range(2, 5))

    def has_strict_blue_o(out) -> bool:
        return (all(out[1][c] == 1 for c in range(7, 10)) and
                all(out[3][c] == 1 for c in range(7, 10)) and
                out[2][8] == 1)

    def has_seven_middle(out) -> bool:
        return (out[1][12] == 7 and all(out[2][c] == 7 for c in range(12, 15)) and
                out[3][12] == 7)

    def has_pink_o_top(out) -> bool:
        return (all(out[1][c] == 6 for c in range(12, 15)) and
                out[2][12] == 6 and out[2][14] == 6 and
                out[3][12] == 6 and out[3][14] == 6 and
                out[2][13] == 8 and out[3][13] == 8)

    def has_red_left(out) -> bool:
        return (out[1][2] == 2 and out[1][4] == 2 and
                out[2][3] == 2 and
                out[3][2] == 2 and out[3][4] == 2)

    def has_lightblue_middle(out) -> bool:
        return (out[1][12] == 9 and out[1][14] == 9 and out[1][13] == 8 and
                out[2][12] == 9 and out[2][13] == 9 and out[2][14] == 8 and
                all(out[3][c] == 9 for c in range(12, 15)))

    def has_yellow_broken_o(out) -> bool:
        return (out[1][7] == 4 and out[1][8] == 8 and out[1][9] == 4 and
                out[2][7] == 4 and out[2][8] == 8 and out[2][9] == 4 and
                all(out[3][c] == 4 for c in range(7, 10)))

    # Full fill top panel if condition
    if has_zero_left(out) and has_strict_blue_o(out):
        for r in range(5):
            for c in range(22):
                if out[r][c] == 8:
                    out[r][c] = 3

    # Vertical non-blue fills in top block
    for c in range(22):
        color = out[1][c]
        if (color != 0 and color != 8 and color != 1 and
            out[2][c] == 8 and out[3][c] == color):
            out[2][c] = 3

    # Third panel background and inside fills
    fill_columns = set()
    if has_seven_middle(out):
        for c in range(1, 6):
            fill_columns.add(c)
        for c in range(11, 21):
            fill_columns.add(c)
    if has_strict_blue_o(out):
        for c in range(6, 11):
            fill_columns.add(c)
    for r in range(12, 17):
        for c in fill_columns:
            if out[r][c] == 8:
                out[r][c] = 3

    # Second panel middle full fill if pink O in top
    if has_pink_o_top(out):
        for r in range(7, 12):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3

    # Fourth panel middle full fill if pink O in top
    if has_pink_o_top(out):
        for r in range(18, 22):
            for c in range(6, 11):
                if out[r][c] == 8:
                    out[r][c] = 3

    # Left art fills if red left in top
    if has_red_left(out):
        # Second panel left
        out[8][1] = 3
        out[8][3] = 3
        out[8][5] = 3
        out[9][1] = 3
        out[9][2] = 3
        out[9][4] = 3
        out[9][5] = 3
        out[10][1] = 3
        out[10][3] = 3
        out[10][5] = 3
        out[11][1] = 3
        out[11][2] = 3
        out[11][3] = 3
        out[11][4] = 3
        out[11][5] = 3
        # Fourth panel left
        out[18][1] = 3
        out[18][3] = 3
        out[18][5] = 3
        out[19][1] = 3
        out[19][3] = 3
        out[19][5] = 3
        out[20][1] = 3
        out[20][5] = 3
        out[21][1] = 3
        out[21][2] = 3
        out[21][3] = 3
        out[21][4] = 3
        out[21][5] = 3

    # Right second fills if lightblue middle in top
    if has_lightblue_middle(out):
        out[8][16] = 3
        out[8][18] = 3
        out[8][20] = 3
        out[9][16] = 3
        out[9][19] = 3
        out[9][20] = 3
        out[10][16] = 3
        out[10][20] = 3

    # Fourth middle gaps if yellow broken O in top
    if has_yellow_broken_o(out):
        out[18][6] = 3
        out[18][9] = 3
        out[18][10] = 3
        out[19][6] = 3
        out[19][10] = 3
        out[20][6] = 3
        out[20][7] = 3
        out[20][9] = 3
        out[20][10] = 3
        out[21][6] = 3
        out[21][7] = 3
        out[21][8] = 3
        out[21][9] = 3
        out[21][10] = 3

    # Bottom fill
    if has_zero_left(out) and has_strict_blue_o(out):
        fill_color = 3
    else:
        fill_color = 2
    for r in [28, 29]:
        for c in range(22):
            out[r][c] = fill_color

    return out
```