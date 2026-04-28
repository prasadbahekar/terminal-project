import curses
import random


# =========================
# RETRO SNAKE (Decorated)
# =========================

BOARD_W = 60     # width
BOARD_H = 20     # height


def create_food(snake):
    while True:
        food = [
            random.randint(1, BOARD_H - 2),
            random.randint(1, BOARD_W - 2)
        ]
        if food not in snake:
            return food


def draw_border(stdscr, start_y, start_x):
    # Top / Bottom
    for x in range(BOARD_W):
        stdscr.addstr(start_y, start_x + x, "-", curses.color_pair(2))
        stdscr.addstr(start_y + BOARD_H - 1, start_x + x, "-", curses.color_pair(2))

    # Left / Right
    for y in range(BOARD_H):
        stdscr.addstr(start_y + y, start_x, "|", curses.color_pair(2))
        stdscr.addstr(start_y + y, start_x + BOARD_W - 1, "|", curses.color_pair(2))

    # Corners
    stdscr.addstr(start_y, start_x, "+", curses.color_pair(2))
    stdscr.addstr(start_y, start_x + BOARD_W - 1, "+", curses.color_pair(2))
    stdscr.addstr(start_y + BOARD_H - 1, start_x, "+", curses.color_pair(2))
    stdscr.addstr(start_y + BOARD_H - 1, start_x + BOARD_W - 1, "+", curses.color_pair(2))


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(90)
    stdscr.keypad(True)

    # Colors
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_GREEN, -1)     # Snake
    curses.init_pair(2, curses.COLOR_YELLOW, -1)    # Border
    curses.init_pair(3, curses.COLOR_RED, -1)       # Food
    curses.init_pair(4, curses.COLOR_CYAN, -1)      # Title
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)   # Score
    curses.init_pair(6, curses.COLOR_WHITE, -1)     # Text

    sh, sw = stdscr.getmaxyx()

    if sh < BOARD_H + 6 or sw < BOARD_W + 4:
        stdscr.addstr(0, 0, "Terminal too small. Resize and run again.")
        stdscr.getch()
        return

    start_y = (sh - BOARD_H) // 2
    start_x = (sw - BOARD_W) // 2

    snake = [
        [BOARD_H // 2, BOARD_W // 4],
        [BOARD_H // 2, BOARD_W // 4 - 1],
        [BOARD_H // 2, BOARD_W // 4 - 2]
    ]

    direction = curses.KEY_RIGHT
    food = create_food(snake)
    score = 0

    while True:
        stdscr.clear()

        # Decorations
        title = "RETRO SNAKE"
        stdscr.addstr(start_y - 2, sw // 2 - len(title) // 2,
                      title, curses.color_pair(4) | curses.A_BOLD)

        stdscr.addstr(start_y - 1, start_x,
                      f"Score: {score}",
                      curses.color_pair(5) | curses.A_BOLD)

        draw_border(stdscr, start_y, start_x)

        # Controls
        stdscr.addstr(start_y + BOARD_H + 1, start_x,
                      "Arrows = Move   Q = Quit",
                      curses.color_pair(6))

        # Food
        stdscr.addstr(start_y + food[0], start_x + food[1],
                      "*", curses.color_pair(3) | curses.A_BOLD)

        # Snake
        for i, part in enumerate(snake):
            ch = "@"
            color = curses.color_pair(1) | curses.A_BOLD

            if i == 0:
                ch = "O"   # Head

            stdscr.addstr(start_y + part[0], start_x + part[1], ch, color)

        stdscr.refresh()

        # Input
        key = stdscr.getch()

        if key == ord("q") or key == ord("Q"):
            break

        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            direction = key

        # New head
        head = snake[0].copy()

        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        # Collision with border
        if (
            head[0] == 0 or
            head[0] == BOARD_H - 1 or
            head[1] == 0 or
            head[1] == BOARD_W - 1 or
            head in snake
        ):
            msg = f"GAME OVER | SCORE: {score}"
            stdscr.clear()
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2,
                          msg, curses.color_pair(3) | curses.A_BOLD)
            stdscr.refresh()
            curses.napms(2200)
            break

        snake.insert(0, head)

        # Eat food
        if head == food:
            score += 1
            food = create_food(snake)
        else:
            snake.pop()


curses.wrapper(main)