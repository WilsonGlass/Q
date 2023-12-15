To: CEOs
From: Dilan Piscatello and Oliver Toh
CC: Matthias Felleisen
Subject: Planning the Sprints of the Q Game

Hello, here is the list of the sprint definitions.

# Sprint 1

Thesis: Design the fundamental components of the game.

We want to develop all the items that are the most concrete and independent. Some examples of this are the board, the pieces, and the referee (game logic).

We want to design the basic interface for the player-referee abstracting away the TCP.
Develop some basic view of the game - this is a convenience view to keep track of the board as the game gets complex.

# Sprint 2

Thesis: Design the player client while considering the use of TCP communication

Complete the player-referee interface - perhaps using the command design pattern. Develop what a Player means in our game and how communication might work. Additionally, add the logically signup of the players. 

# Sprint 3

Thesis: Develop the TCP connection for the game, implement non-player observers and finish loose ends.

We want to develop the communication TCP for the AI bots on the server as well as develop and implement the concept of the non-players observers. Listen to TCP registers of AI bots and make necessary signups

Throughout the process, we will also test all of the components for each sprint and improve on the view as more features are added.


Best,
Dilan and Oliver
