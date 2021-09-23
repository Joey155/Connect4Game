from flask import Flask, render_template, request, redirect, jsonify
from json import dump
from Gameboard import Gameboard
import db


app = Flask(__name__)

import logging
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
    game = Gameboard()
    if request.method == 'GET':
        return render_template('player1_connect.html', status = "Pick a Color.")
    

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
        return render_template('player1_connect.html', status = player1Color)


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
            return "ERROR."
        else:
            if game.player1 == 'red':
                player2Color = 'yellow'
            elif game.player1 == 'yellow':
                player2Color = 'red'
            game.player2 = player2Color
            assert(game.player2 != "")
            return render_template('p2Join.html', status = player2Color)
    


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
        if game.game_result == "":
            if game.current_turn == 'p1':
                if game.isValidLocation(col):
                    game.makeMove(col, player1Color)
                    game.updateTurn('p1')
                    if game.isWinningMove(game.player1):
                        return jsonify(move=game.board, invalid=False, winner=game.game_result)
                    else:
                        if game.remaining_moves == 0:
                            return jsonify(move=game.board, invalid=False, winner=game.game_result)
                        return jsonify(move=game.board, invalid=False, winner=game.game_result)
                
                else:
                    return jsonify(move=game.board, invalid=True, 
                                    winner=game.game_result, reason="Invalid location")
            else:
                return jsonify(move=game.board, invalid=True, 
                                    winner=game.game_result, reason="Sorry {} is next".format(game.current_turn))
        else:
            return jsonify(move=game.board, invalid=True, 
                                    winner=game.game_result, reason="Game Over {} won!".format(game.game_result))

        
'''
Same as '/move1' but instead proccess Player 2
'''


@app.route('/move2', methods=['POST'])
def p2_move():
    if request.method == 'POST':
        columnNumber = int(request.json['column'][-1])
        col = columnNumber - 1
        if game.game_result == "":
            if game.current_turn == 'p2':
                if game.isValidLocation(col):
                    game.makeMove(col, player2Color)
                    game.updateTurn('p2')
                    if game.isWinningMove(game.player2):
                        return jsonify(move=game.board, invalid=False, winner=game.game_result)
                    else:
                        if game.remaining_moves == 0:
                            return jsonify(move=game.board, invalid=False, winner=game.game_result)
                        return jsonify(move=game.board, invalid=False, winner=game.game_result)
                
                else:
                    return jsonify(move=game.board, invalid=True, 
                                    winner=game.game_result, reason="Invalid location")
            else:
                return jsonify(move=game.board, invalid=True, 
                                    winner=game.game_result, reason="Sorry {} is next".format(game.current_turn))
        else:
            return jsonify(move=game.board, invalid=True, 
                                    winner=game.game_result, reason="Game Over {} won!".format(game.game_result))



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
