import time
import random

class Bot():
    def __init__(self):
        # seed the random number generator
        random.seed = time.time()

    def get_move(self, board, next_subgame):
        node = Node()
        return board, next_subgame


class Node():
    def __init__(self):
        pass