import curses
import sys
import random
import numpy as np
# from curses import window
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
        self.outerBoard = curses.newwin(22, 30, 1, 1)
        self.outerBoard.border()
        self.outerBoard.refresh()
        self.innerBoard = curses.newwin(22, 30, 1, 32)
        self.innerBoard.border()
        self.innerBoard.refresh()
      
        return self.innerBoard, self.outerBoard
    
  

class PlayerBoard(object):
    def __init__(self, player, p1token, p2token, board1, board2):
        self.board = [{0:{"tokenType": 2, "number": 2}, 
        1:{"tokenType": 1, "number": 0}, 
        2:{"tokenType": 1, "number": 0}, 
        3:{"tokenType": 1, "number": 0},  
        4:{"tokenType": 1, "number": 0}, 
        5:{"tokenType": 1, "number": 5}},
        {0:{"tokenType": 1, "number": 0}, 
        1:{"tokenType": 1, "number": 3}, 
        2:{"tokenType": 1, "number": 0}, 
        3:{"tokenType": 1, "number": 0}, 
        4:{"tokenType": 1, "number": 0}, 
        5:{"tokenType": 2, "number": 5}}]

        self.jail = []
        self.safe = []
        self.player = player
        self.p1token = p1token
        self.p2token = p2token
        self.boards = [board1, board2]
        
        self.boardHeight = board1.getmaxyx()[0]
        self.boardWidth = board1.getmaxyx()[1]
        
    def drawBoard(self):
        for i in range(2):
            for j in range(6): #prongs
                prong = self.board[i][j]
                # for x in range(prong["number"]):
                for x in range(6):
                    if x < prong["number"]:
                        if prong["tokenType"] == 1:
                            character = self.p1token
                        else:
                            character = self.p2token
                    else:
                        character = " "
                    if self.player == 1:
                        self.boards[i].addstr(x*2+1, self.boardWidth-(j*5+3), character)
                    elif self.player == 2:
                        self.boards[i].addstr(self.boardHeight-(x*2+2), self.boardWidth-(j*5+3), character)
            self.boards[i].refresh()

    def changeBoard(self, board, prong, playerNumber, add=1):
        """
        board: 0: inner, 1: outer
        prong
        add: 1 to add 1, -1 to take away
        playerNumber
        """
        if self.board[board][prong]["tokenType"] != playerNumber:
            if add > 0:
                if self.board[board][prong]["number"] == 0:
                    self.board[board][prong]["tokenType"] = playerNumber
                elif self.board[board][prong]["number"] == 1:
                    raise Exception("players do not match")
            else:
                raise Exception("players do not match")
        if add > 0:
            if self.board[board][prong]["number"] >= 5:
                raise Exception(f"prong {prong} already full on board {board}")
            else:
                self.board[board][prong]["number"] += add
        if add < 0:
            if self.board[board][prong]["number"] <= 0:
                raise Exception(f"prong {prong} already empty on board {board}")
            else:
                self.board[board][prong]["number"] += add
                print(self.board[board][prong]["number"], file=debug)


class Game(object):
    def __init__(self, screen):
        self.bgBoard = BgBoard()
        self.dice1 = Dice(9, 64)
        self.dice2 = Dice(14, 64)
        
        screen = self.bgBoard.screen
        
        self.screen = screen
        self.bgBoard.drawInitialBoard()
        self.bgBoard.drawPlayerBoards()

        self.p1Board = PlayerBoard(1, PLAYERONE_TOKEN, PLAYERTWO_TOKEN, self.bgBoard.innerBoard, self.bgBoard.outerBoard)
        self.p2Board = PlayerBoard(2, PLAYERTWO_TOKEN, PLAYERONE_TOKEN, self.bgBoard.innerBoard, self.bgBoard.outerBoard)
        

        self.p1Board.drawBoard()
        self.p2Board.drawBoard()

        self.dice1.draw()
        self.dice2.draw()

    def checkScreenSize(self):
        height = self.screen.getmaxyx()[0]
        width = self.screen.getmaxyx()[1]
        if height <= 23:
            raise Exception("Terminal window does not fit board size, window must be greater than 24 by 80")
        elif width <= 50:
            raise Exception("Terminal window does not fit board size, window must be greater than 24 by 60")

    def mainLoop(self):
        curses.curs_set(False)
        while True:
            char = self.screen.getkey()
            if char == "q":
                break
            elif char == "KEY_UP":
                self.p1Board.changeBoard(0, 1, 1, 1)
                self.p1Board.drawBoard()
            elif char == "KEY_DOWN":
                self.p1Board.changeBoard(0, 1, 1,-1)
                self.p1Board.drawBoard()
            

def main(screen):
    game = Game(screen)
    game.checkScreenSize()
  
    game.mainLoop()
    
wrapper(main)
