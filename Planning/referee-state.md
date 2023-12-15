Dear CEOS,<br>
From: Dilan Piscatello and Wilson Glass<br>
CC: Matthias Felleisen<br>
Subject: Planning the Referee State<br>

## Task: Design the Referee Component:
### Communication between the Referee and the GameState

<b> def save_state() </b> <br>
Saves this current state of the game for later use. 
This would be called after each turn.

<b> def pause_game() </b> <br>
Pauses the current game at the current state. 
This would occur if any of the players disconnect.
Saves the current players

<b> def resume_game() </b> <br>
Resumes the current game at some previously saved state.
The game would resume if all the players that signed up are active again.
Refresh all players with their current player game state.

<b> def end_game() </b> <br>
Ends the game for all players currently playing the game.
Sends win/loss messages with a final leaderboard to the all players.

<b> def start_game() </b> <br>
Starts the game for the given players in the game.
gets the initial player game states which include the basic information 


Thank you,
Dilan Piscatello and Wilson Glass