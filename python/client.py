import math

from bot import Bot
from shared import *

def main():
    MAX_TIME = 1  # thinking time for the bot in seconds

    # make the game and the bot
    game = Game()
    bot = Bot(MAX_TIME)

    # render starting board
    print('Ultimate Tic-Tac-Toe')
    game.draw_board()

    # main loop
    current_player = 1
    while True:
        if current_player == 1:
            # get player move
            game.player_move()

            # next player is up
            current_player = 2
        else:
            # get bot move
            game.bot_move(bot)

            # next player is up
            current_player = 1
        
        game.draw_board()

        # check for win
        win_status = check_win(game.big_board)
        if win_status == 1:
            print("Player win")
            break
        elif win_status == 2:
            print("Bot win")
            break
        elif win_status == -1:
            print("Draw")
            break


class Game:
    def __init__(self):
        # define game variables
        self.ROW_LABELS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.COLUMN_LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        """
        make the board

        list of ints
        0 is empty square
        1 is player 1 (client)
        2 is player 2 (bot)

        goes by game, starts at top left, goes by column then row, same order within games
        """ 

        self.board = [0] * 81
        self.big_board = [0] * 9

        self.next_subgame = -1

        
    def draw_board(self):
        print()

        for i in range(9):
            print(f"{ self.ROW_LABELS[i] } ", end="")  # row label
            for j in range(9):
                square = self.board[lines_to_board(9 * i + j)]
                if square == 0:
                    print(' ', end="")
                elif square == 1:
                    print('X', end="")
                elif square == 2:
                    print('O', end="")
                
                if (j + 1) % 3 != 0:
                    print(' ', end="")
                elif j != 8:
                    print('|', end="")
            print()

            if (i + 1) % 3 == 0 and i != 8:
                print("  -----┼-----┼-----")
            
        print()
        print("  ", end="")
        for j in range(9):
            print(f"{self.COLUMN_LABELS[j]} ", end="")            
        print()


    def player_move(self):
        # make the vars for telling the user which subgame to play in
        if self.next_subgame == -1:
            col_low = 'a'
            col_high = 'i'
            row_low = '1'
            row_high = '9'
        else:
            col_low = self.COLUMN_LABELS[3 * (self.next_subgame % 3)]
            col_high = self.COLUMN_LABELS[3 * (self.next_subgame % 3) + 2]
            row_low = self.ROW_LABELS[3 * math.floor(self.next_subgame / 3)]
            row_high = self.ROW_LABELS[3 * math.floor(self.next_subgame / 3) + 2]

        while True:
            move = input(f"Enter your move [{ col_low }-{ col_high }][{ row_low }-{ row_high }]: ")

            # check that move follows format
            if len(move) != 2:
                continue
            if not (move[0] in self.COLUMN_LABELS and move[1] in self.ROW_LABELS):
                continue

            # check that move is legal
            col_index = self.COLUMN_LABELS.index(move[0])
            row_index = self.ROW_LABELS.index(move[1])
            move_parsed = lines_to_board(9 * row_index + col_index)

            # check in correct subgame
            if self.next_subgame != -1:
                if math.floor(move_parsed / 9) != self.next_subgame:
                    print('wrong subgame')
                    continue

            # check open square
            if self.board[move_parsed] != 0:
                continue

            # if we get to here in the loop then move is valid
            break

        # execute the move
        self.board[move_parsed] = 1

        # update big board
        self.board, self.big_board = update_big_board(self.board, self.big_board, move_parsed)

        # update next subgame
        if self.big_board[move_parsed % 9] == 0:
            self.next_subgame = move_parsed % 9
        else:
            self.next_subgame = -1


    def bot_move(self, bot):
        # get move
        move = bot.get_move(self.board, self.big_board, self.next_subgame)

        # execute the move
        self.board[move] = 2

        # update big board
        self.board, self.big_board = update_big_board(self.board, self.big_board, move)

        # update next subgame
        if self.big_board[move % 9] == 0:
            self.next_subgame = move % 9
        else:
            self.next_subgame = -1


if __name__ == "__main__":
    main()
