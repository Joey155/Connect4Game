from flask import Flask, render_template, request, jsonify
from json import dumps, loads
from Gameboard import Gameboard
import logging
import db


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

game = None
player1Color = None
player2Color = None


'''
Implement '/' endpoint
Method Type: GET
return: template player1_connect.html and status = "Pick a Color."
Initial Webpage where gameboard is initialized
'''


@app.route('/', methods=['GET'])
def player1_connect():
    global game
    db.init_db()
    game = Gameboard()
    recentGameMove = db.getMove()
    if recentGameMove is not None:
        game.board = loads(recentGameMove[1])
        game.current_turn = recentGameMove[0]
        game.player1 = recentGameMove[3]
        game.player2 = recentGameMove[4]
        game.remaining_moves = recentGameMove[5]
        return render_template('player1_connect.html')
    elif request.method == 'GET':
        return render_template('player1_connect.html', status="Pick a Color.")


'''
Helper function that sends to all boards don't modify
'''


@app.route('/autoUpdate', methods=['GET'])
def updateAllBoards():
    try:
        return jsonify(move=game.board, winner=game.game_result,
                       color=game.player1)
    except Exception:
        return jsonify(move="")


'''
Implement '/p1Color' endpoint
Method Type: GET
return: template player1_connect.html and status = <Color picked>
Assign player1 their color
'''


@app.route('/p1Color', methods=['GET'])
def player1_config():
    if request.method == 'GET':
        global player1Color
        player1Color = request.args.get('color')
        game.player1 = player1Color
        return render_template('player1_connect.html', status=player1Color)


'''
Implement '/p2Join' endpoint
Method Type: GET
return: template p2Join.html and status = <Color picked> or Error
if P1 didn't pick color first

Assign player2 their color
'''


@app.route('/p2Join', methods=['GET'])
def p2Join():
    if request.method == 'GET':
        global player2Color
        if game.player1 == "":
            return "ERROR. Player 1 must choose first"
        else:
            if game.player1 == 'red':
                player2Color = 'yellow'
            elif game.player1 == 'yellow':
                player2Color = 'red'
            game.player2 = player2Color
            assert(game.player2 != "")
            return render_template('p2Join.html', status=player2Color)


'''
Implement '/move1' endpoint
Method Type: POST
return: jsonify (move=<CurrentBoard>,
invalid=True or False, winner = <currWinner>)
If move is valid --> invalid = False else invalid = True
If invalid == True, also return reason= <Why Move is Invalid>

Process Player 1's move
'''


@app.route('/move1', methods=['POST'])
def p1_move():
    if request.method == 'POST':
        columnNumber = int(request.json['column'][-1])
        col = columnNumber - 1
        result = game.firstPlayerMove(col, game.player1)
        db.add_move((game.current_turn, dumps(game.board), game.game_result,
                     game.player1, game.player2, game.remaining_moves))
        if result["winner"] != "":
            db.clear()
            return jsonify(move=game.board, invalid=result["invalid"],
                           winner=result["winner"])
        return jsonify(move=game.board, invalid=result["invalid"],
                       winner=result["winner"], reason=result["reason"])


'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    if request.method == 'POST':
        columnNumber = int(request.json['column'][-1])
        col = columnNumber - 1
        result = game.secondPlayerMove(col, game.player2)
        db.add_move((game.current_turn, dumps(game.board), game.game_result,
                     game.player1, game.player2, game.remaining_moves))
        if result["winner"] != "":
            db.clear()
            return jsonify(move=game.board, invalid=result["invalid"],
                           winner=result["winner"])
        return jsonify(move=game.board, invalid=result["invalid"],
                       winner=result["winner"], reason=result["reason"])


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
