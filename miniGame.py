import curses
from curses import wrapper

screen = curses.initscr()

def main(screen):
    x=0
    y=0
    while True:
        char = screen.getkey()
        if char == "q":
            break
        elif char == "KEY_RIGHT":
            x += 1
        elif char == "KEY_UP":
            y -= 1
        elif char == "KEY_DOWN":
            y += 1
        elif char == "KEY_LEFT":
            x -= 1

        screen.addstr(y, x, "f")

        screen.refresh()



    curses.endwin()

wrapper(main)