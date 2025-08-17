from flask import Flask, render_template, request, session, jsonify
from . import tictactoe
import secrets
import os

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(16))


@app.route("/", methods=["GET", "POST"])
def play_tictactoe():
    string = "Choose X or O (X moves first)"
    if request.method == "GET":
        session["waiting"] = False
        session["board"] = tictactoe.initialize()
        return render_template("tictactoe.html", board=session["board"], string=string)
    elif request.method == "POST":
        if session["board"] == tictactoe.initialize():
            session["person"] = request.values.get("X") or request.values.get("O")
            session["waiting"] = False
        if tictactoe.game_over(session["board"]):
            session["board"] = tictactoe.initialize()
            session["waiting"] = False
            return jsonify({"board": session["board"], "string": string})
        if session["person"] == "O" and session["board"] == tictactoe.initialize():
            randommove = tictactoe.random_move()
            session["board"][randommove[0]][randommove[1]] = "X"
            string = "Your move."
            return jsonify({"board": session["board"], "string": string})
        next_move = int(request.values.get("guess")[0]), int(
            request.values.get("guess")[1]
        )
        if not session["waiting"] and tictactoe.is_valid(next_move, session["board"]):
            string = "AI is thinking..."
            session["board"] = tictactoe.result(session["board"], next_move)
            if tictactoe.game_over(session["board"]):
                if tictactoe.winner(session["board"]) == session["person"]:
                    string = "You win!"
                elif not tictactoe.winner(session["board"]):
                    string = "Draw."
                else:
                    string = "AI Wins!"
            session["waiting"] = True
        elif session["waiting"]:
            string = "Your move."
            ai_move = tictactoe.minimax(session["board"])
            session["board"] = tictactoe.result(session["board"], ai_move)
            if tictactoe.game_over(session["board"]):
                if tictactoe.winner(session["board"]) == session["person"]:
                    string = "You win!"
                elif not tictactoe.winner(session["board"]):
                    string = "Draw."
                else:
                    string = "AI Wins!"
            session["waiting"] = False
        else:
            string = "Invalid move."
        return jsonify({"board": session["board"], "string": string})
