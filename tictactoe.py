#! /usr/bin/env python3

import os
import sys
import random
from itertools import compress

wins = ((1, 1, 1, 0, 0, 0, 0, 0, 0), (0, 0, 0, 1, 1, 1, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 1, 1, 1), (1, 0, 0, 1, 0, 0, 1, 0, 0),
        (0, 1, 0, 0, 1, 0, 0, 1, 0), (0, 0, 1, 0, 0, 1, 0, 0, 1),
        (1, 0, 0, 0, 1, 0, 0, 0, 1), (0, 0, 1, 0, 1, 0, 1, 0, 0))

porks = {('O', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'): (2, 6),
         (' ', ' ', 'O', ' ', 'X', ' ', 'X', ' ', ' '): (0, 8),
         ('X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'O'): (2, 6),
         (' ', ' ', 'X', ' ', 'X', ' ', 'O', ' ', ' '): (0, 8),
         ('X', ' ', ' ', ' ', 'O', ' ', ' ', ' ', 'X'): (1, 3, 5, 7),
         (' ', ' ', 'X', ' ', 'O', ' ', 'X', ' ', ' '): (1, 3, 5, 7),
         (' ', 'X', ' ', ' ', 'O', 'X', ' ', ' ', ' '): (0, 2, 8),
         (' ', ' ', ' ', ' ', 'O', 'X', ' ', 'X', ' '): (2, 6, 8),
         (' ', ' ', ' ', 'X', 'O', ' ', ' ', 'X', ' '): (0, 6, 8),
         (' ', 'X', ' ', 'X', 'O', ' ', ' ', ' ', ' '): (0, 2, 6),
         ('X', ' ', ' ', ' ', 'O', ' ', ' ', 'X', ' '): (5, 6),
         (' ', ' ', 'X', ' ', 'O', ' ', ' ', 'X', ' '): (3, 8),
         (' ', 'X', ' ', ' ', 'O', ' ', ' ', ' ', 'X'): (2, 3),
         (' ', 'X', ' ', ' ', 'O', ' ', 'X', ' ', ' '): (0, 5),
         ('X', ' ', ' ', ' ', 'O', 'X', ' ', ' ', ' '): (7, 2),
         (' ', ' ', ' ', ' ', 'O', 'X', 'X', ' ', ' '): (1, 8),
         (' ', ' ', 'X', 'X', 'O', ' ', ' ', ' ', ' '): (0, 7),
         (' ', ' ', ' ', 'X', 'O', ' ', ' ', ' ', 'X'): (1, 6)}


class TicTacToe:
    def __init__(self, order="XO"):
        self.__state = [' ' for _ in range(9)]
        self.__order = order

    @property
    def indxs(self):
        return [n for n, s in enumerate(self.state) if s == ' ']

    @property
    def state(self):
        return self.__state.copy()

    def is_full(self):
        return len(self) == 9

    def check(self, state=None):
        if not state:
            state = self.state
        for win in wins:
            s1, s2, s3 = compress(state, win)
            if s1 == s2 == s3 != " ":
                return s1

    def next_move(self):
        symbol = self.__order[len(self) % 2]
        if symbol == "X":
            index = self.__human_turn()
        else:
            index = self.__cpu_turn()
        if index in self.indxs:
            self.__state[index] = symbol

    def __cpu_turn(self):
        # opening
        if len(self) < 1:
            return random.choice((0, 2, 4, 6, 8))
        if len(self) < 3:
            if 4 in self.indxs:
                return 4
            return random.choice((0, 2, 6, 8))

        # check for win, or block
        state = self.state
        for symbol in "OX":
            for index in self.indxs:
                state[index] = symbol
                if self.check(state):
                    return index
                state[index] = " "

        # block potential fork, ... or choose whatever
        valid_moves = porks.get(tuple(state), self.indxs)
        return random.choice(valid_moves)

    def __human_turn(self):
        try:
            prompt = "        CHOOSE (ROW COL) : "
            row, col = map(int, input(prompt).split())
            if row in (1, 2, 3) and col in (1, 2, 3):
                return (3 * row + col) - 4
        except ValueError:
            pass

    def __len__(self):
        return 9 - len(self.indxs)

    def __repr__(self):
        return '''
          1   2   3
        ┌───┬───┬───┐
      1 │ {} │ {} │ {} │
        ├───┼───┼───┤
      2 │ {} │ {} │ {} │
        ├───┼───┼───┤
      3 │ {} │ {} │ {} │
        └───┴───┴───┘
        '''.format(*self.state)


def new_game(clrscr):
    while True:
        os.system(clrscr)
        first = input("\n  WANNA GO FIRST ? (Y/N) ")
        if first.upper() in ("Y", "N"):
            break

    # comp -> O, human -> X
    order = {"Y": "XO", "N": "OX"}.get(first.upper())
    board = TicTacToe(order)

    while True:
        os.system(clrscr)
        print(board)

        winner = board.check()
        if winner:
            print(f"\r         CONGRATS ({winner}) !\n")
            break

        if board.is_full():
            print(f"\r         POINTLESS ... \n")
            break

        board.next_move()


if __name__ == "__main__":
    try:
        new_game("cls" if "win" in sys.platform else "clear")
    except (KeyboardInterrupt, EOFError):
        sys.exit("\n")
