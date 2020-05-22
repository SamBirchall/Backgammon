import curses
import sys
import random
import numpy as np
from curses import window
from random import randint
from curses import wrapper

# PLAYERONE_TOKEN = "A"
# PLAYERTWO_TOKEN = "B"

PLAYERONE_TOKEN = "\u2591"
PLAYERTWO_TOKEN = "\u2593"


debug = open("debug.txt", "w")

class Dice(object):
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.roll()
        
    def roll(self):
        self.number = str(randint(1, 6))
        # return self.number

    def draw(self):
        dice = curses.newwin(3, 3, self.y, self.x)
        dice.border()
        dice.addstr(1, 1, self.number)
        dice.refresh()
        # return dice

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
        self.outerBoard = curses.newwin(30, 30, 1, 1)
        self.outerBoard.border()
        self.outerBoard.refresh()
        self.innerBoard = curses.newwin(30, 30, 1, 32)
        self.innerBoard.border()
        self.innerBoard.refresh()
      
        return self.innerBoard, self.outerBoard
    
  

class PlayerBoard(object):
    def __init__(self):
        self.board = [{0:{"tokenType": 2, "number": 2}, 1:{"tokenType": 1, "number": 0}, 2:{"tokenType": 1, "number": 0}, 3:{"tokenType": 1, "number": 0},  4:{"tokenType": 1, "number": 0}, 5:{"tokenType": 1, "number": 5}},
        {0:{"tokenType": 1, "number": 0}, 1:{"tokenType": 1, "number": 3}, 2:{"tokenType": 1, "number": 0}, 3:{"tokenType": 1, "number": 0}, 4:{"tokenType": 1, "number": 0}, 5:{"tokenType": 2, "number": 5}}]
        self.jail = []
        self.safe = []

    def drawBoard(self, board, p1token, p2token, i, player):
        boardHeight = board.getmaxyx()[0]
        boardWidth = board.getmaxyx()[1]
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

                    board.addstr(x*2+1, boardWidth-(j*5+3), character)
        else:
            for j in range(6): #prongs
                prong = self.board[i][j]
                for x in range(prong["number"]):
                    
                    if prong["tokenType"] == 1:
                        character = p1token 
                    else:
                        character = p2token

                    board.addstr(boardHeight-(x*2+2), boardWidth-(j*5+3), character)
        board.refresh()
    
bgBoard = BgBoard()
pBoard = PlayerBoard()
dice1 = Dice(15, 64)
dice2 = Dice(19, 64)
screen = bgBoard.screen

def main(screen):

    bgBoard.drawInitialBoard()
    bgBoard.drawPlayerBoards()
    pBoard.drawBoard(bgBoard.innerBoard, PLAYERONE_TOKEN, PLAYERTWO_TOKEN, 0, 1) #draw outerBoard
    pBoard.drawBoard(bgBoard.outerBoard, PLAYERONE_TOKEN, PLAYERTWO_TOKEN, 1, 1) #draw homeBoard
    pBoard.drawBoard(bgBoard.innerBoard, PLAYERTWO_TOKEN, PLAYERONE_TOKEN, 0, 2) #draw outerBoard
    pBoard.drawBoard(bgBoard.outerBoard, PLAYERTWO_TOKEN, PLAYERONE_TOKEN, 1, 2) #draw homeBoard
    
    # dice1.draw()
    # dice2.draw()
    # while True:
    #     char = screen.getkey()
    #     print(char, file=debug)
    #     if char == "1":
    #         # print("enter was pressed", file=debug)
    #         dice1.roll()
    #         dice1.draw()
    #         screen.refresh()
    #     if char == "2":
    #         dice2.roll()
    #         dice2.draw()
    #         screen.refresh()
    #     elif char == "q":
    #         break

    curses.curs_set(False)
  
    screen.getkey()
    
wrapper(main)
