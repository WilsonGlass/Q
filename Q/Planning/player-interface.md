To: CEOs
From: Dilan Piscatello and Oliver Toh
CC: Matthias Felleisen
Subject: Planning the Player Interface

Player Interface Details:

Methods:
A turnOutcome is a:

- placed
- exchanged
- pass

A turn is: TurnOutcome, List of Tiles, List of Positions

PlayerGameState is defined in player_game_state.py

Creates a turn using some given strategy
def create_move(current_state: PlayerGameState) -> Turn

converts a given Turn into a json ojbect that can be passed via TCP
def normalize_move(Turn) -> JSON

sends json over TCP for the server to recieve and process move and game commands
def send_json(JSON)

Sign up for a given hostname and given port
def sign_up(hostname, port)

After signing up, the player listens for updates from the server. (e.g waiting for turn)
def listen_on_port():

convert recieved json to the player game state
def json_to_player_game_state()

Thank you and have a nice day,

Sincerely,
Dilan Piscatello and Oliver Toh
