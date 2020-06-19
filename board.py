import curses
import sys
import random
import numpy as np
from random import randint
from curses import wrapper

PLAYERONE_TOKEN = "\u2593"
PLAYERTWO_TOKEN = "\u2591"

CURSOR_CHAR = "\u2588"

debug = open("debug.txt", "w")

class Dice(object):
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.dice = curses.newwin(3, 3, self.y, self.x)
        self.roll()
        
    def roll(self):
        self.number = str(randint(1, 6))
        self.draw()
        return self.number

    def draw(self):
        self.dice.border()
        self.dice.addstr(1, 1, self.number)
        self.dice.refresh()

    def getNumber(self):
        return int(self.number)

class PlayerIndicator(object):
    def __init__(self, y, x, p1token, p2token):
        self.y = y
        self.x = x
        self.tokens = [p2token, p1token]
        self.currentplayer = 0
        self.window = curses.newwin(3,3, self.y, self.x)

    def changePlayer(self, player=None):
        self.window.border()
        if type(player) == int:
            self.currentplayer = player
        else:
            self.currentplayer += 1
            self.currentplayer %= 2
        self.window.addstr(1,1, self.tokens[self.currentplayer])
        self.window.refresh()
        return self.currentplayer

class Log(object):
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.window = curses.newwin(3, 9+2, self.y, self.x)

    def newMsg(self, msg):
        msgDict = {" ":"SPACE", "\n":"ENTER", "\t":"TAB"}
        if msg in msgDict.keys(): msg=msgDict[msg]
        self.window.border()
        self.window.addstr(1,1, f'{msg:>9}')
        self.window.refresh()

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

class Jail(object):
    pass

class Safe(object):
    pass
    
        
class PlayerBoard(object):
    def __init__(self, player, p1token, p2token, board1, board2):
        self.currentCursorPos = False # prong, position
        self.board = [ # 1: red/clockwise, 0: black/anticlockwise
            {"tokenType": 1, "number": 2},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 5},

            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 3},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 1, "number": 5},
            
            {"tokenType": 0, "number": 5},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 1, "number": 3},
            {"tokenType": 0, "number": 0},
            
            {"tokenType": 1, "number": 5},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 0},
            {"tokenType": 0, "number": 2}
        ]

        self.jail = {1:0, 2:0}
        self.safe = {1:0, 2:0}
        self.player = player
        self.p1token = p1token
        self.p2token = p2token
        self.cursesBoards = [board1, board2] # left, right?
        
        self.boardHeight = board1.getmaxyx()[0]
        self.boardWidth = board1.getmaxyx()[1]

    def drawCharacter(self, prong, position, character):
        '''
        prong: 0 to 23, the prong to display on
        position: how far up or down the prong to display the character on
        character: the character to display
        '''
        cursesBoard = 1 if (prong > 5 and prong < 18) else 0

        if position == "end":
            position = self.prongInfo(prong)["number"] - 0.5

        if prong < 12: # bottom
            self.cursesBoards[cursesBoard].addstr(int(self.boardHeight-(position*2+2)), self.boardWidth-((prong%6)*5+3), character)
        else: # top
            self.cursesBoards[cursesBoard].addstr(int(position*2+1), int((prong%6)*5+2), character)
        
    def drawBoard(self):
        for i in range(24):
            prong = self.board[i]
            for x in range(6):
                if x < prong["number"]:
                    character = self.p1token if prong["tokenType"] == 1 else self.p2token
                else:
                    character = " "

                self.drawCharacter(i, x, character)

        self.refreshCursesBoards()

    def prongInfo(self, prong):
        """
        {"tokenType":, "number"}
        """
        return self.board[prong]

    def refreshCursesBoards(self):
        for board in self.cursesBoards:
            board.refresh()
    
    def moveCursor(self, prong):
        if self.currentCursorPos:
            self.drawCharacter(*self.currentCursorPos, " ")
        
        self.currentCursorPos = [prong, self.prongInfo(prong)["number"] - 0.5]

        self.drawCharacter(*self.currentCursorPos, CURSOR_CHAR)

    def changeBoard(self, prong, playerNumber, add=1):
        """
        prong: which prong to add the token to
        add: 1 to add 1, -1 to take away
        playerNumber: which player the token belongs to
        """
        if self.board[prong]["tokenType"] != playerNumber:
            if add > 0:
                if self.board[prong]["number"] == 0:
                    self.board[prong]["tokenType"] = playerNumber
                elif self.board[prong]["number"] == 1:
                    raise Exception("players do not match")
            else:
                raise Exception("players do not match")
        if add > 0:
            if self.board[prong]["number"] >= 5:
                raise Exception(f"prong {prong} already full on board {board}")
            else:
                self.board[prong]["number"] += add
        if add < 0:
            if self.board[prong]["number"] <= 0:
                raise Exception(f"prong {prong} already empty on board {board}")
            else:
                self.board[prong]["number"] += add
                print(self.board[prong]["number"], file=debug)        


class Game(object):
    def __init__(self, screen):
        self.tempChars = []

        self.bgBoard = BgBoard()
        self.dice1 = Dice(9, 64)
        self.dice2 = Dice(14, 64)

        self.currentPlayerIndicator = PlayerIndicator(3, 64, PLAYERONE_TOKEN, PLAYERTWO_TOKEN)
        
        self.log = Log(3, 75)
        
        screen = self.bgBoard.screen
        
        self.screen = screen
        self.bgBoard.drawInitialBoard()
        self.bgBoard.drawPlayerBoards()

        self.pBoard = PlayerBoard(1, PLAYERONE_TOKEN, PLAYERTWO_TOKEN, self.bgBoard.innerBoard, self.bgBoard.outerBoard)
        self.pBoard.drawBoard()

        self.dice1.draw()
        self.dice2.draw()
        self.currentPlayerIndicator.changePlayer(0)
        


    def getMoveValues(self):
        moveValues = []
        if self.dice1.getNumber() == self.dice2.getNumber():
            for i in range(4):
                moveValues.append(self.dice2.getNumber())
        else:
            moveValues.append(self.dice1.getNumber())
            moveValues.append(self.dice2.getNumber())

        return moveValues
 
    def validProng(self, player, number, startProng, bearingOff=False):
        """
        checks whether the prong <number> from <startProng> is valid for <player> to move to
        returns: -1 if no prong, otherwise the number of the prong
        """

        currentProng = startProng
        currentProng += number # TODO: -= number for one player, += number for the other

        if bearingOff: # TODO:
            pass
        else:
            if currentProng < 24 and currentProng > -1:
                if (self.pBoard.prongInfo(currentProng)["tokenType"] == player and self.pBoard.prongInfo(currentProng)["number"] < 5) or self.pBoard.prongInfo(currentProng)["number"] == 0:
                    return currentProng
        
        return -1

    def checkScreenSize(self):
        height = self.screen.getmaxyx()[0]
        width = self.screen.getmaxyx()[1]
        if height <= 23:
            raise Exception("Terminal window does not fit board size, window must be greater than 24 by 80")
        elif width <= 50:
            raise Exception("Terminal window does not fit board size, window must be greater than 24 by 60")

    def mainLoop(self):
        curses.curs_set(False)
        currentProng = 0
        currentDiceRoll = [self.dice1.roll(), self.dice2.roll()]
        currentPlayer = 0

        self.pBoard.moveCursor(currentProng)
        self.pBoard.refreshCursesBoards()

        while True:
            char = self.screen.getkey()
            self.log.newMsg(char)
            if char == "q":
                break
            elif char == "p":
                currentPlayer = self.currentPlayerIndicator.changePlayer()
                currentDiceRoll = self.dice1.roll() + self.dice2.roll()
            elif char == "KEY_RIGHT" or "KEY_LEFT":
                foundProng = False
                while not foundProng:
                    if char == "KEY_RIGHT":
                        currentProng += 1
                    else:
                        currentProng -= 1
                    currentProng %= 24

                    if self.pBoard.prongInfo(currentProng)["tokenType"] == currentPlayer and self.pBoard.prongInfo(currentProng)["number"] != 0:
                        foundProng = True

                self.pBoard.moveCursor(currentProng)

                # TODO: display possible moves from the position using getMoveValues() method
                if self.tempChars:
                    for char in self.tempChars:
                        self.pBoard.drawCharacter(char, "end", " ")
                    self.tempChars = []
                for value in self.getMoveValues():
                    endProng = self.validProng(currentPlayer, value, currentProng)
                    if endProng >= 0:
                        self.pBoard.drawCharacter(endProng, "end", "U")
                        self.tempChars.append(endProng)

                self.pBoard.refreshCursesBoards()


def main(screen):
    game = Game(screen)
    game.checkScreenSize()
  
    game.mainLoop()
    
wrapper(main)
