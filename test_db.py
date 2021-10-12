import unittest
import db
import json
from Gameboard import Gameboard


class Test_testdb(unittest.TestCase):
    def setUp(self):
        db.init_db()
        self.game = Gameboard()
        self.game.player1 = "yellow"
        self.game.player2 = "red"

    def tearDown(self):
        self.game = None
        db.clear()

    def setBoard(self):
        col = 6
        for row in range(6):
            if row % 2 == 1:
                self.game.board[row][col] = self.game.player1
                self.game.updateTurn("p1")
                self.game.remaining_moves -= 1
            else:
                self.game.board[row][col] = self.game.player2
                self.game.updateTurn("p2")
                self.game.remaining_moves -= 1
        print(json.dumps(self.game.board))
        return (self.game.current_turn, json.dumps(self.game.board), 
                self.game.game_result, self.game.player1, self.game.player2,
                self.game.remaining_moves)
    
    def test_addMove(self):
        move = self.setBoard()
        cur = db.add_move(move)
        cur.execute('SELECT COUNT(*) from GAME')
        cur_result = cur.fetchone()
        rows = cur_result[0]
        self.assertEqual(rows, 1)

    def test_getMove(self):
        move = self.setBoard()
        _ = db.add_move(move)
        result = db.getMove()
        self.assertEqual(json.loads(move[1]), json.loads(result[1])) 


if __name__ == '__main__':
    unittest.main()
