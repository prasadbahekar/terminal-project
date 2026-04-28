import curses
import subprocess
import sys
import os

menu = ["Snake", "Exit"]


def setup_colors():
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)      # Title
    curses.init_pair(2, curses.COLOR_YELLOW, -1)    # Border
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)  # Selected
    curses.init_pair(4, curses.COLOR_WHITE, -1)     # Normal
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)   # Footer


def draw_border(stdscr, h, w):
    # top
    for x in range(w - 1):
        stdscr.addstr(0, x, "-")

    # bottom
    for x in range(w - 2):
        stdscr.addstr(h - 1, x, "-")

    # left
    for y in range(1, h - 1):
        stdscr.addstr(y, 0, "|")

    # right
    for y in range(1, h - 1):
        stdscr.addstr(y, w - 2, "|")

    # corners (safe positions)
    stdscr.addstr(0, 0, "+")
    stdscr.addstr(0, w - 2, "+")
    stdscr.addstr(h - 1, 0, "+")
    stdscr.addstr(h - 1, w - 2, "+")


def center_text(stdscr, y, text, color=0):
    h, w = stdscr.getmaxyx()
    x = max(0, w // 2 - len(text) // 2)
    if y < h:
        stdscr.addstr(y, x, text, color)


def draw_menu(stdscr, selected):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    if h < 20 or w < 60:
        center_text(stdscr, h // 2, "Resize terminal window bigger.", curses.color_pair(4))
        stdscr.refresh()
        return

    draw_border(stdscr, h, w)

    title = "RETRO GAME HUB"
    center_text(stdscr, 2, title, curses.color_pair(1) | curses.A_BOLD)

    subtitle = "Classic Terminal Arcade"
    center_text(stdscr, 4, subtitle, curses.color_pair(5))

    start_y = 8

    for i, item in enumerate(menu):
        text = item

        if i == selected:
            text = f"> {item} <"
            center_text(stdscr, start_y + i * 2, text,
                        curses.color_pair(3) | curses.A_BOLD)
        else:
            center_text(stdscr, start_y + i * 2, text,
                        curses.color_pair(4))

    footer = "UP/DOWN = Move   ENTER = Select"
    center_text(stdscr, h - 2, footer, curses.color_pair(5))

    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    setup_colors()

    selected = 0

    while True:
        draw_menu(stdscr, selected)

        key = stdscr.getch()
        base_dir = os.path.dirname(os.path.abspath(__file__))

        if key == curses.KEY_UP:
            selected = (selected - 1) % len(menu)

        elif key == curses.KEY_DOWN:
            selected = (selected + 1) % len(menu)

        elif key in [10, 13]:
            if menu[selected] == "Snake":
                curses.endwin()
                game_path = os.path.join(base_dir, "games", "snake.py")
                subprocess.run([sys.executable, game_path])
                stdscr.clear()

            elif menu[selected] == "Exit":
                break


curses.wrapper(main)