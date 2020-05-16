

import curses
from curses import ascii
from curses import panel
from curses import wrapper


def main():
    screen = curses.initscr()
    curses.noecho()
    board1 = curses.newwin(20, 40, 0, 0)
    board2 = curses.newwin(20, 40, 0, 40)
    board1.border()
    #board1.refresh()
    board1.addstr(1, 5, "helloworld!")
    board1.refresh()
    board2.border()
    board2.refresh()
    curses.curs_set(False)
    curses.napms(7000)
    curses.endwin()

wrapper(main())