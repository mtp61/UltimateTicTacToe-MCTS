import math
from bot import Bot


def main():
    MAX_TIME = 2  # thinking time for the bot in seconds

    # make the game and the bot
    game = Game()
    bot = Bot(MAX_TIME)

    # render starting board
    print('Ultimate Tic-Tac-Toe')
    game.render_board()

    # main loop
    while game.game_active:
        game.get_player_move()
        game.render_board()
        if not game.game_active:  # need to check if the player won and stop execution
            break
        game.get_bot_move(bot)
        game.render_board()


class Game:
    def __init__(self):
        # define game variables
        self.ROW_LABELS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.COLUMN_LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        self.game_active = True

        self.next_subgame = (-1, -1)

        # make the board, format is 0 for empty, 1 for player, -1 for bot
        self.board = []
        for i in range(9):
            self.board.append([])
            for j in range(9):
                self.board[-1].append(0)
        # make the bigboard, tracks the scores of the subgames, format is the same
        self.big_board = []
        for i in range(3):
            self.big_board.append([])
            for j in range(3):
                self.big_board[-1].append(0)

        
    def render_board(self):
        print()

        for i in range(9):
            print(f"{self.ROW_LABELS[8 - i]} ", end="")  # row label
            for j in range(9):
                # check big board then full board
                if self.big_board[math.floor(i / 3)][math.floor(j / 3)] == 1:
                    print('X', end="")
                elif self.big_board[math.floor(i / 3)][math.floor(j / 3)] == -1:
                    print('O', end="")
                elif self.board[i][j] == 0:
                    print(' ', end="")
                elif self.board[i][j] == 1:
                    print('X', end="")
                elif self.board[i][j] == -1:
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


    def get_player_move(self):
        # make the vars for telling the user which subgame to play in
        if self.next_subgame == (-1, -1):
            col_low = 'a'
            col_high = 'i'
            row_low = '1'
            row_high = '9'
        else:
            col_low = self.COLUMN_LABELS[self.next_subgame[1] * 3]
            col_high = self.COLUMN_LABELS[self.next_subgame[1] * 3 + 2]
            row_low = self.ROW_LABELS[8 - self.next_subgame[0] * 3]
            row_high = self.ROW_LABELS[8 - (self.next_subgame[0] * 3 + 2)]

        need_move = True
        while need_move:
            move = input(f"Enter your move [{col_low}-{col_high}][{row_low}-{row_high}]: ")

            # check that move follows format
            if len(move) != 2:
                continue
            if not (move[0] in self.COLUMN_LABELS and move[1] in self.ROW_LABELS):
                continue

            # check that move is legal
            move_parsed = (8 - self.ROW_LABELS.index(move[1]), self.COLUMN_LABELS.index(move[0]))
            # check in correct subgame
            if self.next_subgame != (-1, -1):
                if (math.floor(move_parsed[0] / 3), math.floor(move_parsed[1] / 3)) != self.next_subgame:
                    continue

            # check open square
            if self.board[move_parsed[0]][move_parsed[1]] != 0:
                continue

            # check subgame is not complete
            if self.board[move_parsed[0]][move_parsed[1]] != 0:
                continue

            # if we get to here in the loop then move is valid
            need_move = False

        # execute the move
        self.board[move_parsed[0]][move_parsed[1]] = 1

        self.check_subgames()
        self.check_win()

        # update next subgame
        if self.big_board[move_parsed[0] % 3][move_parsed[1] % 3] == 0:
            i = move_parsed[0] % 3
            j = move_parsed[1] % 3
            finished_cells = 0
            for m in range(3):
                for n in range(3):
                    if self.board[3 * i + m][3 * j + n] != 0:
                        finished_cells += 1

            if finished_cells == 9:  # subgame is full
                self.next_subgame = (-1, -1)
            else:
                self.next_subgame = (move_parsed[0] % 3, move_parsed[1] % 3)
        else:
            self.next_subgame = (-1, -1)

    
    def get_bot_move(self, bot):
        self.board, self.big_board, self.next_subgame = bot.get_move(self.board, self.big_board, self.next_subgame)

        self.check_subgames()
        self.check_win()

    
    def check_subgames(self):
        for i in range(3):
            for j in range(3):
                if self.big_board[i][j] == 0:  # subgame not finished
                    # check the rows
                    for m in range(3):
                        row_sum = 0
                        for n in range(3):
                            row_sum += self.board[3 * i + m][3 * j + n]
                        
                        if row_sum == 3:
                            self.big_board[i][j] = 1
                        elif row_sum == -3:
                            self.big_board[i][j] = -1
                        
                    # check the cols
                    for n in range(3):
                        col_sum = 0
                        for m in range(3):
                            col_sum += self.board[3 * i + m][3 * j + n]
                        
                        if col_sum == 3:
                            self.big_board[i][j] = 1
                        elif col_sum == -3:
                            self.big_board[i][j] = -1

                    # check the diagonals
                    # backwards diag
                    diag_sum = 0
                    for p in range(3):
                        diag_sum += self.board[3 * i + p][3 * j + p]

                    if diag_sum == 3:
                        self.big_board[i][j] = 1
                    elif diag_sum == -3:
                        self.big_board[i][j] = -1

                    # forwards diag
                    diag_sum = 0
                    for p in range(3):
                        diag_sum += self.board[3 * i + (2 - p)][3 * j + p]

                    if diag_sum == 3:
                        self.big_board[i][j] = 1
                    elif diag_sum == -3:
                        self.big_board[i][j] = -1


    def check_win(self):
        # check the rows
        for m in range(3):
            row_sum = 0
            for n in range(3):
                row_sum += self.big_board[m][n]

                if row_sum == 3:
                    self.game_active = False
                    print('player win')
                elif row_sum == -3:
                    self.game_active = False
                    print('bot win')

        # check the cols
        for n in range(3):
            col_sum = 0
            for m in range(3):
                col_sum += self.big_board[m][n]
                
                if col_sum == 3:
                    self.game_active = False
                    print('player win')
                elif col_sum == -3:
                    self.game_active = False
                    print('bot win')

        # check the diagonals
        # backwards diag
        diag_sum = 0
        for p in range(3):
            diag_sum += self.big_board[p][p]

            if diag_sum == 3:
                self.game_active = False
                print('player win')
            elif diag_sum == -3:
                self.game_active = False
                print('bot win')

        # forwards diag
        diag_sum = 0
        for p in range(3):
            diag_sum += self.big_board[2 - p][p]

            if diag_sum == 3:
                self.game_active = False
                print('player win')
            elif diag_sum == -3:
                self.game_active = False
                print('bot win')

        # check draw
        finished_games = 0
        for i in range(3):  # go thru the subgames
            for j in range(3):
                if self.big_board[i][j] != 0:
                    finished_games += 1
                else:
                    finished_cells = 0
                    for m in range(3):
                        for n in range(3):
                            if self.board[3 * i + m][3 * j + n] != 0:
                                finished_cells += 1

                    if finished_cells == 9:
                        finished_games += 1

        if finished_games == 9:
            self.game_active = False
            print('draw')


if __name__ == "__main__":
    main()
