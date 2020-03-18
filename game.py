
import random
import math

class Die():
        
    def roll(self):
        return random.randint(1, 6)

class Bgboard:
    def __init__(self, xdim, ydim, die, points, p1_tokens, p2_tokens):
        self.x_dim = xdim
        self.y_dim = ydim
        self.die = None
        self.num_points = points
        self.p1_tokens = p1_tokens
        self.p2_tokens = p2_tokens

    def board(self, xdim, ydim):

        print(('\u250c'), ('\u2500')*(self.x_dim), ('\u2510') )
        print('\u2502\n'*self.y_dim)

bg = Bgboard(10, 10, 10, 10, 10, 10)
bg.board(10, 10)
