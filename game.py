
import random
import curses 
from curses import ACS_CKBOARD, ACS_DIAMOND
import math

class Die():
        
    def roll(self):
        return random.randint(1, 6)


class Bgboard(object):
    def __init__(self, beginy, beginx, height, width, die1, die2, points):
        
        self.begin_y = beginy
        self.begin_x = beginx
        self.height = height
        self.width = width
        self.die1 = None
        self.die2 = None
        self.num_points = points
        self.p1_tokens = ACS_CKBOARD
        self.p2_tokens = ACS_DIAMOND
        

    def drawboard(self, beginy, beginx, height, width):

        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
         
        win = curses.newwin(height, width, beginy, beginx)
        return win

    
    


        


        




