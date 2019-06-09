import curses
try:
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(1)
    stdscr.refresh()
    while 1:
        c = stdscr.getch()
        if c == ord('w'):
            print('frente')
        elif c == ord('s'):
            print('tras')
        elif c == ord('a'):
            print('esquerda')
        elif c == ord('d'):
            print('direita')
        if c == ord('q'):
            exit(0)

finally:
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()


