Dear CEOS,<br>
From: Dilan Piscatello and Wilson Glass<br>
CC: Matthias Felleisen<br>
Subject: Planning the Player protocol<br>

Hello, I hope all is well. We are going to be defining the player protocol in the Q game.

### Player -> Referee

<p>A client needs to be able to connect to the game. A client will pass in their age and some sort of identification
to the referee in a json player object.
The referee would take this input and store the player as a player object. 
<br>def signup_player(player)</p>

<p>A client needs to be able to submit a turn to the referee. Submitting a turn would pass the new proposed game board
to the referee.
<br>def submit_turn(proposed_turn: Tiles, turn_outcome: turnOutcome) </p>


### Referee -> Player
<p>The referee needs to start the game and let the players know the game started. 
This method would relay to all the players the game has started.
<br>def start_game()</p>

<p>A referee needs to let a player know that their turn is next.
This will relay the current board state to the player.
<br>def start_turn(state)</p>

<p>The referee sends a message to all players when the game has won/ended.
<br>def end_game()</p>

<p>A referee calls this method if a player is kicked from the current game
<br>def kick_player(Player)</p>


Thank you for taking the time to read our memo,<br>
Sincerely,<br>
Dilan Piscatello and Wilson Glass
