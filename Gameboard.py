import db

class Gameboard():
    def __init__(self):
        self.player1 = ""
        self.player2 = ""
        self.board = [[0 for x in range(7)] for y in range(6)]
        self.game_result = ""
        self.current_turn = 'p1'
        self.remaining_moves = 42

    '''
    Add Helper functions as needed to handle moves and update board and turns
    '''

    def isValidLocation(self, col):
        # check if a selected location on the board is valid
        return self.board[5][col] == 0
    
    def __getNextOpenRow(self, col):
        availableRow = None
        for row in range(6):
            if self.board[row][col] == 0:
                availableRow = row
        return availableRow

    def makeMove(self, col, playerColor):
        row = self.__getNextOpenRow(col)
        if self.player1 == playerColor:
            self.board[row][col] = '*'
            self.remaining_moves -= 1
        elif self.player2 == playerColor:
            self.board[row][col] == '#'
            self.remaining_moves -= 1

    def isWinningMove(self):
        playerPiece = None
        if self.current_turn == 'p1':
            playerPiece = '*'
            self.current_turn = 'p2'
        else:
            playerPiece = '#'
            self.current_turn = 'p1'

        # check horizontal direction
        for col in range(7-3):
            for row in range(6):
                if self.board[row][col] == playerPiece and self.board[row][col+1] == playerPiece and \
                    self.board[row][col+2] == playerPiece and self.board[row][col+3] == playerPiece:
                    self.__updateGameResult(playerPiece)
                    return True
        
        # check vertical direction
        for col in range(7):
            for row in range(6-3):
                if self.board[row][col] == playerPiece and self.board[row+1][col] == playerPiece and \
                    self.board[row+2][col] == playerPiece and self.board[row+3][col] == playerPiece:
                    self.__updateGameResult(playerPiece)
                    return True

        # There are two diagonal directions
        # Check negative diagonal direction
        for col in range(3, 7):
            for row in range(6-3):
                if self.board[row][col] == playerPiece and self.board[row+1][col-1] == playerPiece and \
                    self.board[row+2][col-2] == playerPiece and self.board[row][col] == playerPiece:
                    self.__updateGameResult(playerPiece)
                    return True

        # Check positive diagonal direction
        for col in range(7-3):
            for row in range(6-3):
                if self.board[row][col] == playerPiece and self.board[row+1][col+1] == playerPiece and \
                    self.board[row+2][col+2] == playerPiece and self.board[row+3][col+3] == playerPiece:
                    self.__updateGameResult(playerPiece)
                    return True

    def __updateGameResult(self, playerPiece):
        if playerPiece == '*':
            self.game_result = "p1"
        else:
            self.game_result = "p2"        
