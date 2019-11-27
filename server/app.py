from flask import Flask
app = Flask(__name__)
import json
import game

lobby = game.Lobby()

@app.route('/')
def index():
    return 'Hello Flask'

@app.route('/join')
def join():
    return str(lobby.join())

@app.route('/lobby')
def lobbycheck():
    return str(lobby.players)