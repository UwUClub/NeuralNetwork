#!/usr/bin/env python3

import re
import random
import numpy as np
import pandas as pd

"""Constants for the pieces"""
KING = 1.0
QUEEN = 0.9
ROOK = 0.7
BISHOP = 0.5
KNIGHT = 0.3
PAWN = 0.1

"""Class representing a chess board"""
class Board:
    """Constructor of the board, takes a match as input"""
    def __init__(self, fen, res):
        self.res = [0.0, 0.0, 0.0, 0.0]
        if res == "white":
            self.res[0] = 1.0
        elif res == "black":
            self.res[1] = 1.0
        elif res == "pat":
            self.res[2] = 1.0
        else:
            self.res[3] = 1.0
        self.board = self.parseFen(fen)

    """Parse the FEN to get the board"""
    def parseFen(self, fen):
        board = []
        for row in fen.split("/"):
            board.append(self.parseRow(row))
        return board

    """Parse a row of the board"""
    def parseRow(self, fenRow):
        row = []
        for char in fenRow:
            if char.isdigit():
                for i in range(int(char)):
                    row.append(".")
            else:
                row.append(char)
        return row

    """Print the board with the result and the checkmate"""
    def __str__(self) -> str:
        res = ""
        res += "RES: {}\n".format(self.res)
        for row in self.board:
            res += str(row) + "\n"
        return res

    """Return the board as a vector"""
    def toVector(self):
        vector: np.array = []
        for row in self.board:
            for col in row:
                if col == "K":
                    vector.append([KING])
                elif col == "Q":
                    vector.append([QUEEN])
                elif col == "R":
                    vector.append([ROOK])
                elif col == "B":
                    vector.append([BISHOP])
                elif col == "N":
                    vector.append([KNIGHT])
                elif col == "P":
                    vector.append([PAWN])
                elif col == "k":
                    vector.append([-KING])
                elif col == "q":
                    vector.append([-QUEEN])
                elif col == "r":
                    vector.append([-ROOK])
                elif col == "b":
                    vector.append([-BISHOP])
                elif col == "n":
                    vector.append([-KNIGHT])
                elif col == "p":
                    vector.append([-PAWN])
                else:
                    vector.append([0.0])
        return np.array(vector)

"""Class to parse the data from a file"""
class DataParser:
    """Constructor of the parser, takes the path to the file as input"""
    def __init__(self, configPath):
        self.matches = pd.read_csv(configPath, sep=";")
        fen = self.matches["FEN"]
        res = self.matches["RES"]
        self.boards = []
        for i in range(len(self.matches)):
            self.boards.append(Board(fen[i], res[i]))

        random.shuffle(self.boards)

    def getNbrBoards(self):
        return len(self.boards)

    """Make a random batch of boards"""
    def makeRandomBatch(self, batchSize):
        batch = []
        for i in range(batchSize):
            batch.append(self.takeRandomBoard())
        return batch

    """Take a random board from the current batch"""
    def takeRandomBoard(self):
        board = random.choice(self.boards)
        self.boards.remove(board)
        return board
