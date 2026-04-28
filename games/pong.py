import curses
import time
import random

# ==========================
# RETRO PONG
# ==========================

PADDLE_H = 5
BALL_SPEED = 0.05


def setup_colors():
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_CYAN, -1)      # Title
    curses.init_pair(2, curses.COLOR_YELLOW, -1)    # Border
    curses.init_pair(3, curses.COLOR_GREEN, -1)     # Left paddle
    curses.init_pair(4, curses.COLOR_RED, -1)       # Right paddle
    curses.init_pair(5, curses.COLOR_WHITE, -1)     # Ball
    curses.init_pair(6, curses.COLOR_MAGENTA, -1)   # Score
    curses.init_pair(7, curses.COLOR_BLUE, -1)      # Center line


def draw_border(stdscr, h, w):
    stdscr.border()


def draw_center_line(stdscr, h, w):
    for y in range(1, h - 1):
        if y % 2 == 0:
            stdscr.addstr(y, w // 2, "|", curses.color_pair(7))


def draw_paddle(stdscr, x, y, color):
    for i in range(PADDLE_H):
        stdscr.addstr(y + i, x, "█", curses.color_pair(color) | curses.A_BOLD)


def reset_ball(h, w):
    dx = random.choice([-1, 1])
    dy = random.choice([-1, 1])
    return [h // 2, w // 2, dy, dx]


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(1)
    stdscr.keypad(True)

    setup_colors()

    h, w = stdscr.getmaxyx()

    left_y = h // 2 - PADDLE_H // 2
    right_y = h // 2 - PADDLE_H // 2

    ball = reset_ball(h, w)

    score_left = 0
    score_right = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        draw_border(stdscr, h, w)
        draw_center_line(stdscr, h, w)

        title = "RETRO PONG"
        stdscr.addstr(0, w // 2 - len(title) // 2,
                      title, curses.color_pair(1) | curses.A_BOLD)

        score_text = f"{score_left} : {score_right}"
        stdscr.addstr(1, w // 2 - len(score_text) // 2,
                      score_text, curses.color_pair(6) | curses.A_BOLD)

        # Controls
        stdscr.addstr(h - 1, 2,
                      "W/S = Move | Q = Quit",
                      curses.color_pair(6))

        # Draw paddles
        draw_paddle(stdscr, 2, left_y, 3)
        draw_paddle(stdscr, w - 3, right_y, 4)

        # Draw ball
        stdscr.addstr(ball[0], ball[1], "●",
                      curses.color_pair(5) | curses.A_BOLD)

        stdscr.refresh()

        # Input
        key = stdscr.getch()

        if key in [ord("q"), ord("Q")]:
            break

        if key == ord("w") and left_y > 1:
            left_y -= 1
        elif key == ord("s") and left_y + PADDLE_H < h - 1:
            left_y += 1

        # AI paddle follows ball
        if ball[0] < right_y and right_y > 1:
            right_y -= 1
        elif ball[0] > right_y + PADDLE_H - 1 and right_y + PADDLE_H < h - 1:
            right_y += 1

        # Move ball
        ball[0] += ball[2]
        ball[1] += ball[3]

        # Top/bottom bounce
        if ball[0] <= 1 or ball[0] >= h - 2:
            ball[2] *= -1

        # Left paddle collision
        if ball[1] == 3 and left_y <= ball[0] < left_y + PADDLE_H:
            ball[3] *= -1

        # Right paddle collision
        if ball[1] == w - 4 and right_y <= ball[0] < right_y + PADDLE_H:
            ball[3] *= -1

        # Score
        if ball[1] <= 1:
            score_right += 1
            ball = reset_ball(h, w)

        elif ball[1] >= w - 2:
            score_left += 1
            ball = reset_ball(h, w)

        time.sleep(BALL_SPEED)


curses.wrapper(main)