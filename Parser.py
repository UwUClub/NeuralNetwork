#!/usr/bin/env python3

import re
import random
import numpy as np

"""Constants for the pieces"""
KING = 1.0
QUEEN = 0.9
ROOK = 0.5
BISHOP = 0.3
KNIGHT = 0.3
PAWN = 0.1

"""Class representing a chess board"""
class Board:
    """Constructor of the board, takes a match as input"""
    def __init__(self, match):
        self.board = [["." for i in range(8)] for j in range(8)]
        regex_res = r"RES:\s*(\S+)" # Regex to get the result of the match
        regex_checkmate = r"CHECKMATE:\s*(True|False)" # Regex to get if the match ended with a checkmate

        res = re.findall(regex_res, match[0])[0] # Get the result of the match
        self.res = [0.0, 0.0, 0.0, 0.0]
        if res == "1-0":
            self.res[0] = 1.0
        elif res == "0-1":
            self.res[1] = 1.0
        elif res == "1/2-1/2":
            self.res[2] = 1.0
        else:
            self.res[3] = 1.0
        self.checkmate = re.findall(regex_checkmate, match[1]) # Get if the match ended with a checkmate
        fen = match[2]
        (self.board, self.turn, self.castling, self.enPassant, self.halfMove, self.fullMove) = self.parseFen(fen)

    """Parse the FEN to get the board"""
    def parseFen(self, fen):
        fenParts = fen.split(" ")
        fenParts.pop(0)
        board = self.parseBoard(fenParts[0])
        turn = fenParts[1]
        castling = fenParts[2]
        enPassant = fenParts[3]
        halfMove = fenParts[4]
        turn = fenParts[5]
        return (board, turn, castling, enPassant, halfMove, turn)

    """Parse the board from the FEN"""
    def parseBoard(self, fenBoard):
        board = []
        for row in fenBoard.split("/"):
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
        res += "CHECKMATE: {}\n".format(self.checkmate)
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
        fileContent = self.getFileContent(configPath)
        self.matches = self.parseFile(fileContent)
        self.boards = []
        for match in self.matches:
            self.boards.append(Board(match))

        random.shuffle(self.boards)
        nbTestBoards = int(len(self.boards) * 0.2)
        self.testBoards = self.boards[:nbTestBoards]
        self.boards = self.boards[nbTestBoards:]

    """Get the content of a file"""
    def getFileContent(self, path):
        with open(path, "r") as f:
            content = f.read()
        return content

    """Parse the file to get the matches"""
    def parseFile(self, content):
        regex_combined = (
            r"(RES:\s*\S+)\n"
            r"(CHECKMATE:\s*\S+)\n"
            r"(FEN:\s*[\w\/\s-]+\d\s+\d+)"
        )

        matches = re.findall(regex_combined, content)
        return matches

    """Make a random batch of boards"""
    def makeRandomBatch(self, batchSize):
        batch = []
        for i in range(batchSize):
            batch.append(self.takeRandomBoard(batch))
        return batch

    """Take a random board from the current batch"""
    def takeRandomBoard(self, currentBatch):
        board = random.choice(self.boards)
        if board in currentBatch:
            return self.takeRandomBoard(currentBatch)
        return board

    """Make a random batch of test boards"""
    def makeRandomTestBatch(self, batchSize):
        batch = []
        for i in range(batchSize):
            batch.append(self.takeRandomTestBoard(batch))
        return batch

    """Take a random test board from the current batch"""
    def takeRandomTestBoard(self, currentBatch):
        board = random.choice(self.testBoards)
        if board in currentBatch:
            return self.takeRandomTestBoard(currentBatch)
        return board
