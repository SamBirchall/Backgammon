import curses
import sys
import random
import numpy as np
from curses import window
from random import randint
from curses import wrapper

N_LINES = 64
N_COLS = 64

debug = open("debug.txt", "w")

class Dice(object):
    def makeRoll(self):
        self.value = str(randint(1, 6))
        return self.value

    def drawDice(self, screen):
        dice = curses.newwin(3, 3, N_LINES-3, N_COLS-3)
        dice.border()
        x = str(self.value)
        dice.addstr(1, 1, x)
        dice.refresh()
        return dice

class BgBoard(object):

    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        self.p1board = None
        self.p2board = None
        self.jail = None
        self.safe = None
        self.p1tokens = []
        self.p2tokens = []
   
    def drawInitialBoard(self):
        self.screen.border() 
        self.screen.refresh()
    
    def drawPlayerBoards(self):
        screenWidth = self.screen.getmaxyx()[1]
        screenHeight = self.screen.getmaxyx()[0]
        self.p1board = curses.newwin(30, 30, 1, 1)
        self.p1board.border()
        self.p1board.refresh()
        self.p2board = curses.newwin(30, 30, 1, 32)
        self.p2board.border()
        self.p2board.refresh()
        return self.p1board, self.p2board
    
    def drawHomeBoard(self, playerBoard):
        pass

    def drawOuterBoard(self, playerBoard):
        pass

class PlayerBoard(object):
    def __init__(self):
        self.board = [{0:{"tokenType": 1, "number": 2}, 1:{"tokenType": 1, "number": 3}, 2:{"tokenType": 1, "number": 0}, 3:{"tokenType": 1, "number": 0},  4:{"tokenType": 1, "number": 0}, 5:{"tokenType": 1, "number": 0}},
        {0:{"tokenType": 1, "number": 0}, 1:{"tokenType": 1, "number": 0}, 2:{"tokenType": 1, "number": 4}, 3:{"tokenType": 1, "number": 2}, 4:{"tokenType": 1, "number": 3}, 5:{"tokenType": 1, "number": 0}}]


    def drawBoard(self, board, p1token, p2token):
        for i in range(2): #homeBoard, outerBoard
            for j in range(6): #prongs
                prong = self.board[i][j]
                for x in range(prong["number"]):
                    print(x, file=debug)
                    if prong["tokenType"] == 1:
                        character = p1token 
                    else:
                        character = p2token

                    board.addstr(x*2+1, j*5+1+30*i, character)
        board.refresh()

def main():
    
    try:
        bgBoard = BgBoard()
        pBoard = PlayerBoard()
        bgBoard.drawInitialBoard()
        bgBoard.drawPlayerBoards()
        pBoard.drawBoard(bgBoard.p1board, "A", "B")
    
        curses.curs_set(False)
    except:
        e = sys.exc_info()[0]
        print(e, file=debug)
    curses.napms(7000)
    curses.endwin()
wrapper(main())
