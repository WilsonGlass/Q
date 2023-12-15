To: CEOs <br>
From: Dilan Piscatello and Wilson Glass <br>
CC: Matthias Felleisen <br>
Subject: Planning the Sprints of the Q Game <br>

### Changing the bonus points again and allow more players to participate in a game
- We'll add a config structure to the rulebook which will take in the constant point values to adjust for changing 
scoring rules
- Allowing more players to join is similar. We could add players in the rulebook and inside the config we would 
ask the setup user for the max number of players allowed to join the game.
Difficulty: 2
### Adding wildcard tiles
- We'll have to add a new value to TileShape and TileColor enum called wildcard
- We'll have to add logic inside the rulebook to modify is_valid_placements to account for wildcards.
- There many be some interesting complexities with scoring a Q.
Difficulty: 3

### imposing restrictions that enforce the rules of Qwirkle instead of Q.
- We'll abstract out the rulebook class and create a new specific rulebook implementation called Qwirkle rules.
- The most difficult part of this task will be creating the rules to enforce Qwrikle rather than redoing design.
Difficulty: 4


Best,
Dilan Piscatello and Wilson Glass