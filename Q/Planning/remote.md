Dear CEOS,
From: George ElMassih and Wilson Glass
CC: Matthias Felleisen
Subject: Planning the remote-proxy

Task: Design the remote-proxy:

<b>ClientProxy:</b>
<p>def signup():<br>
"""<br>
attempts to connect to the server in the beginning of the game, permitting that there are not the maximum allotted players already signed up<br>
"""<br>
</p>

<p>def send_turn(turn: Turn):<br>
"""<br>
sends encoded json representation of a turn to be taken to the server. Our representation will
be of the form jaction to be easily converted.<br>
"""
</p>

<p>def get_outcome(outcome: jresult):<br>
"""<br>
Receives encoded outcome of the game from the server. Our outcome representation is a jresult.
This method will parse this jresult and call the player's win() method with the parsed jresult. We don't believe we will have to notify
a player who was kicked because the referee should not care about them anymore.<br>
"""<br>
</p>

<b>ServerProxy:</b>
<p>def gather_players(time_to_gather: int, players_allotted: int):<br>
"""<br>
Listens for player connections. Once players_allotted join or time_to_gather has 
been surpassed (if the players joined is >= 2), this method will create a list of player objects by receiving their 
name and age. This information will be passed into launch_game().<br>
"""<br>

<p>def launch_game(players: List[Player]):<br>
"""<br>
Sorts the players by age calls run_game() in referee with list of player objects created<br>
"""<br>
</p>

<p>def send_outcome(players: List[Player], pair_results: PairResults):<br>
"""<br>
Creates a jresult from pair_results and sends to each player in the player list<br>
"""<br>
</p>

Thank you, George ElMassih and Wilson Glass