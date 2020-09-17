# Ultimate Tic-Tac-Toe MCTS

This program uses Monte-Carlo Tree Search with Upper Confidence Trees to play a user in the game of Ultimate Tic-Tac-Toe. This project was solely intended as a tool for better understanding how to implement MCTS and therefore is somewhat inefficient, especially the python implementation. The Java implementation runs pretty quickly and is a very strong opponent.

The program should be quite intuitive to use, simply run the main python class (client.py) or alternatively compile and run Client.java. The python version is very weak when given a reasonable time for moves (5 seconds), but I was unable to beat the Java version with MAX_TIME = 5 (set in Bot.java) in the five or so games I tried. This game is very well suited to tree search, as the branching factor is small and the bot is able to avoid making blunders while fully capitalizing on any made by the human player. I really enjoyed being able to see the bots "confidence" in winning (the root node win loss) as I played. It could be interesting to make a program to generate bot moves for a given position in a more friendly interface than the tree diagram it currently prints. 

See https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe#Rules for a complete explanation of the rules of the game.

See https://github.com/mtp61/gof_ISMCTS for tree search (and more) implemented for Gang of Four, a card game.
