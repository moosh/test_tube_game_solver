# Test tube pouring game analysis

import re
import numpy as np
import networkx as nx
from collections import deque

YELLOW = "a"
ORANGE = "b"
GRAY = "c"
LT_GREEN = "d"
LT_BLUE = "e"
OLIVE_GREEN = "f"
PURPLE = "g"
RED = "h"
PINK = "i"
BROWN = "j"
DK_BLUE = "k"
DK_GREEN = "m"
COLORS = [
    YELLOW,
    ORANGE,
    GRAY,
    LT_GREEN,
    LT_BLUE,
    OLIVE_GREEN,
    PURPLE,
    RED,
    PINK,
    BROWN,
    DK_BLUE,
    DK_GREEN,
]

# NUM_TUBES = 5
# TUBE_VOLUME = 4
# COLORS = ["y", "r", "b"]
# STARTING_TEST1 = "yyrb,ryrr,bbby,,"

# NUM_TUBES = 6
# TUBE_VOLUME = 4
# COLORS = ["r", "b", "y", "g"]
# STARTING_TEST2 = "yrrr,gbyy,gryb,bbgg,,"

# NUM_TUBES = 14
# TUBE_VOLUME = 4
# COLORS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m"]
# STARTING_LEVEL_105 = "aafb,cegh,ijhk,kjgk,bmjf,fifm,djhi,dghd,bace,ecmi,bdmc,kgae,,"

## Level 107
# NUM_TUBES = 14
# TUBE_VOLUME = 4
# TUBES = [
#     str(YELLOW + ORANGE + GRAY + LT_GREEN),
#     str(LT_BLUE + OLIVE_GREEN + PURPLE + RED),
#     str(PURPLE + LT_GREEN + PINK + OLIVE_GREEN),
#     str(BROWN + RED + PINK + YELLOW),
#     str(PURPLE + BROWN + DK_BLUE + OLIVE_GREEN),
#     str(YELLOW + PURPLE + GRAY + OLIVE_GREEN),
#     str(DK_GREEN + LT_BLUE + GRAY + ORANGE),
#     str(PINK + LT_BLUE + DK_GREEN + RED),
#     str(LT_GREEN + LT_BLUE + DK_BLUE + DK_BLUE),
#     str(ORANGE + PINK + BROWN + DK_GREEN),
#     str(ORANGE + YELLOW + LT_GREEN + GRAY),
#     str(DK_BLUE + DK_GREEN + BROWN + RED),
#     "",
#     "",
# ]

# Level 145
# NUM_TUBES = 14
# TUBE_VOLUME = 4
# TUBES = [
#     str(BROWN + LT_GREEN + DK_BLUE + GRAY),
#     str(DK_GREEN + RED + RED + DK_GREEN),
#     str(PINK + DK_BLUE + OLIVE_GREEN + LT_BLUE),
#     str(OLIVE_GREEN + GRAY + BROWN + ORANGE),
#     str(DK_BLUE + ORANGE + LT_BLUE + PURPLE),
#     str(YELLOW + YELLOW + LT_GREEN + LT_BLUE),
#     str(OLIVE_GREEN + DK_BLUE + PURPLE + GRAY),
#     str(PINK + RED + DK_GREEN + ORANGE),
#     str(LT_BLUE + YELLOW + GRAY + BROWN),
#     str(PURPLE + PINK + BROWN + OLIVE_GREEN),
#     str(RED + LT_GREEN + DK_GREEN + PURPLE),
#     str(YELLOW + ORANGE + LT_GREEN + PINK),
#     "",
#     "",
# ]

# Level 159
NUM_TUBES = 14
TUBE_VOLUME = 4
TUBES = [
    str(BROWN + ORANGE + GRAY + BROWN),
    str(PURPLE + LT_BLUE + OLIVE_GREEN + PINK),
    str(RED + ORANGE + OLIVE_GREEN + GRAY),
    str(PINK + BROWN + RED + DK_BLUE),
    str(DK_GREEN + DK_BLUE + YELLOW + ORANGE),
    str(DK_BLUE + ORANGE + LT_GREEN + YELLOW),
    str(LT_BLUE + LT_GREEN + LT_GREEN + DK_BLUE),
    # row 2
    str(OLIVE_GREEN + DK_GREEN + PURPLE + PINK),
    str(YELLOW + DK_GREEN + LT_GREEN + OLIVE_GREEN),
    str(LT_BLUE + BROWN + GRAY + PURPLE),
    str(LT_BLUE + GRAY + PURPLE + DK_GREEN),
    str(PINK + RED + RED + YELLOW),
    "",
    "",
]

STARTING_GAME_STATE = ""
for tube in TUBES:
    STARTING_GAME_STATE += tube + ","
STARTING_GAME_STATE = STARTING_GAME_STATE[:-1]

print("foo")


def main():
    game_over_win = False
    game_graph = nx.DiGraph()
    game_visited = set()  # the set of all moves made, to avoid dupes
    game_stack = deque()
    game_stack.append(STARTING_GAME_STATE)
    game_visited.add(STARTING_GAME_STATE)
    dd = 0
    while len(game_stack) > 0 and not game_over_win:
        stack_progress = int(len(game_stack))
        print("." * stack_progress)

        game_state = game_stack.pop()
        for i in range(0, NUM_TUBES):
            for j in range(0, NUM_TUBES):
                if i == j:
                    continue
                can_pour, next_state = pour(game_state, i, j)
                if next_state not in game_visited:
                    game_visited.add(next_state)
                    game_stack.append(next_state)
                    game_graph.add_edge(game_state, next_state, pour=f"{i+1},{j+1}")
                game_over_win = is_game_over(next_state)

    if game_over_win is True:
        game_path = nx.algorithms.dag_longest_path(game_graph)
        print(f"Game Over. Winning path exists in {len(game_path)} moves")
        for i in range(0, len(game_path) - 1):
            edge = game_graph[game_path[i]][game_path[i + 1]]
            print(f"{edge['pour']} {game_path[i]}")
    else:
        print(f"Game Over. NO winning path found :-/")


def is_game_over(in_game_state: str) -> bool:
    game_array = str_to_array(in_game_state)
    out_game_over = True
    for tube in game_array:
        if len(tube) == 0:
            continue

        for letter in COLORS:
            count = tube.count(letter)
            # check if letter is spread out among multiple tubes
            if 0 < count < len(tube):
                out_game_over = False
                break
        if out_game_over is False:
            break

    return out_game_over


# returns (can pour, updated game state)
def pour(in_game_state, from_tube_idx, to_tube_idx) -> (bool, str):
    game_array = str_to_array(in_game_state)

    from_tube = game_array[from_tube_idx]
    to_tube = game_array[to_tube_idx]
    can_pour = False

    # from_tube has letters AND
    # to_tube is empty OR to_tube has same letter

    while True:
        if len(game_array[from_tube_idx]) == 0:
            break  # Nothing to pour

        if len(game_array[to_tube_idx]) == TUBE_VOLUME:
            break  # Don't pour into a full tube

        # Don't pour into a tube with an unlike color at the top
        if (
            len(game_array[to_tube_idx]) > 0
            and game_array[from_tube_idx][-1] != game_array[to_tube_idx][-1]
        ):
            break

        # Don't pour a solo color from its tube to another empty tube
        letter = game_array[from_tube_idx][-1]
        if (
            game_array[from_tube_idx].count(letter) == len(game_array[from_tube_idx])
            and len(game_array[to_tube_idx]) == 0
        ):
            break

        # Don't pour if not all the color moves to the destination tube
        pourable = pourable_count(game_array[from_tube_idx])
        if TUBE_VOLUME - len(game_array[to_tube_idx]) < pourable:
            break

        can_pour = True
        char_to_move = game_array[from_tube_idx][-1]
        game_array[from_tube_idx] = game_array[from_tube_idx][:-1]
        game_array[to_tube_idx] += char_to_move

    return can_pour, array_to_str(game_array)


def pourable_count(in_array: []):
    # Returns the number of items of the same color are at the top of the tube
    out_count = 0
    if len(in_array) == 0:
        return 0
    letter = in_array[-1]
    out_count += 1

    for i in range(2, len(in_array) + 1):  # use NEGATIVE of the range
        if in_array[-i] == letter:
            out_count += 1
        else:
            break

    return out_count


def array_to_str(in_array: []) -> str:
    out_str = np.array2string(np.array(in_array), separator=",")
    out_str = re.sub("['\[\] \n]", "", out_str)
    return out_str


def str_to_array(in_rack: str) -> np.array:
    return in_rack.split(",")


def enumerate_moves(in_tubes):
    for idx, tube in enumerate(in_tubes):
        last_char = tube[-1]
        idx = -2
        while tube[idx] == last_char:
            idx -= 1
        chars_to_move = -1 - idx

        # can we fit chars_to_mov


if __name__ == "__main__":
    main()
