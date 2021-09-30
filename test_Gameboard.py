import unittest
import random
from Gameboard import Gameboard


class Test_testGameboard(unittest.TestCase):
    def setUp(self):
        self.game = Gameboard()
        self.game.player1 = "yellow"
        self.game.player2 = "red"

    def testNotCurrentPlayersTurn(self):
        self.game.current_turn = "p2"
        log = self.game.firstPlayerMove(
            random.randint(0, 6), self.game.player1)
        expectedInvalidLog = True
        actualInvalidLog = log["invalid"]
        message = "Invalid moved not checked properly"
        self.assertEqual(actualInvalidLog, expectedInvalidLog, message)

    def testWinnerAlreadyDeclared(self):
        self.game.game_result = "p1"
        log = self.game.firstPlayerMove(
            random.randint(0, 6), self.game.player1)
        expectedInvalidLog = True
        actualInvalidLog = log["invalid"]
        message = "Invalid moved not checked properly"
        self.assertEqual(actualInvalidLog, expectedInvalidLog, message)

    def testGameTied(self):
        self.game.remaining_moves = 0
        log = self.game.firstPlayerMove(
            random.randint(0, 6), self.game.player2)
        expectedInvalidLog = True
        actualInvalidLog = log["invalid"]
        message = "Invalid moved not checked properly"
        self.assertEqual(actualInvalidLog, expectedInvalidLog, message)

    def testCurrentColumnFilled(self):
        col = 6
        for row in range(5):
            self.game.board[row][col] = "yellow"
        isValid = self.game.isValidLocation(6)
        self.assertEqual(False, isValid)

    def testHorizontalWinningMove(self):
        row = 5
        for col in range(4):
            self.game.board[row][col] = "red"
        _ = self.game.isWinningMove(playerPiece="red")
        expectedLog = "horizontal"
        actualLog = self.game.winingMoveLog["direction"]
        message = "Horizontal winning move check is faulty"
        self.assertEqual(actualLog, expectedLog, message)

    def testVerticalWinningMove(self):
        col = 6
        for row in range(5):
            self.game.board[row][col] = "yellow"
        _ = self.game.isWinningMove(playerPiece="yellow")
        expectedLog = "vertical"
        actualLog = self.game.winingMoveLog["direction"]
        message = "Vertical winning move check is faulty"
        self.assertEqual(actualLog, expectedLog, message)

    def testPositiveDiagonalWinningMove(self):
        row = 3
        for col in range(4):
            self.game.board[row - col][col] = "yellow"
        _ = self.game.isWinningMove(playerPiece="yellow")
        expectedLog = "positive diagonal"
        actualLog = self.game.winingMoveLog["direction"]
        message = "Positive diagonal winning move check is faulty"
        self.assertEqual(actualLog, expectedLog, message)

    def testNegativeDiagonalwinningMove(self):
        col = 2
        for row in range(2, 6):
            self.game.board[row-2+col][row-2+col] = "red"
        _ = self.game.isWinningMove(playerPiece="red")
        expectedLog = "negative diagonal"
        actualLog = self.game.winingMoveLog["direction"]
        message = "Negative diagonal winning move check is faulty"
        self.assertEqual(actualLog, expectedLog, message)


if __name__ == '__main__':
    unittest.main()
