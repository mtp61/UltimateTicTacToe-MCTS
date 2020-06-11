import time
import random
import copy


class Bot():
    def __init__(self, MAX_TIME):
        # seed the random number generator
        random.seed = time.time()

        # time limit for thinking in seconds
        self.MAX_TIME = MAX_TIME

    def get_move(self, board, big_board, next_subgame):
        """
        # simple random move bot
        root.update_children()
        num_moves = len(root.children)
        print(f"{num_moves} possible moves")
        child = root.children[random.randrange(num_moves)]
        return child.board, child.big_board, child.next_subgame
        """

        # get the current time
        start_time = time.time()

        # make the root node
        root = Node(board, big_board, next_subgame, -1, 0)



        
        



        # main loop
        #while time.time() - self.MAX_TIME < start_time:  # do loop until out of time
            # selection


            # expansion


            # simulation


            # backpropogation
            
            pass
            # todo



        # find best move from the game tree and return it

        return board, big_board, next_subgame


class Node():
    def __init__(self, board, big_board, next_subgame, player_to_act, is_win):
        self.board = board
        self.big_board = big_board
        self.next_subgame = next_subgame
        self.player_to_act = player_to_act
        self.is_win = is_win

        self.children = []  # list of child nodes


    def get_children(self, board, big_board, next_subgame, player_to_act):
        children = []

        if next_subgame == (-1, -1):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:  # open square
                        temp_child = {}
                        temp_child['board'] = copy.deepcopy(board)
                        temp_child['board'][i][j] = player_to_act
                        temp_child['next_subgame'] = (i % 3, j % 3)

                        children.append(temp_child)
        else:
            for i in range(3):
                for j in range(3):
                    if board[next_subgame[0] * 3 + i][next_subgame[1] * 3 + j] == 0:  # open square
                        temp_child = {}
                        temp_child['board'] = copy.deepcopy(board)
                        temp_child['board'][next_subgame[0] * 3 + i][next_subgame[1] * 3 + j] = player_to_act
                        temp_child['next_subgame'] = ((next_subgame[0] * 3 + i) % 3, (next_subgame[1] * 3 + j) % 3)

                        children.append(temp_child)

        # compute bigboard and add player to act and make sure next_subgame is correct
        row_indices = [i + 3 * next_subgame[0] for i in [0, 1, 2]]
        col_indices = [i + 3 * next_subgame[1] for i in [0, 1, 2]]

        for child in children:
            # add the big_board
            child['big_board'] = copy.deepcopy(big_board)

            # check the subgame to see if it is completed
            need_update = False
            i = next_subgame[0]
            j = next_subgame[1]
            # check the rows
            for m in row_indices:
                row_sum = 0
                for n in col_indices:
                    row_sum += child['board'][m][n]
                
                if row_sum == 3:
                    child['big_board'][i][j] = 1
                    need_update = True
                elif row_sum == -3:
                    child['big_board'][i][j] = -1
                    need_update = True
                
            # check the cols
            for n in row_indices:
                col_sum = 0
                for m in col_indices:
                    col_sum += child['board'][m][n]
                
                if col_sum == 3:
                    child['big_board'][i][j] = 1
                    need_update = True
                elif col_sum == -3:
                    child['big_board'][i][j] = -1
                    need_update = True

            # check the diagonals
            # backwards diag
            diag_sum = 0
            for m in row_indices:
                for n in col_indices:
                    diag_sum += child['board'][m][n]

            if diag_sum == 3:
                child['big_board'][i][j] = 1
                need_update = True
            elif diag_sum == -3:
                child['big_board'][i][j] = -1
                need_update = True

            # forwards diag
            diag_sum = 0
            for m in row_indices:
                for n in reversed(col_indices):
                    diag_sum += child['board'][m][n]

            if diag_sum == 3:
                child['big_board'][i][j] = 1
                need_update = True
            elif diag_sum == -3:
                child['big_board'][i][j] = -1
                need_update = True

            child['is_win'] = False
            if need_update:  # update big_board if needed
                # check if big_board is a win
                row_indices, col_indices = [0, 1, 2], [0, 1, 2]
                # check the rows
                for m in row_indices:
                    row_sum = 0
                    for n in col_indices:
                        row_sum += child['big_board'][m][n]
                    
                    if row_sum == 3:
                        child['is_win'] = 1
                        break
                    elif row_sum == -3:
                        child['is_win'] = -1
                        break
                    
                # check the cols
                for n in row_indices:
                    col_sum = 0
                    for m in col_indices:
                        col_sum += child['big_board'][m][n]
                    
                    if col_sum == 3:
                        child['is_win'] = 1
                        break
                    elif col_sum == -3:
                        child['is_win'] = -1
                        break

                # check the diagonals
                # backwards diag
                diag_sum = 0
                for m in row_indices:
                    for n in col_indices:
                        diag_sum += child['big_board'][m][n]

                if diag_sum == 3:
                    child['is_win'] = 1
                    break
                elif diag_sum == -3:
                    child['is_win'] = -1
                    break

                # forwards diag
                diag_sum = 0
                for m in row_indices:
                    for n in reversed(col_indices):
                        diag_sum += child['big_board'][m][n]

                if diag_sum == 3:
                    child['is_win'] = 1
                    break
                elif diag_sum == -3:
                    child['is_win'] = -1
                    break
                

            # player to act
            child['player_to_act'] = player_to_act * -1

            # make sure next_subgame is correct
            if child['big_board'][child['next_subgame'][0]][child['next_subgame'][1]] != 0:
                child['next_subgame'] = (-1, -1)

        return children


    def update_children(self):
        for child in self.get_children(self.board, self.big_board, self.next_subgame, self.player_to_act):
            self.children.append(Node(child['board'], child['big_board'], child['next_subgame'], child['player_to_act'], child['is_win']))

    def play_random_game(self):
        # todo

        return 1  # return the winner
