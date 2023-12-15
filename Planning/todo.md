To: CEOs
From: Dilan Piscatello and Wilson Glass
CC: Matthias Felleisen
Subject: Fixing the TODO

Here are some of the items we want to fix:

Completed: 
- Fix the purpose statements of all classes
  - ABC in abstract for example
"Added/changed many purpose statements"
https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/commit/4a4aa4e70f5831250ae505fe856043713bdf8aef

- Move the points methods to the rulebook
"move scoring into the rulebook.py file instead of gamestate."
https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/commit/3b9880230bdf8b4def8bd90a1ba5c6928e16dd83

- We need to account for when there are no players for the queue
"Made it so we account for when there are no players in the queue"
https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/commit/55c318094844d86022e5cc50f37be454406834cf

- All same row/col needs to be in rulebook
"Moved all_same_row_or_col() into rulebook and refactored to account f…"
https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/commit/0bb9845046c8a1d6f323177deceaf377eb293014

- Fix the integration test
  "fix integration tests"
- https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/commit/ce4e675c19a2bfc191b55c0aeb7503956ff1af25

- Try/Catch in the referee should be converted to a True/False checking if player made valid move
- "add try catch for all player api function calls"
- https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/commit/6788523eec022b80d91c477b20398f3ce5588c00

- Rulebook should be an input to the GameState not the map 
- "add referee to the gamestate and the players" -- (I meant "add rulebook" in commit message oops)
- https://github.khoury.northeastern.edu/CS4500-F23/salty-camels/commit/e456732184902275bffc6838ae19ce837a3f2f99



Best,
Dilan Piscatello and Wilson Glass