# Ultimate Tic-Tac-Toe MCTS

This program uses Monte-Carlo Tree Search with Upper Confidence Trees to play a user in the game of Ultimate Tic-Tac-Toe

This project was solely intended as a tool for better understanding how to implement MCTS and therefore is very inefficient. Hopefully this code will serve as a launching point for more complex future projects...

Bugs:
- it runs into gamestates where there is no move, must not be checking endgames correctly
- incorrectly categorizing some subgame wins
- sometimes subgames will have no open squares, how to deal with this? - 
  - probably just go anywhere, 
  - raises the issue of ties, 
    - probably just randomly assign winner
  - this needs to be addressed in client and bot