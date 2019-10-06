#! /usr/bin/env python3

import os
import sys
import random
from itertools import compress

wins = ((1, 1, 1, 0, 0, 0, 0, 0, 0), (0, 0, 0, 1, 1, 1, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 1, 1, 1), (1, 0, 0, 1, 0, 0, 1, 0, 0),
        (0, 1, 0, 0, 1, 0, 0, 1, 0), (0, 0, 1, 0, 0, 1, 0, 0, 1),
        (1, 0, 0, 0, 1, 0, 0, 0, 1), (0, 0, 1, 0, 1, 0, 1, 0, 0))


class TicTacToe:
    def __init__(self, order="OX"):
        self.__order = order
        self.__state = [' '] * 9
        self.__indxs = list(range(9))

    def is_full(self):
        return len(self.__indxs) == 0

    def check(self, state=None):
        if not state:
            state = self.__state.copy()
        for win in wins:
            s1, s2, s3 = compress(state, win)
            if s1 == s2 == s3 != " ":
                return s1

    def minimax(self, state, is_maxing):
        res = self.check(state)
        if res:
            return {"O": 10, "X": -10}.get(res)

        indxs = [n for n, s in enumerate(state) if s == ' ']
        if not indxs:
            return 0

        if is_maxing:
            best = -1000
            for index in indxs:
                state[index] = "O"
                best = max(best, self.minimax(state, not is_maxing))
                state[index] = " "
        else:
            best = 1000
            for index in indxs:
                state[index] = "X"
                best = min(best, self.minimax(state, not is_maxing))
                state[index] = " "

        return best

    def __cpu_turn(self):
        if len(self.__indxs) > 8:
            return random.choice(self.__indxs)

        best_move, best_value = -1, -1000
        state = self.__state.copy()

        for index in self.__indxs:
            state[index] = "O"
            move_value = self.minimax(state, False)
            state[index] = " "
            if move_value > best_value:
                best_value = move_value
                best_move = index

        return best_move

    def __human_turn(self):
        try:
            prompt = "        CHOOSE (ROW COL) : "
            row, col = map(int, input(prompt).split())
            if row in (1, 2, 3) and col in (1, 2, 3):
                return (3 * row + col) - 4
        except ValueError:
            pass

    def next_move(self):
        symbol = self.__order[len(self.__indxs) % 2]
        index = {"X": self.__human_turn, "O": self.__cpu_turn}.get(symbol)()
        if index in self.__indxs:
            self.__state[index] = symbol
            self.__indxs.remove(index)

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
        '''.format(*self.__state)


def new_game():
    while True:
        os.system("clear")
        first = input("\n  WANNA GO FIRST ? (Y/N) ")
        if first.upper() in ("Y", "N"):
            break

    # comp -> O, human -> X
    order = {"Y": "OX", "N": "XO"}.get(first.upper())
    board = TicTacToe(order)

    while True:
        os.system("clear")
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
        new_game()
    except (KeyboardInterrupt, EOFError):
        sys.exit("\n")
