import time
import random
import copy
import math

from shared import *

class Bot():
    def __init__(self, MAX_TIME):
        # seed the random number generator
        random.seed = time.time()

        # time limit for thinking in seconds
        self.MAX_TIME = MAX_TIME


    def get_move(self, board, big_board, next_subgame):
        # get the current time
        start_time = time.time()

        # make the root node
        root = Node(board, big_board, next_subgame, -1, 2, 'root')  # create the root
        root.generate_children()

        # main loop
        nodes_searched = 0
        while time.time() - self.MAX_TIME < start_time:  # do loop until out of time
            nodes_searched += 1
            
            # selection
            current_node = root
            node_chain = [current_node]

            # for dfs in choosing a node
            visited = set([root])

            while current_node.num_visits > 0 or current_node == root:  # keep searching until we have a node with no visits
                # check children
                non_visited_children = []
                for child in current_node.children:
                    if child not in visited:
                        non_visited_children.append(child)

                if len(non_visited_children) > 0:
                    # pick a child
                    max_score = -1
                    for child in non_visited_children:
                        if child.num_visits == 0:
                            # select child
                            max_child = child
                            break

                        parent_player = current_node.player_to_act
                        num_wins = child.simulation_outcomes[parent_player] + 0.5 * child.simulation_outcomes[-1]
                        win_ratio = num_wins / child.num_visits

                        parent_visits = current_node.num_visits
                        explore_component = math.sqrt(2) * math.sqrt(math.log(parent_visits) / child.num_visits)
                        
                        child_score = win_ratio + explore_component

                        if child_score > max_score:
                            max_score = child_score
                            max_child = child

                    current_node = max_child
                    node_chain.append(current_node)
                else:                   
                    # check if at root
                    if current_node == root:
                        # tree is complete
                        break
                    
                    # go up the chain
                    del node_chain[-1]
                    current_node = node_chain[-1]

                # add node to visited set
                if current_node not in visited:
                    visited.add(current_node)

            # check if tree complete
            if current_node == root:
                print("tree complete")
                break

            # expansion
            current_node.generate_children()

            # simulation
            simulation_result = current_node.simulate_game()

            # backpropogation
            for node in node_chain:
                node.num_visits += 1
                node.simulation_outcomes[simulation_result] += 1
            
        # find the best move
        best_child_score = -2
        for child in root.children:
            if child.is_win == 2:  # bot win
                # pick the move, don't need to do anything else
                best_child_node = child
                break
            elif child.is_win == 1:  # player win
                child_score = -1
            elif child.is_win == -1:  # draw
                child_score = 0
            else:
                child_score = (child.simulation_outcomes[2] + 0.5 * child.simulation_outcomes[-1]) / child.num_visits

            if child_score > best_child_score:
                best_child_node = child
                best_child_score = child_score

        # draw the tree
        draw_tree(root)

        # output move
        print(f"bot played { best_child_node.id }, result of searching { nodes_searched } nodes")

        return best_child_node.move


class Node():
    def __init__(self, board, big_board, next_subgame, move, player_to_act, id="node"):
        # game state info
        self.board = board
        self.big_board = big_board
        self.next_subgame = next_subgame
        self.move = move
        self.player_to_act = player_to_act
        self.is_win = check_win(big_board)
        
        # for MCTS
        self.children = []  # list of child nodes
        self.num_visits = 0
        self.simulation_outcomes = {
            1: 0, 2: 0, -1: 0
        }

        # needed for drawing tree
        self.id = id


    def generate_children(self):
        # make sure we need to do this
        if len(self.children) == 0:
            # needed for naming children
            ROW_LABELS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            COLUMN_LABELS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

            # get potential moves
            potential_moves = []
            if self.next_subgame == -1:
                # need to check all squares
                for i in range(len(self.board)):
                    if self.board[i] == 0:
                        potential_moves.append(i)
            else:
                # just need to check subgame squares
                for i in range(9 * self.next_subgame, 9 * self.next_subgame + 9):
                    if self.board[i] == 0:
                        potential_moves.append(i)

            # make a child for each of the potential moves
            for move in potential_moves:
                new_board = copy.deepcopy(self.board)
                new_board[move] = self.player_to_act
                
                # todo
                new_id = COLUMN_LABELS[move % 9] + ROW_LABELS[math.floor(move / 9)]
                
                
                new_board, new_big_board = update_big_board(new_board, copy.deepcopy(self.big_board), move)
                if new_big_board[move % 9] == 0:
                    new_next_subgame = move % 9
                else:
                    new_next_subgame = -1
                if self.player_to_act == 1:
                    new_player_to_act = 2
                else:
                    new_player_to_act = 1
                self.children.append(Node(new_board, new_big_board, new_next_subgame, move, new_player_to_act, new_id))


    def simulate_game(self):
        # need to make a copy of the node
        current_node = copy.deepcopy(self)

        # main loop
        while current_node.is_win == 0:
            # get children
            current_node.generate_children()

            # pick random child
            num_children = len(current_node.children)
            current_node = current_node.children[random.randrange(num_children)]

        return current_node.is_win
