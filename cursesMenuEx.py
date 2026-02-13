import curses

def menu(stdscr, options):
    curses.curs_set(0)
    current_row = 0

    while True:
        stdscr.clear()
        for idx, row in enumerate(options):
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(idx, 0, row)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(idx, 0, row)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_row = (current_row - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_row = (current_row + 1) % len(options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return options[current_row]

        stdscr.refresh()

options = ["Option 1", "Option 2", "Option 3", "Exit"]
selected = curses.wrapper(menu, options)
print("Selected:", selected)
