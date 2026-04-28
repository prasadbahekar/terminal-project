import curses
import random

# ==========================
# RETRO TIC TAC TOE
# ==========================

BOARD = [" "] * 9


def setup_colors():
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)      # Title
    curses.init_pair(2, curses.COLOR_YELLOW, -1)    # Border
    curses.init_pair(3, curses.COLOR_GREEN, -1)     # X
    curses.init_pair(4, curses.COLOR_RED, -1)       # O
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)   # Footer
    curses.init_pair(6, curses.COLOR_WHITE, -1)     # Normal
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Selected


def draw_box(stdscr, y, x, h, w):
    for i in range(w):
        stdscr.addstr(y, x + i, "-", curses.color_pair(2))
        stdscr.addstr(y + h, x + i, "-", curses.color_pair(2))

    for i in range(h + 1):
        stdscr.addstr(y + i, x, "|", curses.color_pair(2))
        stdscr.addstr(y + i, x + w - 1, "|", curses.color_pair(2))

    stdscr.addstr(y, x, "+", curses.color_pair(2))
    stdscr.addstr(y, x + w - 1, "+", curses.color_pair(2))
    stdscr.addstr(y + h, x, "+", curses.color_pair(2))
    stdscr.addstr(y + h, x + w - 1, "+", curses.color_pair(2))


def draw_board(stdscr, selected):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    title = "RETRO TIC TAC TOE"
    stdscr.addstr(1, w // 2 - len(title) // 2,
                  title, curses.color_pair(1) | curses.A_BOLD)

    start_y = 5
    start_x = w // 2 - 10

    cell = 0

    for row in range(3):
        for col in range(3):
            y = start_y + row * 4
            x = start_x + col * 7

            # Use different border color for selected cell
            if cell == selected:
                # Draw selected cell border with highlight
                for i in range(7):
                    stdscr.addstr(y, x + i, "-", curses.color_pair(7) | curses.A_BOLD)
                    stdscr.addstr(y + 3, x + i, "-", curses.color_pair(7) | curses.A_BOLD)
                
                for i in range(4):
                    stdscr.addstr(y + i, x, "|", curses.color_pair(7) | curses.A_BOLD)
                    stdscr.addstr(y + i, x + 6, "|", curses.color_pair(7) | curses.A_BOLD)
                
                stdscr.addstr(y, x, "+", curses.color_pair(7) | curses.A_BOLD)
                stdscr.addstr(y, x + 6, "+", curses.color_pair(7) | curses.A_BOLD)
                stdscr.addstr(y + 3, x, "+", curses.color_pair(7) | curses.A_BOLD)
                stdscr.addstr(y + 3, x + 6, "+", curses.color_pair(7) | curses.A_BOLD)
            else:
                draw_box(stdscr, y, x, 3, 7)

            value = BOARD[cell]

            if value == "X":
                color = curses.color_pair(3) | curses.A_BOLD
            elif value == "O":
                color = curses.color_pair(4) | curses.A_BOLD
            else:
                if cell == selected:
                    color = curses.color_pair(7) | curses.A_BOLD
                else:
                    color = curses.color_pair(6)

            stdscr.addstr(y + 1, x + 3, value if value != " " else str(cell + 1), color)

            cell += 1

    footer = "Arrows = Move | Enter = Select | Q = Quit"
    stdscr.addstr(start_y + 14, w // 2 - len(footer) // 2,
                  footer, curses.color_pair(5))

    stdscr.refresh()


def winner():
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in wins:
        if BOARD[a] == BOARD[b] == BOARD[c] and BOARD[a] != " ":
            return BOARD[a]

    if " " not in BOARD:
        return "Draw"

    return None


def ai_move():
    empty = [i for i in range(9) if BOARD[i] == " "]
    if empty:
        BOARD[random.choice(empty)] = "O"


def message(stdscr, text, color):
    h, w = stdscr.getmaxyx()
    stdscr.addstr(19, w // 2 - len(text)//2, text,
                  curses.color_pair(color) | curses.A_BOLD)
    stdscr.refresh()
    curses.napms(1800)


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    setup_colors()

    selected = 0

    while True:
        draw_board(stdscr, selected)

        result = winner()
        if result:
            if result == "X":
                message(stdscr, "YOU WIN!", 3)
            elif result == "O":
                message(stdscr, "COMPUTER WINS!", 4)
            else:
                message(stdscr, "DRAW!", 5)
            break

        key = stdscr.getch()

        if key == ord("q") or key == ord("Q"):
            break

        elif key == curses.KEY_UP:
            if selected >= 3:
                selected -= 3

        elif key == curses.KEY_DOWN:
            if selected <= 5:
                selected += 3

        elif key == curses.KEY_LEFT:
            if selected % 3 != 0:
                selected -= 1

        elif key == curses.KEY_RIGHT:
            if selected % 3 != 2:
                selected += 1

        elif key in [10, 13]:
            if BOARD[selected] == " ":
                BOARD[selected] = "X"

                if not winner():
                    ai_move()


curses.wrapper(main)