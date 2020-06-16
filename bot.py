import time
import random
import copy
import math


class Bot():
    def __init__(self, MAX_TIME):
        # seed the random number generator
        random.seed = time.time()

        # time limit for thinking in seconds
        self.MAX_TIME = MAX_TIME

        self.MY_NUMBER = -1

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
        root = Node(board, big_board, next_subgame, -1, 0, 'root')  # create the root

        # main loop
        while time.time() - self.MAX_TIME < start_time:  # do loop until out of time
            # selection
            current_node = root
            node_chain = [current_node]
            while current_node.num_visits > 0:  # keep searching until we have a node with no visits
                max_score = -1
                for child in current_node.children:
                    if child.num_visits == 0:
                        child_score = 999999
                    elif child.is_win != 0:
                        child_score = -1  # can't select nodes that are wins
                    else:
                        parent_visits = current_node.num_visits

                        parent_player = current_node.player_to_act

                        num_wins = child.outcomes[parent_player] + 0.5 * child.outcomes[2]

                        win_ratio = num_wins / child.num_visits
                        
                        explore_component = math.sqrt(2) * math.sqrt(math.log(parent_visits) / child.num_visits)
                        child_score = win_ratio + explore_component

                    if child_score > max_score:
                        max_score = child_score
                        max_node = child

                # new current node 
                current_node = max_node
                node_chain.append(current_node)
            
            # expansion
            if current_node.is_win == 0:
                current_node.update_children()                    

            # simulation
            simulation_winner = self.simulate_game(current_node)

            # backpropogation
            for node in node_chain:  # update wins and visits for nodes in the chain
                node.num_visits += 1
                node.outcomes[simulation_winner] += 1
        
        # find best move from the game tree and return it
        best_child_score = -1
        for child in root.children:
            if child.num_visits == 0:  # this should not happen if the bot is given sufficient time
                child_score = 0
            else:
                child_score = (child.outcomes[-1] + 0.5 * child.outcomes[2]) / child.num_visits

            if child_score > best_child_score:
                best_child_score = child_score
                best_child_node = child

        # draw the tree -- mostly testing
        self.draw_tree(root)
        print(f"selected move {best_child_node.id}")

        return best_child_node.board, best_child_node.big_board, best_child_node.next_subgame


    def simulate_game(self, start_node):
        current_node = Node(start_node.board, start_node.big_board, start_node.next_subgame, start_node.player_to_act, start_node.is_win)
        
        # go to random moves until there is a win
        while current_node.is_win == 0:
            # generate children
            current_node.update_children()

            # pick a random child and reset current node
            num_children = len(current_node.children)


            if num_children == 0:  # testing, looking for a bug
                self.render_board(current_node.board, current_node.big_board)
                print(current_node.is_win)


            current_node = current_node.children[random.randrange(num_children)]

            #self.render_board(current_node.board, current_node.big_board)  # testing

        return current_node.is_win  # return winner, 1 or -1


    def draw_tree(self, root, max_depth=999, show_no_visit_nodes=False):
        # draw the tree in dfs
        node_stack = [(root, 0)]  # format for entries is (node, depth)
        while len(node_stack) > 0:  # run until stack is empty
            # get top node
            (top_node, depth) = node_stack.pop()

            # draw node if less than max_depth
            if depth < max_depth:
                if depth == 0:
                    print(f"{top_node.id}: {top_node.outcomes[-1]} {top_node.outcomes[2]} {top_node.outcomes[1]} / {top_node.num_visits}")
                else:
                    if show_no_visit_nodes or top_node.num_visits > 0:
                        print("    " * (depth - 1) + "----" + f"{top_node.id}: {top_node.outcomes[-1]} {top_node.outcomes[2]} {top_node.outcomes[1]} / {top_node.num_visits}")

            # add children to stack
            for child in top_node.children:  
                node_stack.append((child, depth + 1))
        print()  # add a newline

    
    def render_board(self, board, big_board):  # for testing only
        ROW_LABELS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        COLUMN_LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        
        print()

        for i in range(9):
            print(f"{ROW_LABELS[8 - i]} ", end="")  # row label
            for j in range(9):
                # check big board then full board
                if big_board[math.floor(i / 3)][math.floor(j / 3)] == 1:
                    print('X', end="")
                elif big_board[math.floor(i / 3)][math.floor(j / 3)] == -1:
                    print('O', end="")
                elif board[i][j] == 0:
                    print(' ', end="")
                elif board[i][j] == 1:
                    print('X', end="")
                elif board[i][j] == -1:
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
            print(f"{COLUMN_LABELS[j]} ", end="")            
        print()


class Node():
    def __init__(self, board, big_board, next_subgame, player_to_act, is_win, id="node"):
        # game state info
        self.board = board
        self.big_board = big_board
        self.next_subgame = next_subgame
        self.player_to_act = player_to_act
        self.is_win = is_win

        # for MCTS
        self.children = []  # list of child nodes
        self.num_visits = 0
        self.outcomes = {-1: 0, 1: 0, 2: 0}

        # needed for drawing tree
        self.id = id


    def get_children(self, board, big_board, next_subgame, player_to_act):
        # needed for naming children
        ROW_LABELS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        COLUMN_LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        children = []

        if next_subgame == (-1, -1):
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:  # open square
                        temp_child = {}
                        temp_child['board'] = copy.deepcopy(board)
                        temp_child['board'][i][j] = player_to_act
                        temp_child['next_subgame'] = (i % 3, j % 3)

                        temp_child['id'] = COLUMN_LABELS[j] + ROW_LABELS[8 - i]

                        children.append(temp_child)
        else:
            for i in range(3):
                for j in range(3):
                    if board[next_subgame[0] * 3 + i][next_subgame[1] * 3 + j] == 0:  # open square
                        temp_child = {}
                        temp_child['board'] = copy.deepcopy(board)
                        temp_child['board'][next_subgame[0] * 3 + i][next_subgame[1] * 3 + j] = player_to_act
                        temp_child['next_subgame'] = (i % 3, j % 3)

                        temp_child['id'] = COLUMN_LABELS[next_subgame[1] * 3 + j] + ROW_LABELS[8 - (next_subgame[0] * 3 + i)]

                        children.append(temp_child)

        # compute bigboard and add player to act and make sure next_subgame is correct
        row_indices = [i + 3 * next_subgame[0] for i in [0, 1, 2]]
        col_indices = [i + 3 * next_subgame[1] for i in [0, 1, 2]]

        for child in children:
            # add the big_board
            child['big_board'] = copy.deepcopy(big_board)

            # player to act
            child['player_to_act'] = player_to_act * -1

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
            for p in range(3):
                diag_sum += child['board'][row_indices[0] + p][col_indices[0] + p]
    
            if diag_sum == 3:
                child['big_board'][i][j] = 1
                need_update = True
            elif diag_sum == -3:
                child['big_board'][i][j] = -1
                need_update = True

            # forwards diag
            diag_sum = 0
            for p in range(3):
                diag_sum += child['board'][row_indices[0] + p][col_indices[-1] - p]

            if diag_sum == 3:
                child['big_board'][i][j] = 1
                need_update = True
            elif diag_sum == -3:
                child['big_board'][i][j] = -1
                need_update = True

            child['is_win'] = 0
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
                    elif row_sum == -3:
                        child['is_win'] = -1
                    
                # check the cols
                for n in row_indices:
                    col_sum = 0
                    for m in col_indices:
                        col_sum += child['big_board'][m][n]
                    
                    if col_sum == 3:
                        child['is_win'] = 1
                    elif col_sum == -3:
                        child['is_win'] = -1

                # check the diagonals
                # backwards diag
                diag_sum = 0
                for p in range(3):
                    diag_sum += child['big_board'][row_indices[0] + p][col_indices[0] + p]

                if diag_sum == 3:
                    child['is_win'] = 1
                elif diag_sum == -3:
                    child['is_win'] = -1

                # forwards diag
                diag_sum = 0
                for p in range(3):
                    diag_sum += child['big_board'][row_indices[0] + p][col_indices[-1] - p]

                if diag_sum == 3:
                    child['is_win'] = 1
                elif diag_sum == -3:
                    child['is_win'] = -1
            
            # make sure next_subgame is correct
            check_draw = False
            i = child['next_subgame'][0]
            j = child['next_subgame'][1]
            if child['big_board'][i][j] != 0:
                child['next_subgame'] = (-1, -1)
                check_draw = True
            else:
                # check if subgame full
                finished_cells = 0
                for m in range(3):
                    for n in range(3):
                        if child['board'][3 * i + m][3 * j + n] != 0:
                            finished_cells += 1
                
                if finished_cells == 9:  # if subgame draw
                    check_draw = True
                    child['next_subgame'] = (-1, -1)
                
            if check_draw:  # check if entire game full
                finished_games = 0
                for i in range(3):
                    for j in range(3):
                        if child['big_board'][i][j] != 0:
                            finished_games += 1
                        else:
                            finished_cells = 0
                            for m in range(3):
                                for n in range(3):
                                    if child['board'][3 * i + m][3 * j + n] != 0:
                                        finished_cells += 1
                            if finished_cells == 9:
                                finished_games += 1
                
                if finished_games == 9:  # if draw
                    #random_win = random.randrange(2) * 2 - 1  # 1 or -1  # old, set winner to random win
                    child['is_win'] = 2

        return children


    def update_children(self):
        children = self.get_children(self.board, self.big_board, self.next_subgame, self.player_to_act)    

        for child in children:
            self.children.append(Node(child['board'], child['big_board'], child['next_subgame'], child['player_to_act'], child['is_win'], child['id']))
