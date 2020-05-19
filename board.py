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
        self.innerBoard = None
        self.outerBoard = None
        self.p1tokens = []
        self.p2tokens = []
   
    def drawInitialBoard(self):
        self.screen.border() 
        self.screen.refresh()
    
    def drawPlayerBoards(self):
        screenWidth = self.screen.getmaxyx()[1]
        screenHeight = self.screen.getmaxyx()[0]
        self.innerBoard = curses.newwin(30, 30, 1, 1)
        self.innerBoard.border()
        self.innerBoard.refresh()
        self.outerBoard = curses.newwin(30, 30, 1, 32)
        self.outerBoard.border()
        self.outerBoard.refresh()
        return self.innerBoard, self.outerBoard
    
    def drawHomeBoard(self, playerBoard):
        pass

    def drawOuterBoard(self, playerBoard):
        pass

class PlayerBoard(object):
    def __init__(self):
        self.board = [{0:{"tokenType": 2, "number": 2}, 1:{"tokenType": 1, "number": 0}, 2:{"tokenType": 1, "number": 0}, 3:{"tokenType": 1, "number": 0},  4:{"tokenType": 1, "number": 0}, 5:{"tokenType": 1, "number": 5}},
        {0:{"tokenType": 1, "number": 0}, 1:{"tokenType": 1, "number": 3}, 2:{"tokenType": 1, "number": 0}, 3:{"tokenType": 1, "number": 0}, 4:{"tokenType": 1, "number": 0}, 5:{"tokenType": 2, "number": 5}}]
        self.jail = []
        self.safe = []

    def drawBoard(self, board, p1token, p2token, i, player):
        boardHeight = board.getmaxyx()[0]
        #for i in range(2): #homeBoard, outerBoard
        if player == 1:
            for j in range(6): #prongs
                prong = self.board[i][j]
                for x in range(prong["number"]):
                    print(x, file=debug)
                    if prong["tokenType"] == 1:
                        character = p1token 
                    else:
                        character = p2token

                    board.addstr(x*2+1, j*5+2, character)
        else:
            for j in range(6): #prongs
                prong = self.board[i][j]
                for x in range(prong["number"]):
                    
                    if prong["tokenType"] == 1:
                        character = p1token 
                    else:
                        character = p2token

                    board.addstr(boardHeight-(x*2+2), j*5+2, character)
        board.refresh()
    
bgBoard = BgBoard()
pBoard = PlayerBoard()
screen = bgBoard.screen

def main(screen):
    

    bgBoard.drawInitialBoard()
    bgBoard.drawPlayerBoards()
    pBoard.drawBoard(bgBoard.innerBoard, "A", "B", 0, 1) #draw outerBoard
    pBoard.drawBoard(bgBoard.outerBoard, "A", "B", 1, 1) #draw homeBoard
    pBoard.drawBoard(bgBoard.innerBoard, "A", "B", 0, 2) #draw outerBoard
    pBoard.drawBoard(bgBoard.outerBoard, "B", "A", 1, 2) #draw homeBoard
    curses.curs_set(False)
  
    screen.getkey()
    
wrapper(main)
