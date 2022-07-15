# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.9 Beta
Licensed under {License info} for general use with attribution.
For works using this code please cite:
    Sandborn, D.E., Minor E.C., Hill, C. (2022)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from utils.conversions import mV_to_pH, pH_to_mV
from sklearn import linear_model
from sklearn.metrics import r2_score

def gran_plot(datasheet, mass, k, Eo):
    """
    Plots diagnostic titration figures.  Matplotlib backend.

    Parameters
    ----------
    datasheet : TYPE
        DESCRIPTION.
    mass : TYPE
        DESCRIPTION.
    k : TYPE
        DESCRIPTION.
    Eo : TYPE
        DESCRIPTION.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    datasheet = datasheet.drop([0])  # drop first filler row
    datasheet['x'] = datasheet.Vol
    datasheet['y'] = (mass+datasheet.Vol) * \
        10**(-mV_to_pH(datasheet.mV, Eo, k, datasheet.TC))  # gran function
    for i in datasheet.index:
        datasheet.loc[i, 'pH'] = mV_to_pH(datasheet.loc[i, 'mV'], Eo, k, datasheet.loc[i, 'TC'])
    regr = linear_model.LinearRegression()
    regr.fit(np.array(datasheet.x).reshape(-1, 1), np.array(datasheet.y))
    datasheet['y_pred'] = regr.predict(np.array(datasheet.x).reshape(-1, 1))
    r2 = round(r2_score(datasheet.y, datasheet.y_pred), 4)
    fig, axs = plt.subplots(3,1)
    scatter = axs[0].scatter(datasheet.x, datasheet.y, c = datasheet.TC, cmap = 'winter')
    axs[0].plot(datasheet.x, datasheet.y_pred, ls = ':', c = 'k')
    axs[0].set_ylabel('Gran Function')
    axs[0].annotate('$r^2$ = ' +str(r2), xy = ((datasheet.x.min()+datasheet.x.mean())/2, (datasheet.y.max()+datasheet.y.mean())/2))
    plt.colorbar(scatter, ax = axs[0])
    resid = axs[1].scatter(datasheet.x, datasheet.y-datasheet.y_pred, c = datasheet.TC, cmap = 'winter')
    axs[1].axhline(y = 0, c = 'k', ls = ':')
    axs[1].set_ylabel('Gran Function Residuals')
    axs[1].set_ylim([-0.001,0.001])
    axs[1].fill_between(datasheet.x, datasheet.y-datasheet.y_pred, color = 'k', alpha = 0.1)
    plt.colorbar(resid, ax = axs[1])
    titrate = axs[2].scatter(datasheet.x, datasheet.pH, c = datasheet.TC, cmap = 'winter')
    plt.colorbar(titrate, ax = axs[2])
    axs[2].set_xlabel('Titrant Volume (mL)')
    axs[2].set_ylabel('pH')
    fig.tight_layout()
    return fig



class TicTacToe:

    def __init__(self):
        self.board = []

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

    def get_random_first_player(self):
        return random.randint(0, 1)

    def fix_spot(self, row, col, player):
        self.board[row][col] = player

    def is_player_win(self, player):
        win = None

        n = len(self.board)

        # checking rows
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[i][j] != player:
                    win = False
                    break
            if win:
                return win

        # checking columns
        for i in range(n):
            win = True
            for j in range(n):
                if self.board[j][i] != player:
                    win = False
                    break
            if win:
                return win

        # checking diagonals
        win = True
        for i in range(n):
            if self.board[i][i] != player:
                win = False
                break
        if win:
            return win

        win = True
        for i in range(n):
            if self.board[i][n - 1 - i] != player:
                win = False
                break
        if win:
            return win
        return False

        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def is_board_filled(self):
        for row in self.board:
            for item in row:
                if item == '-':
                    return False
        return True

    def swap_player_turn(self, player):
        return 'X' if player == 'O' else 'O'

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def start(self):
        self.create_board()

        player = 'X' if self.get_random_first_player() == 1 else 'O'
        while True:
            print(f"Player {player} turn")

            self.show_board()

            # taking user input
            row, col = list(
                map(int, input("Enter row number [space] column number to choose spot: ").split()))
            print()

            # fixing the spot
            self.fix_spot(row - 1, col - 1, player)

            # checking whether current player is won or not
            if self.is_player_win(player):
                print(f"Player {player} wins the game!")
                break

            # checking whether the game is draw or not
            if self.is_board_filled():
                print("A strange game. The only winning move is not to play.")
                break

            # swapping the turn
            player = self.swap_player_turn(player)

        # showing the final view of board
        print()
        self.show_board()


# starting the game
#tic_tac_toe = TicTacToe()
#tic_tac_toe.start()