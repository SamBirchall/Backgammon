import curses
from curses import ascii
from curses import panel
from curses import wrapper

screen = curses.initscr()
def main(screen):
    
    while True:
        char = screen.getkey()
        if char == "KEY_RIGHT":
            screen.addstr(1 ,5, "You pressed KEY RIGHT")
        elif char == "KEY_UP":
            screen.addstr(1 ,5, "You pressed KEY UP   ")
        elif char == "KEY_DOWN":
            screen.addstr(1 ,5, "You pressed KEY Down ")
        elif char == "KEY_LEFT":
            screen.addstr(1, 5, "You pressed KEY Left ")
        else:
            screen.addstr(1, 5, char)
        screen.refresh()
    
    
    curses.endwin() #hello

wrapper(main)