# Server
<img src="server_interaction_diagram.png" alt="isolated" width="800"/>
<br>
This is the interaction diagram for the server side of our remote proxy. Per each
client connection, a thread is created that waits for the signup period and attempts to launch
the game. Although there are multiple threads being run, we lock the launch_game method
and ensure that only one game is ever ran by the referee.
<br>
The Referee is passed proxy players that send and receive json information to/from the client.
When we receive information from the client, we parse it using our util methods and return it as
our own data representation to the referee.

![Remote Signup Interaction Diagram](remote_signup.png)
![Remote Turns Interaction Diagram](remote_turns.png)
![Remote Request New Tiles Interaction Diagram](remote_new_tiles.png)
![Remote Setup Interaction Diagram](remote_setup.png)
![Remote Win Interaction Diagram](remote_win.png)
![Ending Game](image.png)