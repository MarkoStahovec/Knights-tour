import random
import sys
import time

sys.setrecursionlimit(100000)
ROUNDS = 0  # number of rounds as to how many different solutions are desired
start_coords = []  # holds array of all starting coordinates to feed the algorithm
turn = 0  # this variable holds a number of turns in order to terminate a program is a certain threshold is exceeded


# find a solution by making moves on a board using Warndorffs rule
def jump(number, row, col, board, moves, run):
    global turn
    turn += 1
    if turn == 4000000:  # if maximum turns is reached
        end = time.time()
        print(f"Time elapsed: {end - start}")
        if run == ROUNDS - 1:  # condition to ensure to run the program multiple times
            exit(5)
        else:
            place_knight(len(board), start_coords[run + 1][1], start_coords[run + 1][0],
                         run + 1)  # rerun with new coords
        # exit(1)
    board[row][col] = number  # write a move into the board

    if number == len(board) ** 2:  # if solution was found
        for i in range(len(board)):
            for j in range(len(board[i])):
                print(board[i][j], end="\t")
            print()
        print()
        if run == ROUNDS - 1:  # condition to ensure to run the program multiple times
            end = time.time()
            print(f"Time elapsed: {end - start}")
            exit(4)
        else:
            place_knight(len(board), start_coords[run + 1][1], start_coords[run + 1][0],
                         run + 1)  # rerun with new coords
    else:  # if we are not yet at the end
        poss = []
        for mov in moves:  # look for next possible move
            new_row = row + mov[0]
            new_col = col + mov[1]
            if 0 <= new_row < len(board) and 0 <= new_col < len(board) and board[new_row][new_col] is None:
                poss.append([mov[0], mov[1]])

        exits = [0] * len(poss)
        for i in range(0, len(poss)):  # evaluate moves using Warndorffs rule by counting their exits from the next move
            valid = 0
            for mov in moves:  # try all the 2 moves ahead
                fir_row = row + poss[i][0]
                fir_col = col + poss[i][1]
                new_row = fir_row + mov[0]
                new_col = fir_col + mov[1]
                if 0 <= new_row < len(board) and 0 <= new_col < len(board) and board[new_row][new_col] is None:
                    valid += 1
            exits[i] = valid

        bst_moves = {repr(poss[i]): exits[i] for i in range(len(poss))}  # make a dictionary out of possible moves
        # mvs = dict(sorted(bst_moves.items(), key=lambda item: item[0]))
        sorted_moves = sorted(bst_moves.items(), key=lambda kv: kv[1])  # and sort them so the best option is picked

        for mov in sorted_moves:  # cycle through best moves and pick the next best, also backtracking happens here
            res = mov[0].strip('][').split(', ')
            new_row = row + int(res[0])
            new_col = col + int(res[1])
            if 0 <= new_row < len(board) and 0 <= new_col < len(board) and board[new_row][new_col] is None:
                jump(number + 1, new_row, new_col, board, moves, run)  # make a move or backtrack into another move

    board[row][col] = None  # if no proper move is found, we put None and go one move back using backtrack


def place_knight(size, x, y, run):  # menu for an algorithm
    global turn
    turn = 0  # reset for number of turns
    print(f"--------------------------------------------\n{run + 1}\n--------------------------------------------")
    board = [[None] * size for i in range(size)]  # fill the board with None
    # moves = [[2, 1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [-1, -2], [1, -2], [2, -1]]  # list of all possible moves
    moves = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
    jump(1, x, y, board, moves, run)  # start


if __name__ == '__main__':
    while True:
        choice = int(input("Insert board size: "))
        if choice <= 4:
            continue
        else:
            break
    while True:
        ROUNDS = int(input("How many times do you want to run the program? "))
        if ROUNDS <= 0:
            continue
        else:
            break
    while True:
        manual_coords = input("Insert coordinates manually? [y/n] ")
        x = y = 0

        # x = int(input("Insert x coordinate: "))
        # y = int(input("Insert y coordinate: "))

        if manual_coords == "n":
            while len(start_coords) != ROUNDS:  # generate n different coords
                x = random.randint(0, choice - 1)
                y = random.randint(0, choice - 1)
                if [x, y] not in start_coords:
                    start_coords.append([x, y])
        elif manual_coords == "y":
            while len(start_coords) != ROUNDS:  # generate n different coords yourself
                x = int(input("Insert x coordinate: "))
                y = int(input("Insert y coordinate: "))
                if [x, y] not in start_coords:
                    start_coords.append([x, y])
        else:
            continue

        break

    # start_coords[0][1] = 2
    # start_coords[0][0] = 2

    start = time.time()
    place_knight(choice, start_coords[0][1], start_coords[0][0], 0)  # initiate with first coords
    end = time.time()
    print(f"Time elapsed: {end - start}")
    print(f"\nTerminating")

