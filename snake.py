import curses
import random

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()

    snake = [
        [sh // 2, sw // 4],
        [sh // 2, sw // 4 - 1],
        [sh // 2, sw // 4 - 2]
    ]

    key = curses.KEY_RIGHT

    food = [sh // 2, sw // 2]
    stdscr.addch(food[0], food[1], '*')

    score = 0

    while True:
        next_key = stdscr.getch()
        if next_key != -1:
            key = next_key

        head = snake[0].copy()

        if key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1

        if (
            head[0] in [0, sh] or
            head[1] in [0, sw] or
            head in snake
        ):
            msg = f"Game Over! Score: {score}"
            stdscr.clear()
            stdscr.addstr(sh // 2, sw // 2 - len(msg)//2, msg)
            stdscr.refresh()
            curses.napms(2000)
            break

        snake.insert(0, head)

        #Food
        if head == food:
            score += 1
            while food in snake:
                food = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
            stdscr.addch(food[0], food[1], '*')
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        stdscr.addch(head[0], head[1], '#')
        stdscr.addstr(0, 2, f'Score: {score}')

curses.wrapper(main)