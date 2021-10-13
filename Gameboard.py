
class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42
        self.winingMoveLog = {"direction": None}

    def __getNextOpenRow(self, col):
        availableRow = None
        for row in range(6):
            if self.board[row][col] == 0:
                availableRow = row
        return availableRow

    def __updateGameResult(self, playerPiece):
        if playerPiece == self.player1:
            self.game_result = "p1"
        else:
            self.game_result = "p2"

    def isValidLocation(self, col):
        # check if a selected location on the board is valid
        return self.board[0][col] == 0

    def makeMove(self, col, playerPiece):
        row = self.__getNextOpenRow(col)
        self.board[row][col] = playerPiece
        self.remaining_moves -= 1
        return row

    def updateTurn(self, currentTurn):
        if currentTurn == 'p1':
            self.current_turn = 'p2'
        else:
            self.current_turn = 'p1'

    def __makeLog(self, row, invalid, reason, winner):
        log = {"row": None, "invalid": None, "reason": None, "winner": None}
        log["row"] = row
        log["invalid"] = invalid
        log["reason"] = reason
        log["winner"] = winner
        return log

    def firstPlayerMove(self, col, playerPiece):
        if self.player1 == "":
            return self.__makeLog(None, True, "Player 1 must connect",
                                  self.game_result)
        elif self.player2 == "":
            return self.__makeLog(None, True, "Player 2 must connect",
                                  self.game_result)

        elif self.remaining_moves == 0:
            return self.__makeLog(None, True, "Game Over! Draw game.",
                                  self.game_result)

        elif self.game_result != "":
            return self.__makeLog(None, True, "Game Over! Winner declared.",
                                  self.game_result)

        elif self.current_turn != 'p1':
            return self.__makeLog(None, True,
                                  "{} is next".format(self.current_turn),
                                  self.game_result)

        elif not self.isValidLocation(col):
            return self.__makeLog(None, True, "Invalid Location",
                                  self.game_result)

        else:
            row = self.makeMove(col, playerPiece)
            self.updateTurn('p1')
            _ = self.isWinningMove(playerPiece)
            if self.remaining_moves == 0:
                return self.__makeLog(row, False, "Draw Game!", "Draw")
            else:
                return self.__makeLog(row, False, "", self.game_result)

    def secondPlayerMove(self, col, playerPiece):
        if self.remaining_moves == 0:
            return self.__makeLog(None, True, "Game Over! Draw game.",
                                  self.game_result)

        elif self.game_result != "":
            return self.__makeLog(None, True, "Game Over! Winner declared.",
                                  self.game_result)

        elif self.current_turn != 'p2':
            return self.__makeLog(None, True,
                                  "{} is next".format(self.current_turn),
                                  self.game_result)

        elif not self.isValidLocation(col):
            return self.__makeLog(None, True, "Invalid Location",
                                  self.game_result)

        else:
            row = self.makeMove(col, playerPiece)
            self.updateTurn('p2')
            _ = self.isWinningMove(playerPiece)
            if self.remaining_moves == 0:
                return self.__makeLog(row, False, "Draw Game!", "Draw")
            else:
                return self.__makeLog(row, False, "", self.game_result)

    def isWinningMove(self, playerPiece):
        # check horizontal direction
        for col in range(7-3):
            for row in range(6):
                if self.board[row][col] == playerPiece and \
                   self.board[row][col+1] == playerPiece and \
                   self.board[row][col+2] == playerPiece and \
                   self.board[row][col+3] == playerPiece:
                    self.__updateGameResult(playerPiece)
                    self.winingMoveLog["direction"] = "horizontal"
                    return True

        # check vertical direction
        for col in range(7):
            for row in range(6-3):
                if self.board[row][col] == playerPiece and \
                   self.board[row+1][col] == playerPiece and \
                   self.board[row+2][col] == playerPiece and \
                   self.board[row+3][col] == playerPiece:
                    self.__updateGameResult(playerPiece)
                    self.winingMoveLog["direction"] = "vertical"
                    return True

        # There are two diagonal directions
        # Check positive diagonal direction
        for col in range(3, 7):
            for row in range(6-3):
                if self.board[row][col] == playerPiece and \
                   self.board[row+1][col-1] == playerPiece and \
                   self.board[row+2][col-2] == playerPiece and \
                   self.board[row+3][col-3] == playerPiece:
                    self.__updateGameResult(playerPiece)
                    self.winingMoveLog["direction"] = "positive diagonal"
                    return True

        # Check negative diagonal direction
        for col in range(7-3):
            for row in range(6-3):
                if self.board[row][col] == playerPiece and \
                   self.board[row+1][col+1] == playerPiece and \
                   self.board[row+2][col+2] == playerPiece and \
                   self.board[row+3][col+3] == playerPiece:
                    self.__updateGameResult(playerPiece)
                    self.winingMoveLog["direction"] = "negative diagonal"
                    return True
        return False
