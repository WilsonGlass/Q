# Client
<img src="client_interaction_diagram.png" alt="isolated" width="800"/>
<br>
This is the interaction diagram for the client side of the remote proxy design. The client hosts
a proxy referee which continuously listens for jsons to be dispatched. When a json is dispatched
the mname is parsed and the RefereeFactory calls for the appropriate RefereeMethod. Those methods
send void to the ProxyPlayer when complete.

![Client Class Diagram](client_class_diagram.png)
![Remote Signup Interaction Diagram](remote_signup.png)
![Remote Turns Interaction Diagram](remote_turns.png)
![Remote Request New Tiles Interaction Diagram](remote_new_tiles.png)
![Remote Setup Interaction Diagram](remote_setup.png)
![Remote Win Interaction Diagram](remote_win.png)
![Ending Game](image.png)