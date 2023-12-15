Dear CEOS,<br>
From: Dilan Piscatello and Wilson Glass<br>
CC: Matthias Felleisen<br>
Subject: Planning the Game Observer<br>

## Designing the Game Observer Mechanism:

<p>The observer should be able to see three main components about the game:</p>
<p>The observer should be able to view all of the players current scores</p>
<p>def observe_scores() </p>

<p> The observer should be able to have a live updated map of the game </p>
<p> def observe_map() </p>

<p>The observer should be able to see the number of referee tiles that are left in the deck.</p>
<p> def observe_of_ref_tiles() </p>

<p> The observer should have some way of signing up to the referee to get game. 
This can be at any time and does not need to be at the start of the game. 
This would be a method in the referee class singing up the player </p>
<p> def join_game_as_observer(observer) </p>

<p> The observer should be able to freely leave and join at their liking. An observer joining can come and go as they please.
</p>

The game observer should not be a component in the game state as they do not affect anything in the gamestate. The
observers have the ability to watch over the gamestate and can view some public knowledge. They observers will
not be able to view private information about the players like the hands they have as there could be cheating involved.


Thank you,
Dilan Piscatello and Wilson Glass
